# ============================== integration.py =========================== #
#  One-stop script that runs the FW-VTOL mass-optimiser and updates        #
#  the shared `inputs` dictionary with the resulting dimensions & masses.  #
# ------------------------------------------------------------------------ #
from __future__ import annotations
import numpy as np
from dataclasses import dataclass
from functools import lru_cache
from typing import Tuple
from scipy.optimize import minimize, Bounds

from Contraints_for_mass_calculations import Constraints, powerLoading
from vtol_propulsion_sizing import VTOLProp
from electric_propulsion_mass_sizing import PropMass
from Battery_Mass_Calculations import BattMass

# ─────────────────────────────────────────────────────────────────────────
# 1.  Global defaults (these may be overwritten by `inputs`)              |
# ─────────────────────────────────────────────────────────────────────────
DEFAULTS = dict(
    # Performance & aero
    V_cruise=100 / 3.6,  # m/s
    stall_margin=2.0,
    AR=8.0,
    CL_max=1.5,
    CD0=0.040,
    e=0.7,
    prop_eff_cr=0.85,
    R_C=3.0,
    span_max=3.0,
    # Geometry & config
    STOT_S_W=1.35,
    n_props_vtol=4,
    n_props_cruise=1,
    # Motor/prop constants
    U_max=25.5,
    F1=0.889,
    E1=-0.288,
    E2=0.1588,
    f_install=1.0,
    K_material=0.6,
    n_blades=4,
    K_p=0.0938,
    # Battery & mission
    t_hover=4 * 60,
    t_loiter=0,
    E_spec=168,
    eta_batt=0.95,
    f_usable=6000,
    eta_elec=0.95,
    LD_max=12,
    CL_cruise=0.846,
    CD_cruise=0.04,
    h_end=100,
    h_start=0,
    # Fixed masses / fractions
    M_payload=5.0,
    MF_struct=0.35,
    MF_avion=0.05,
    MF_subsyst=0.07,
)

rho, g = 0.9013, 9.81  # constants


# ─────────────────────────────────────────────────────────────────────────
# 2.  Dataclass representing ONE design point                             |
# ─────────────────────────────────────────────────────────────────────────
@dataclass(frozen=True, slots=True)
class DP:
    W_S: float
    P_W: float
    cfg: dict  # all other constants

    # --- helper caches ---------------------------------------------------
    @property
    @lru_cache(maxsize=None)
    def vtol(self):
        return VTOLProp(
            self.W_S, self.cfg["STOT_S_W"], self.MTOW, self.cfg["n_props_vtol"]
        ).power_required_vtol()  # (P_VTOL, S_prop, DL, T)

    @property
    def MTOW(self):
        return self.MTOM * g

    @property
    @lru_cache(maxsize=None)
    def MTOM(self):
        """fixed-point mass loop"""
        mtom = 30.0
        while True:
            W_TO = mtom * g
            P_VTOL, S_p, DL, T = VTOLProp(
                self.W_S, self.cfg["STOT_S_W"], W_TO, self.cfg["n_props_vtol"]
            ).power_required_vtol()
            D_v = 2 * np.sqrt(S_p / np.pi)

            prop = PropMass(
                W_TO * self.P_W,
                P_VTOL,
                self.cfg["U_max"],
                self.cfg["F1"],
                self.cfg["E1"],
                self.cfg["E2"],
                self.cfg["f_install"],
                self.cfg["f_install"],
                self.cfg["n_props_cruise"],
                self.cfg["n_props_vtol"],
                self.cfg["K_material"],
                self.cfg["n_props_cruise"],
                self.cfg["n_props_vtol"],
                self.cfg["n_blades"],
                self.cfg["n_blades"],
                D_v,
                self.cfg["K_p"],
            )
            M_FW, M_VT = prop.calculate_propulsion_mass()

            batt = BattMass(
                self.cfg["t_hover"],
                self.cfg["t_loiter"],
                mtom,
                self.cfg["E_spec"],
                self.cfg["eta_batt"],
                self.cfg["f_usable"],
                self.cfg["eta_elec"],
                T,
                DL,
                self.cfg["LD_max"],
                self.cfg["CL_cruise"],
                self.cfg["CD_cruise"],
                self.W_S,
                self.cfg["h_end"],
                self.cfg["h_start"],
                P_VTOL,
                self.cfg["n_props_vtol"],
            )
            MF_batt, _ = batt.Batt_Mass_Total()

            denom = 1.0 - (
                MF_batt
                + self.cfg["MF_struct"]
                + self.cfg["MF_subsyst"]
                + self.cfg["MF_avion"]
            )
            mtom_new = (M_VT + M_FW + self.cfg["M_payload"]) / denom
            if abs(mtom_new - mtom) < 1e-3:
                return mtom_new
            mtom = mtom_new

    # --- derived geometry ------------------------------------------------
    @property
    def span(self):
        return np.sqrt(self.cfg["AR"] * (self.MTOW / self.W_S))

    @property
    @lru_cache(maxsize=None)
    def prop_diams(self):
        P_VTOL, S_p, _, _ = self.vtol
        D_v = 2 * np.sqrt(S_p / np.pi)
        D_c = (
            self.cfg["K_p"]
            * (self.MTOW * self.P_W / self.cfg["n_props_cruise"]) ** 0.25
        )
        return D_c, D_v


