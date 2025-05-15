# =========================== integration.py ============================ #
#  Lean FW-VTOL optimiser with robust seeding                             #
# ---------------------------------------------------------------------- #

import numpy as np
from functools import lru_cache
from scipy.optimize import minimize, Bounds

from Contraints_for_mass_calculations import Constraints, powerLoading
from vtol_propulsion_sizing import VTOLProp
from electric_propulsion_mass_sizing import PropMass
from Battery_Mass_Calculations import BattMass

# ──────────────── Defaults (override via optimise()) ─────────────────── #
DEFAULTS = dict(
    # Performance & aero
    V_cruise=100 / 3.6,
    stall_margin=2.0,
    AR=8.0,
    CL_max=1.5,
    CD0=0.040,
    e=0.7,
    prop_eff=0.85,
    R_C=3.0,
    # Geometric limits & config
    span_max=3.0,
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
    MF_subsystem=0.07,
)

rho, g = 0.9013, 9.81  # constants
_CFG = {}  # filled inside optimise(), used by caches


# ───────────────────── Cached mass loop (expensive) ──────────────────── #
@lru_cache(maxsize=256)
def _mass_loop(W_S: float, P_W: float) -> float:
    c = _CFG
    MTOM = 30.0
    while True:
        W_TO = MTOM * g
        vtol = VTOLProp(W_S, c["STOT_S_W"], W_TO, c["n_props_vtol"])
        P_VTOL, S_p, DL, T = vtol.power_required_vtol()
        D_v = 2 * np.sqrt(S_p / np.pi)

        prop = PropMass(
            W_TO * P_W,
            P_VTOL,
            c["U_max"],
            c["F1"],
            c["E1"],
            c["E2"],
            c["f_install"],
            c["f_install"],
            c["n_props_cruise"],
            c["n_props_vtol"],
            c["K_material"],
            c["n_props_cruise"],
            c["n_props_vtol"],
            c["n_blades"],
            c["n_blades"],
            D_v,
            c["K_p"],
        )
        M_FW, M_VT = prop.calculate_propulsion_mass()

        batt = BattMass(
            c["t_hover"],
            c["t_loiter"],
            MTOM,
            c["E_spec"],
            c["eta_batt"],
            c["f_usable"],
            c["eta_elec"],
            T,
            DL,
            c["LD_max"],
            c["CL_cruise"],
            c["CD_cruise"],
            W_S,
            c["h_end"],
            c["h_start"],
            P_VTOL,
            c["n_props_vtol"],
        )
        MF_batt, _ = batt.Batt_Mass_Total()

        denom = 1 - (MF_batt + c["MF_struct"] + c["MF_subsystem"] + c["MF_avion"])
        MTOM_new = (M_VT + M_FW + c["M_payload"]) / denom
        if abs(MTOM_new - MTOM) < 1e-3:
            return MTOM_new
        MTOM = MTOM_new


# ───────────────────── Constraint builder (cheap) ────────────────────── #
def _constraint_functions(cfg):
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

    def g_stall(ws, _):  # W/S ≤ limit from stall margin
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
        return 0.5 - D_cr

    def g_prop_vt(ws, pw):
        mtom = _mass_loop(ws, pw)
        vtol = VTOLProp(ws, cfg["STOT_S_W"], mtom * g, cfg["n_props_vtol"])
        _, S_p, _, _ = vtol.power_required_vtol()
        D_v = 2 * np.sqrt(S_p / np.pi)
        return 0.5 - D_v

    return [g_stall, g_cruise, g_climb, g_span, g_prop_cr, g_prop_vt]


# ──────────────────── Coarse grid seed for globality ─────────────────── #
def _coarse_seed(bounds: Bounds, g_list, n_ws=10, n_pw=8):
    ws_lin = np.linspace(bounds.lb[0], bounds.ub[0], n_ws)
    pw_lin = np.linspace(bounds.lb[1], bounds.ub[1], n_pw)
    best = None
    f_best = np.inf
    for ws in ws_lin:
        for pw in pw_lin:
            if all(g(ws, pw) >= 0 for g in g_list):  # feasible?
                f = _mass_loop(ws, pw)
                if f < f_best:
                    f_best, best = f, (ws, pw)
    if best is None:
        raise RuntimeError("No feasible seed found in coarse grid.")
    return np.array(best)


# ──────────────────────── Main optimise() API ────────────────────────── #
def optimise(overrides: dict | None = None) -> dict:
    """Run sizing optimisation; returns dict with optimum & masses."""
    global _CFG
    _CFG = {**DEFAULTS, **(overrides or {})}

    # ---- Bounds and constraint wrappers
    bnds = Bounds([20.0, 2.0], [200.0, 25.0])
    g_list = _constraint_functions(_CFG)
    cons = [{"type": "ineq", "fun": lambda x, f=f: f(x[0], x[1])} for f in g_list]

    # ---- Seed from coarse grid, then three local starts
    seed = _coarse_seed(bnds, g_list)
    starts = [seed, seed * np.array([1.1, 0.9]), seed * np.array([0.9, 1.1])]

    best_res = None
    for x0 in starts:
        res = minimize(
            lambda x: _mass_loop(x[0], x[1]),
            x0,
            method="SLSQP",
            bounds=bnds,
            constraints=cons,
            options={"ftol": 1e-3, "maxiter": 120},
        )
        if res.success and (best_res is None or res.fun < best_res.fun):
            best_res = res

    if best_res is None or not best_res.success:
        raise RuntimeError("Optimiser failed.")
    W_S_opt, P_W_opt = best_res.x
    MTOM_opt = best_res.fun
    span_opt = np.sqrt(_CFG["AR"] * (MTOM_opt * g / W_S_opt))

    # Prop diameters
    vtol = VTOLProp(W_S_opt, _CFG["STOT_S_W"], MTOM_opt * g, _CFG["n_props_vtol"])
    _, S_p, _, _ = vtol.power_required_vtol()
    D_v = 2 * np.sqrt(S_p / np.pi)
    D_cr = _CFG["K_p"] * ((MTOM_opt * g) * P_W_opt / _CFG["n_props_cruise"]) ** 0.25

    result = dict(
        _CFG,
        W_S=W_S_opt,
        P_W=P_W_opt,
        MTOM=MTOM_opt,
        span=span_opt,
        D_cruise=D_cr,
        D_vtol=D_v,
    )
    # simple breakdown
    result.update(
        Structure=_CFG["MF_struct"] * MTOM_opt,
        Avionics=_CFG["MF_avion"] * MTOM_opt,
        Subsystem=_CFG["MF_subsystem"] * MTOM_opt,
    )

    print("\n*** Optimisation complete ***")
    print(f"W/S  = {W_S_opt:6.2f} N/m²   P/W  = {P_W_opt:6.2f} W/N")
    print(
        f"MTOM = {MTOM_opt:6.2f} kg    Span = {span_opt:4.3f} m (limit { _CFG['span_max']} m)"
    )
    print(f"Cruise prop Ø = {D_cr:4.3f} m   VTOL prop Ø = {D_v:4.3f} m")
    return result


# ────────────────────────── CLI convenience ─────────────────────────── #
if __name__ == "__main__":
    optimise()  # run with defaults
