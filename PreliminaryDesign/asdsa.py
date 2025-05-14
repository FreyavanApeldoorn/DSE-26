# =====================  Optimisation of FW-VTOL UAV  ===================== #
#  This script implements the constrained optimisation routine proposed in #
#  Tyan et al. “Comprehensive preliminary sizing/resizing method for a      #
#  fixed-wing – VTOL electric UAV”, Aerospace Science & Technology 71       #
#  (2017) 30-41.  Objective: minimise total mass subject to performance    #
#  constraints.                                                             #
# ========================================================================= #

import numpy as np
from scipy.optimize import minimize, Bounds

from Contraints_for_mass_calculations import powerLoading, Constraints
from vtol_propulsion_sizing import VTOLProp
from electric_propulsion_mass_sizing import PropMass
from Battery_Mass_Calculations import BattMass

# ------------------------------------------------------------------------- #
# 1. Global, mission & geometric constants                                  #
# ------------------------------------------------------------------------- #
# ––– Aerodynamic / performance data –––
rho = 0.9013  # [kg m-3]      density at 3000 m
V_CRUISE = 100 / 3.6  # [m s-1]       100 km h-1
V_STALL = 13.8  # [m s-1]
CD0 = 0.040
e = 0.7
AR = 10.03
CL_MAX = 1.34
N_PROP_EFFIC = 0.85  # propeller η
R_C = 3.0  # [m s-1]       climb requirement

# ––– VTOL sizing inputs –––
STOT_S_W = 1.35  # S_tot / S_w
N_PROPS_VTOL = 4  # number VTOL rotors

# ––– Cruise / VTOL propulsion inputs –––
U_MAX = 25.5  # [V]
F1, E1, E2 = 0.889, -0.288, 0.1588
N_MOT_CRUISE = 1
N_MOT_VTOL = 4
F_INSTALL = 1.0  # install factor (both systems)
K_MATERIAL = 0.6  # composite props
N_PROPS_CRUISE = 1
N_BLADES = 4
K_P = 0.0938

# ––– Battery & mission –––
T_HOVER = 4 * 60  # [s] 4 min hover
T_LOITER = 0  # no loiter in this mission
E_SPEC = 168  # [Wh kg-1]
ETA_BATT = 0.95
F_USABLE = 6000  # [mAh] (nominal)
ETA_ELECTRIC = 0.95
L_D_MAX = 12
CL_CRUISE = 0.846  # chosen aero point
CD_CRUISE = 0.04
H_END, H_START = 100, 0  # [m]

# ––– Fixed masses / fractions –––
M_PAYLOAD = 5.0  # [kg]
MF_STRUCT = 0.35
MF_AVIONICS = 0.05
MF_SUBSYSTEMS = 0.07

# Convenience: build one Constraints object for reuse
_CONSTRAINTS = Constraints(
    V_STALL, V_CRUISE, e, AR, CL_MAX, CD0, N_PROP_EFFIC, R_C_service=0.5
)


# ------------------------------------------------------------------------- #
# 2. Integrated sizing routine (one run = one design point)                 #
# ------------------------------------------------------------------------- #
def _sizing_loop(
    W_S: float, P_W: float, tol: float = 1e-3, max_iter: int = 15
) -> float:
    """
    Returns MTOM [kg] for the candidate wing-loading W_S [N m-2]
    and power-loading P_W [W N-1] using the fixed-point loop of Tyan et al.
    """
    MTOM_kg = 30.0  # initial guess
    g = 9.81

    for _ in range(max_iter):
        W_TO = MTOM_kg * g  # [N]
        S_wing = W_TO / W_S  # [m²]

        # -- VTOL sizing --------------------------------------------------- #
        vtol = VTOLProp(W_S, STOT_S_W, W_TO, N_PROPS_VTOL)
        P_VTOL, S_prop, DL, Thrust = vtol.power_required_vtol()
        D_prop = 2 * np.sqrt(S_prop / np.pi)

        # -- Propulsion masses -------------------------------------------- #
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
        M_FW, M_VTOL = prop.calculate_propulsion_mass()  # [kg]

        # -- Battery sizing (mass fraction) ------------------------------- #
        batt = BattMass(
            T_HOVER,
            T_LOITER,
            MTOM_kg,
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
        )
        MF_batt, _ = batt.Batt_Mass_Total()

        # -- Fixed-point update ------------------------------------------- #
        denom = 1.0 - (MF_batt + MF_STRUCT + MF_SUBSYSTEMS + MF_AVIONICS)
        MTOM_new = (M_VTOL + M_FW + M_PAYLOAD) / denom

        if abs(MTOM_new - MTOM_kg) < tol:
            return MTOM_new
        MTOM_kg = MTOM_new

    return MTOM_kg  # if not converged


# ------------------------------------------------------------------------- #
# 3. Objective and constraint wrappers for SciPy                            #
# ------------------------------------------------------------------------- #
def _objective(x):
    """Scalar objective: total mass [kg] to be minimised."""
    W_S, P_W = x
    return _sizing_loop(W_S, P_W)


def _stall_ineq(x):
    """g(x) ≥ 0  ⇒  W/S does NOT exceed stall limit."""
    return _CONSTRAINTS.WingLoading_Vstall() - x[0]


def _cruise_ineq(x):
    W_S, P_W = x
    req_pw = powerLoading(_CONSTRAINTS.thrustLoadingCruise(W_S), V_CRUISE, N_PROP_EFFIC)
    return P_W - req_pw


def _climb_ineq(x):
    W_S, P_W = x
    V_roc = _CONSTRAINTS.Vroc(W_S)
    req_pw = powerLoading(
        _CONSTRAINTS.thrustLoadingClimb(V_roc, W_S, R_C, _CONSTRAINTS.q_climb(V_roc)),
        V_roc,
        N_PROP_EFFIC,
    )
    return P_W - req_pw


# ------------------------------------------------------------------------- #
# 4. SciPy SLSQP call                                                       #
# ------------------------------------------------------------------------- #
if __name__ == "__main__":
    # Bounds taken from the paper’s discussion (sec. 2.2.2).
    bounds = Bounds([20.0, 2.0], [200.0, 25.0])  # lower  # upper

    constraints = [
        {"type": "ineq", "fun": f} for f in (_stall_ineq, _cruise_ineq, _climb_ineq)
    ]

    # Sensible starting point: half of stall-limited W/S, mid-range P/W
    x0 = np.array([0.5 * _CONSTRAINTS.WingLoading_Vstall(), 9.0])

    result = minimize(
        _objective,
        x0,
        method="SLSQP",
        bounds=bounds,
        constraints=constraints,
        options={"ftol": 1e-3, "maxiter": 50, "disp": True},
    )

    if result.success:
        W_S_opt, P_W_opt = result.x
        MTOM_opt = result.fun
        print(f"\nOptimal wing-loading  W/S  : {W_S_opt:6.2f} N m⁻²")
        print(f"Optimal power-loading P/W  : {P_W_opt:6.2f} W N⁻¹")
        print(f"Minimum take-off mass MTOM : {MTOM_opt:6.2f} kg")
    else:
        raise RuntimeError(f"SLSQP failed → {result.message}")
