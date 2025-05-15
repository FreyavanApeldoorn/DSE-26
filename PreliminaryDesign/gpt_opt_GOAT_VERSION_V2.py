# =========================== integration.py ============================ #
#  Single-entry mass-optimiser for the AeroShield FW-VTOL UAV            #
# ---------------------------------------------------------------------- #

import numpy as np
from functools import lru_cache
from scipy.optimize import minimize, Bounds

from Classes.Contraints_for_mass_calculations import Constraints, powerLoading
from Classes.vtol_propulsion_sizing import VTOLProp
from Classes.electric_propulsion_mass_sizing import PropMass
from Classes.Battery_Mass_Calculations import BattMass

# ───────────────────── Defaults (can be overridden) ──────────────────── #
DEFAULTS = dict(
    # Performance & aero
    V_cruise=100 / 3.6,  # m/s
    stall_margin=2.0,
    AR=8.0,
    CL_max=1.5,
    CD0=0.040,
    e=0.7,
    prop_eff=0.85,
    R_C=3.0,  # m/s climb
    # Geometric limits
    span_max=3.0,  # m
    STOT_S_W=1.35,
    n_props_vtol=4,
    n_props_cruise=1,
    # Motor / prop constants
    U_max=25.5,
    F1=0.889,
    E1=-0.288,
    E2=0.1588,
    f_install=1.0,
    K_material=0.6,
    n_blades=4,
    K_p=0.0938,
    # Battery & mission
    t_hover=4 * 60,  # s
    t_loiter=0,
    E_spec=168,  # Wh/kg
    eta_batt=0.95,
    f_usable=6000,  # mAh
    eta_elec=0.95,
    LD_max=12,
    CL_cruise=0.846,
    CD_cruise=0.04,
    h_end=100,
    h_start=0,
    # Fixed masses / fractions
    M_payload=5.0,  # kg
    MF_struct=0.35,
    MF_avion=0.05,
    MF_subsystem=0.07,
)

rho, g = 0.9013, 9.81  # constants

# ─────────────────── Fixed-point mass loop (cached) ──────────────────── #
_CFG = {}  # will be filled inside optimise()


@lru_cache(maxsize=256)
def _mass_loop(W_S: float, P_W: float) -> float:
    cfg = _CFG
    MTOM = 30.0
    while True:
        W_TO = MTOM * g

        # VTOL sizing
        vtol = VTOLProp(W_S, cfg["STOT_S_W"], W_TO, cfg["n_props_vtol"])
        P_VTOL, S_prop, DL, Thrust = vtol.power_required_vtol()
        D_prop_vtol = 2 * np.sqrt(S_prop / np.pi)

        # Propulsion masses
        prop = PropMass(
            W_TO * P_W,
            P_VTOL,
            cfg["U_max"],
            cfg["F1"],
            cfg["E1"],
            cfg["E2"],
            cfg["f_install"],
            cfg["f_install"],
            cfg["n_props_cruise"],
            cfg["n_props_vtol"],
            cfg["K_material"],
            cfg["n_props_cruise"],
            cfg["n_props_vtol"],
            cfg["n_blades"],
            cfg["n_blades"],
            D_prop_vtol,
            cfg["K_p"],
        )
        M_FW, M_VT = prop.calculate_propulsion_mass()

        # Battery fraction
        batt = BattMass(
            cfg["t_hover"],
            cfg["t_loiter"],
            MTOM,
            cfg["E_spec"],
            cfg["eta_batt"],
            cfg["f_usable"],
            cfg["eta_elec"],
            Thrust,
            DL,
            cfg["LD_max"],
            cfg["CL_cruise"],
            cfg["CD_cruise"],
            W_S,
            cfg["h_end"],
            cfg["h_start"],
            P_VTOL,
            cfg["n_props_vtol"],
        )
        MF_batt, _ = batt.Batt_Mass_Total()

        denom = 1 - (MF_batt + cfg["MF_struct"] + cfg["MF_subsystem"] + cfg["MF_avion"])
        MTOM_new = (M_VT + M_FW + cfg["M_payload"]) / denom
        if abs(MTOM_new - MTOM) < 1e-3:
            return MTOM_new
        MTOM = MTOM_new


