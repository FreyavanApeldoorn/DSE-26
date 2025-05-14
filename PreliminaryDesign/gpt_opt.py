# =====================  Optimisation of FW-VTOL UAV  ===================== #
#  Compatible with the 14-May-2025 module versions of:                     #
#     • Battery_Mass_Calculations.py                                       #
#     • Contraints_for_mass_calculations.py                                #
#     • electric_propulsion_mass_sizing.py                                 #
#     • vtol_propulsion_sizing.py                                          #
#  Implements the mass-minimisation routine of Tyan et al. (2017).         #
# ========================================================================= #

import numpy as np
from scipy.optimize import minimize, Bounds
from functools import lru_cache  # small speed-up

from PreliminaryDesign.Classes.Contraints_for_mass_calculations import Constraints, powerLoading
from PreliminaryDesign.Classes.vtol_propulsion_sizing import VTOLProp
from PreliminaryDesign.Classes.electric_propulsion_mass_sizing import PropMass
from PreliminaryDesign.Classes.Battery_Mass_Calculations import BattMass

# --------------------------------------------------------------------- #
# 1. Global constants & fixed inputs                                   #
# --------------------------------------------------------------------- #
rho = 0.9013  # [kg m⁻³]  3000 m ISA-Std
g = 9.81  # [m s⁻²]

# –– Performance
V_CRUISE = 100 / 3.6  # 100 km h⁻¹  ⇒  m s⁻¹
M_STALL = 2.2  # stall margin
V_STALL = V_CRUISE / M_STALL  # [m s⁻¹]
R_C = 3.0  # rate-of-climb [m s⁻¹]

# –– Aerodynamics
CD0 = 0.040
e = 0.7
AR = 5
CL_MAX = 1.5
N_PROP_EFF = 0.85
b_max = 5  # max wingspan [m]

# –– Configuration
STOT_S_W = 1.35  # S_tot / S_w
N_PROPS_VTOL = 4

# –– Propulsion sizing
U_MAX = 25.5
F1, E1, E2 = 0.889, -0.288, 0.1588
N_MOT_CRUISE = 1
N_MOT_VTOL = N_PROPS_VTOL
F_INSTALL = 1.0
K_MATERIAL = 0.6
N_PROPS_CRUISE = 1
N_BLADES = 4
K_P = 0.0938

# –– Battery & mission
T_HOVER = 4 * 60  # [s]
T_LOITER = 0
E_SPEC = 168  # [Wh kg⁻¹]
ETA_BATT = 0.95
F_USABLE = 6000  # [mAh]
ETA_ELECTRIC = 0.95
L_D_MAX = 12
CL_CRUISE = 0.846
CD_CRUISE = 0.04
H_END, H_START = 100, 0  # [m]

# –– Fixed masses / fractions
M_PAYLOAD = 5.0  # [kg]
MF_STRUCT = 0.35
MF_AVIONICS = 0.05
MF_SUBSYSTEMS = 0.07

# Pre-compute stall constraint helper
_CONS = Constraints(V_STALL, V_CRUISE, e, AR, CL_MAX, CD0, N_PROP_EFF, R_C_service=0.5)


# --------------------------------------------------------------------- #
# 2. Fixed-point sizing loop (cached for speed)                         #
# --------------------------------------------------------------------- #
@lru_cache(maxsize=128)
def _mass_loop(W_S: float, P_W: float, tol: float = 1e-3, it_max: int = 20) -> float:
    """Return MTOM [kg] for candidate (W/S, P/W) after convergence."""
    MTOM = 30.0  # initial guess [kg]
    for _ in range(it_max):
        W_TO = MTOM * g
        S_wing = W_TO / W_S

        # --- VTOL sizing ----------------------------------------------
        vtol = VTOLProp(W_S, STOT_S_W, W_TO, N_PROPS_VTOL)
        P_VTOL, S_prop, DL, Thrust = vtol.power_required_vtol()
        D_prop = 2 * np.sqrt(S_prop / np.pi)

        # --- Propulsion masses ----------------------------------------
        prop = PropMass(
            P_max_cruise=W_TO * P_W,
            P_max_vtol=P_VTOL,
            U_max=U_MAX,
            F1=F1,
            E1=E1,
            E2=E2,
            f_install_cruise=F_INSTALL,
            f_install_vtol=F_INSTALL,
            n_mot_cruise=N_MOT_CRUISE,
            n_mot_vtol=N_MOT_VTOL,
            K_material=K_MATERIAL,
            n_props_cruise=N_PROPS_CRUISE,
            n_props_vtol=N_PROPS_VTOL,
            n_blades_cruise=N_BLADES,
            n_blades_vtol=N_BLADES,
            D_prop_vtol=D_prop,
            K_p=K_P,
        )
        M_FW, M_VTOL = prop.calculate_propulsion_mass()

        # --- Battery fraction -----------------------------------------
        batt = BattMass(
            T_HOVER,
            T_LOITER,
            MTOM,
            E_SPEC,
            ETA_BATT,
            F_USABLE,
            ETA_ELECTRIC,
            Thrust,
            DL,
            L_D_MAX,
            CL_CRUISE,
            CD_CRUISE,
            W_S,
            H_END,
            H_START,
            P_VTOL,
            N_PROPS_VTOL,
        )
        MF_batt, _ = batt.Batt_Mass_Total()

        # --- Update MTOM ----------------------------------------------
        denom = 1.0 - (MF_batt + MF_STRUCT + MF_SUBSYSTEMS + MF_AVIONICS)
        MTOM_new = (M_VTOL + M_FW + M_PAYLOAD) / denom

        if abs(MTOM_new - MTOM) < tol:
            return MTOM_new
        MTOM = MTOM_new

    return MTOM  # not converged (rare)