# ─────────────────────────────────────────────────────────────────────────
# 3.  Constraint functions (g ≥ 0)                                        |
# ─────────────────────────────────────────────────────────────────────────
def build_constraints(cfg):
    cons = Constraints(
        cfg["V_cruise"] / cfg["stall_margin"],
        cfg["V_cruise"],
        cfg["e"],
        cfg["AR"],
        cfg["CL_max"],
        cfg["CD0"],
        cfg["prop_eff_cr"],
        cfg["R_C"],
    )

    def g_stall(dp: DP):
        Ws_max = (
            0.5 * rho * (cfg["V_cruise"] / cfg["stall_margin"]) ** 2 * cfg["CL_max"]
        )
        return Ws_max - dp.W_S

    def g_cruise(dp: DP):
        req = powerLoading(
            cons.thrustLoadingCruise(dp.W_S), cfg["V_cruise"], cfg["prop_eff_cr"]
        )
        return dp.P_W - req

    def g_climb(dp: DP):
        Vroc = cons.Vroc(dp.W_S)
        req = powerLoading(
            cons.thrustLoadingClimb(Vroc, dp.W_S, cfg["R_C"], cons.q_climb(Vroc)),
            Vroc,
            cfg["prop_eff_cr"],
        )
        return dp.P_W - req

    def g_span(dp: DP):
        return cfg["span_max"] - dp.span

    def g_prop_cr(dp: DP):
        return 0.5 - dp.prop_diams[0]

    def g_prop_vt(dp: DP):
        return 0.5 - dp.prop_diams[1]

    return [g_stall, g_cruise, g_climb, g_span, g_prop_cr, g_prop_vt]


# ─────────────────────────────────────────────────────────────────────────
# 4.  Optimiser wrapper                                                   |
# ─────────────────────────────────────────────────────────────────────────
def optimise_uav(user_inputs: dict) -> dict:
    # merge defaults with user overrides
    cfg = {**DEFAULTS, **user_inputs}

    scale = np.array([50.0, 10.0])  # scaling for SLSQP

    def obj(z):
        dp = DP(*(z * scale), cfg)
        return dp.MTOM

    # constraint wrappers
    cons_wrapped = []
    for g in build_constraints(cfg):
        cons_wrapped.append(
            {"type": "ineq", "fun": lambda z, f=g: f(DP(*(z * scale), cfg))}
        )

    # bounds & start guess
    bounds = Bounds(np.array([20.0, 2.0]) / scale, np.array([200.0, 25.0]) / scale)
    x0 = (
        np.array(
            [
                0.6
                * Constraints(
                    cfg["V_cruise"] / cfg["stall_margin"],
                    cfg["V_cruise"],
                    cfg["e"],
                    cfg["AR"],
                    cfg["CL_max"],
                    cfg["CD0"],
                    cfg["prop_eff_cr"],
                    cfg["R_C"],
                ).WingLoading_Vstall(),
                6.0,
            ]
        )
        / scale
    )

    result = minimize(
        obj,
        x0,
        method="SLSQP",
        bounds=bounds,
        constraints=cons_wrapped,
        options={"ftol": 1e-3, "maxiter": 120},
    )

    if not result.success:
        raise RuntimeError(result.message)

    W_S_opt, P_W_opt = result.x * scale
    dp = DP(W_S_opt, P_W_opt, cfg)
    MTOM_opt = dp.MTOM
    D_cr, D_v = dp.prop_diams

    # ---------- Write back into inputs dict ----------
    out = dict(user_inputs)  # copy
    out.update(
        dict(
            W_S=W_S_opt,
            P_W=P_W_opt,
            MTOM=MTOM_opt,
            span=dp.span,
            D_cruise=D_cr,
            D_vtol=D_v,
        )
    )

    # breakdown (simple)
    out["Structure"] = cfg["MF_struct"] * MTOM_opt
    out["Avionics"] = cfg["MF_avion"] * MTOM_opt
    out["Subsystems"] = cfg["MF_subsyst"] * MTOM_opt

    print("\n*** Optimisation complete ***")
    print(f"W/S  : {W_S_opt:6.2f} N/m²")
    print(f"P/W  : {P_W_opt:6.2f} W/N")
    print(f"MTOM : {MTOM_opt:6.2f} kg")
    print(f"Span : {dp.span:4.3f} m  (limit {cfg['span_max']} m)")
    print(f"Cruise prop Ø : {D_cr:4.3f} m")
    print(f"VTOL   prop Ø : {D_v:4.3f} m")
    return out


# ─────────────────────────────────────────────────────────────────────────
# 5.  Simple CLI run                                                      |
# ─────────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    # Example: override just a couple of fields
    my_inputs = {
        "AR": 8,
        "CL_max": 1.5,
        "V_cruise": 100 / 3.6,
        # ... add or override as needed ...
    }
    results = optimise_uav(my_inputs)
    # results now holds everything for mission_profile, etc.