# ───────────────────────── Constraint helpers ────────────────────────── #
def _build_constraints(cfg):
    cons = Constraints(
        cfg["V_cruise"] / cfg["stall_margin"],
        cfg["V_cruise"],
        cfg["e"],
        cfg["AR"],
        cfg["CL_max"],
        cfg["CD0"],
        cfg["prop_eff"],
        cfg["R_C"],
    )

    def g_stall(ws, pw):
        ws_max = (
            0.5 * rho * (cfg["V_cruise"] / cfg["stall_margin"]) ** 2 * cfg["CL_max"]
        )
        return ws_max - ws

    def g_cruise(ws, pw):
        req = powerLoading(
            cons.thrustLoadingCruise(ws), cfg["V_cruise"], cfg["prop_eff"]
        )
        return pw - req

    def g_climb(ws, pw):
        Vroc = cons.Vroc(ws)
        req = powerLoading(
            cons.thrustLoadingClimb(Vroc, ws, cfg["R_C"], cons.q_climb(Vroc)),
            Vroc,
            cfg["prop_eff"],
        )
        return pw - req

    def g_span(ws, pw):
        span = np.sqrt(cfg["AR"] * (_mass_loop(ws, pw) * g / ws))
        return cfg["span_max"] - span

    def g_prop_cr(ws, pw):
        mtom = _mass_loop(ws, pw)
        D_cr = cfg["K_p"] * ((mtom * g) * pw / cfg["n_props_cruise"]) ** 0.25
        return 1 - D_cr

    def g_prop_vt(ws, pw):
        mtom = _mass_loop(ws, pw)
        vtol = VTOLProp(ws, cfg["STOT_S_W"], mtom * g, cfg["n_props_vtol"])
        _, S_p, _, _ = vtol.power_required_vtol()
        D_v = 2 * np.sqrt(S_p / np.pi)
        return 1 - D_v

    return [g_stall, g_cruise, g_climb, g_span, g_prop_cr, g_prop_vt]


# ─────────────────────────── Main optimiser ──────────────────────────── #
def optimise(inputs: dict | None = None) -> dict:
    """Run the optimiser; returns a dict with optimum & masses."""
    global _CFG
    _CFG = {**DEFAULTS, **(inputs or {})}  # freeze for caching

    # --- SciPy set-up
    bounds = Bounds([20.0, 2.0], [200.0, 25.0])
    W_S0 = (
        0.6
        * Constraints(
            _CFG["V_cruise"] / _CFG["stall_margin"],
            _CFG["V_cruise"],
            _CFG["e"],
            _CFG["AR"],
            _CFG["CL_max"],
            _CFG["CD0"],
            _CFG["prop_eff"],
            _CFG["R_C"],
        ).WingLoading_Vstall()
    )
    x0 = np.array([W_S0, 6.0])

    # Build constraint wrappers
    cons_fns = _build_constraints(_CFG)
    cons = [{"type": "ineq", "fun": lambda x, f=f: f(x[0], x[1])} for f in cons_fns]

    res = minimize(
        lambda x: _mass_loop(x[0], x[1]),
        x0,
        method="SLSQP",
        bounds=bounds,
        constraints=cons,
        options={"ftol": 1e-3, "maxiter": 120},
    )

    if not res.success:
        raise RuntimeError(res.message)

    W_S_opt, P_W_opt = res.x
    MTOM_opt = _mass_loop(W_S_opt, P_W_opt)
    span_opt = np.sqrt(_CFG["AR"] * (MTOM_opt * g / W_S_opt))

    # Prop diameters
    vtol = VTOLProp(W_S_opt, _CFG["STOT_S_W"], MTOM_opt * g, _CFG["n_props_vtol"])
    _, S_p, _, _ = vtol.power_required_vtol()
    D_v = 2 * np.sqrt(S_p / np.pi)
    D_cr = _CFG["K_p"] * ((MTOM_opt * g) * P_W_opt / _CFG["n_props_cruise"]) ** 0.25

    # Mass breakdown (simple)
    out = dict(_CFG)
    out.update(
        dict(
            W_S=W_S_opt,
            P_W=P_W_opt,
            MTOM=MTOM_opt,
            span=span_opt,
            D_cruise=D_cr,
            D_vtol=D_v,
            Structure=_CFG["MF_struct"] * MTOM_opt,
            Avionics=_CFG["MF_avion"] * MTOM_opt,
            Subsystem=_CFG["MF_subsystem"] * MTOM_opt,
        )
    )

    # --- Console report
    print("\n*** Optimisation complete ***")
    print(f"W/S  = {W_S_opt:6.2f} N/m²   P/W  = {P_W_opt:6.2f} W/N")
    print(f"MTOM = {MTOM_opt:6.2f} kg    Span = {span_opt:4.3f} m")
    print(f"Cruise prop Ø = {D_cr:4.3f} m   VTOL prop Ø = {D_v:4.3f} m")
    return out


# ───────────────────────── Script entry point ────────────────────────── #
if __name__ == "__main__":
    optimise()  # run with all defaults