# --------------------------------------------------------------------- #
# 2b.  Mass-break-down helper (re-uses the cached loop)                 #
# --------------------------------------------------------------------- #
def _mass_breakdown(W_S: float, P_W: float):
    """
    Returns a dict with the individual masses for the converged MTOM.
    Requires no extra iterations thanks to _mass_loop's @lru_cache.
    """
    MTOM = _mass_loop(W_S, P_W)  # kg
    W_TO = MTOM * g  # N

    # -------- replicate one pass of the component sizing -------------
    vtol = VTOLProp(W_S, STOT_S_W, W_TO, N_PROPS_VTOL)
    P_VTOL, S_prop, DL, Thrust = vtol.power_required_vtol()
    D_prop = 2 * np.sqrt(S_prop / np.pi)

    prop = PropMass(
        P_max_cruise=W_TO * P_W,
        P_max_vtol=P_VTOL,
        U_max=U_MAX,
        F1=F1,
        E1=E1,
        E2=E2,
        f_install_cruise=F_INSTALL,
        f_install_vtol=F_INSTALL,
        n_mot_cruise=N_MOT_CRUISE,
        n_mot_vtol=N_MOT_VTOL,
        K_material=K_MATERIAL,
        n_props_cruise=N_PROPS_CRUISE,
        n_props_vtol=N_PROPS_VTOL,
        n_blades_cruise=N_BLADES,
        n_blades_vtol=N_BLADES,
        D_prop_vtol=D_prop,
        K_p=K_P,
    )
    M_FW, M_VTOL = prop.calculate_propulsion_mass()

    batt = BattMass(
        T_HOVER,
        T_LOITER,
        MTOM,
        E_SPEC,
        ETA_BATT,
        F_USABLE,
        ETA_ELECTRIC,
        Thrust,
        DL,
        L_D_MAX,
        CL_CRUISE,
        CD_CRUISE,
        W_S,
        H_END,
        H_START,
        P_VTOL,
        N_PROPS_VTOL,
    )
    MF_BATT, M_BATT = batt.Batt_Mass_Total()

    return {
        "MTOM": MTOM,
        "Payload": M_PAYLOAD,
        "FW-propulsion": M_FW,
        "VTOL-propulsion": M_VTOL,
        "Battery": MF_BATT * MTOM,
        "Structure": MF_STRUCT * MTOM,
        "Avionics": MF_AVIONICS * MTOM,
        "Subsystems": MF_SUBSYSTEMS * MTOM,
    }


# --------------------------------------------------------------------- #
# 3. Objective and inequality constraints                               #
# --------------------------------------------------------------------- #
def _objective(x):  # minimise MTOM
    return _mass_loop(*x)


def _stall(x):  # g(x) ≥ 0
    return _CONS.WingLoading_Vstall() - x[0]


def _cruise(x):
    W_S, P_W = x
    req = powerLoading(_CONS.thrustLoadingCruise(W_S), V_CRUISE, N_PROP_EFF)
    return P_W - req


def _climb(x):
    W_S, P_W = x
    Vroc = _CONS.Vroc(W_S)
    req = powerLoading(
        _CONS.thrustLoadingClimb(Vroc, W_S, R_C, _CONS.q_climb(Vroc)), Vroc, N_PROP_EFF
    )
    return P_W - req


def _wingspan(x):  # b ≤ 3 m
    W_S, P_W = x
    MTOM = _mass_loop(W_S, P_W)
    W_TO = MTOM * g
    S_w = W_TO / W_S
    b = np.sqrt(AR * S_w)
    return b_max - b


def _stall_margin(x):
    """
    Enforce   V_c / V_s ≥ M_STALL
    ⇒ W/S ≤ ½ ρ ( V_c / M_STALL )²  C_Lmax
    """
    W_S, _ = x
    Vs_allow = V_CRUISE / M_STALL
    W_S_allow = 0.5 * rho * Vs_allow**2 * CL_MAX  # [N m-2]
    return W_S_allow - W_S  # ≥ 0  ⇒  feasible


def _cruise_prop_diam(x):
    """
    Enforce cruise propeller diameter ≤ 0.5 m.
    D_cruise = K_P * (P_max_cruise / n_props_cruise)**(1/4)
    where P_max_cruise = (MTOM*g) * (P/W)
    """
    W_S, P_W = x
    MTOM = _mass_loop(W_S, P_W)  # kg
    W_TO = MTOM * g  # N
    P_max_cr = W_TO * P_W  # W
    D_cruise = K_P * (P_max_cr / N_PROPS_CRUISE) ** 0.25
    return (
        0.5 - D_cruise
    )  # ≥0 ⇒ D_cruise ≤ 0.5 m  :contentReference[oaicite:0]{index=0}:contentReference[oaicite:1]{index=1}


def _vtol_prop_diam(x):
    """
    Enforce VTOL propeller diameter ≤ 0.5 m.
    D_vtol = 2·sqrt(S_prop/π),  where S_prop from power_required_vtol()
    """
    W_S, P_W = x
    MTOM = _mass_loop(W_S, P_W)  # kg
    W_TO = MTOM * g  # N
    vtol = VTOLProp(W_S, STOT_S_W, W_TO, N_PROPS_VTOL)
    _, S_prop, _, _ = vtol.power_required_vtol()
    D_vtol = 2 * np.sqrt(S_prop / np.pi)
    return 0.5 - D_vtol  # ≥0 ⇒ D_vtol ≤ 0.5 m


# --------------------------------------------------------------------- #
# 4. Optimisation call                                                  #
# --------------------------------------------------------------------- #
if __name__ == "__main__":
    bounds = Bounds([20.0, 2.0], [200.0, 25.0])

    constraints = [
        {"type": "ineq", "fun": f}
        for f in (
            _cruise,
            _climb,
            _wingspan,
            _stall_margin,
        )
    ]

    # ----------   NEW: start well inside the feasible region   ----------
    x0 = np.array([0.7 * _CONS.WingLoading_Vstall(), 6.0])

    res = minimize(
        _objective,
        x0,
        method="SLSQP",
        bounds=bounds,
        constraints=constraints,
        options={"ftol": 1e-2, "maxiter": 150, "disp": True},  # slightly looser
    )

    if not res.success:
        raise RuntimeError(f"SLSQP failed → {res.message}")

    W_S_opt, P_W_opt = res.x
    MTOM_opt = res.fun

    # -------- Summary --------
    print("\n*** Optimum found ***")
    print(f"  Wing-loading  W/S : {W_S_opt:6.2f}  N m⁻²")
    print(f"  Power-loading P/W : {P_W_opt:6.2f}  W N⁻¹")
    print(f"  MTOM (minimum)    : {MTOM_opt:6.2f}  kg")

    span = np.sqrt(AR * (MTOM_opt * g) / W_S_opt)
    print(f"  Span              : {span:6.3f}  m (≤ {b_max} m)")

    # -------- Mass breakdown --------
    m = _mass_breakdown(W_S_opt, P_W_opt)
    print("\nMass breakdown (kg)")
    for k, v in m.items():
        if k != "MTOM":
            print(f"  {k:<15s}: {v:6.2f}")
    print(f"  -------------------------------")
    print(f"  Total (MTOM)      : {m['MTOM']:6.2f}")

    # -------- Propeller dimensions --------
    # Recompute one sizing pass to get propeller areas/thrust
    W_TO_opt = MTOM_opt * g
    vtol = VTOLProp(W_S_opt, STOT_S_W, W_TO_opt, N_PROPS_VTOL)
    P_VTOL_opt, S_prop_opt, _, _ = vtol.power_required_vtol()
    D_prop_vtol = 2 * np.sqrt(S_prop_opt / np.pi)

    prop = PropMass(
        P_max_cruise=W_TO_opt * P_W_opt,
        P_max_vtol=P_VTOL_opt,
        U_max=U_MAX,
        F1=F1,
        E1=E1,
        E2=E2,
        f_install_cruise=F_INSTALL,
        f_install_vtol=F_INSTALL,
        n_mot_cruise=N_MOT_CRUISE,
        n_mot_vtol=N_MOT_VTOL,
        K_material=K_MATERIAL,
        n_props_cruise=N_PROPS_CRUISE,
        n_props_vtol=N_PROPS_VTOL,
        n_blades_cruise=N_BLADES,
        n_blades_vtol=N_BLADES,
        D_prop_vtol=D_prop_vtol,
        K_p=K_P,
    )
    D_prop_cruise = (
        prop.calculate_cruise_propeller_diameter()
    )  # :contentReference[oaicite:0]{index=0}:contentReference[oaicite:1]{index=1}

    print("\nPropeller dimensions:")
    print(
        f"  Cruise propeller diameter : {D_prop_cruise:6.3f} m"
        f"  (n={N_PROPS_CRUISE}, blades={N_BLADES})"
    )
    print(
        f"  VTOL propeller diameter   : {D_prop_vtol:6.3f} m"
        f"  (n={N_PROPS_VTOL}, blades={N_BLADES})"
    )
