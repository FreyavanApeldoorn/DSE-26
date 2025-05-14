import numpy as np
import matplotlib.pyplot as plt

from PreliminaryDesign.Classes.Contraints_for_mass_calculations import Constraints, powerLoading
from PreliminaryDesign.Classes.vtol_propulsion_sizing import VTOLProp
from PreliminaryDesign.Classes.electric_propulsion_mass_sizing import PropMass
from PreliminaryDesign.Classes.Battery_Mass_Calculations import BattMass
from Optimization import _mass_loop  # your cached sizing loop

# ─── Constants ─────────────────────────────────────────────────────────
g = 9.81
rho = 0.9013
V_CRUISE = 100 / 3.6
V_STALL = 13.8
R_C = 3.0
CD0, e, AR = 0.04, 0.7, 10.03
CL_MAX = 1.34
N_PROP_EFF = 0.85
STOT_S_W = 1.35
N_PROPS_VTOL = 4
N_PROPS_CRUISE = 1
K_P = 0.0938
M_STALL = 2.2

# Build the “Constraints” helper
_cons = Constraints(V_STALL, V_CRUISE, e, AR, CL_MAX, CD0, N_PROP_EFF, R_C_service=0.5)


# ─── Constraint-functions ───────────────────────────────────────────────
def c_stall_margin(WS, PW):
    Vs_allow = V_CRUISE / M_STALL
    WS_allow = 0.5 * rho * Vs_allow**2 * CL_MAX
    return WS_allow - WS


def c_cruise(WS, PW):
    req = powerLoading(_cons.thrustLoadingCruise(WS), V_CRUISE, N_PROP_EFF)
    return PW - req


def c_climb(WS, PW):
    Vroc = _cons.Vroc(WS)
    req = powerLoading(
        _cons.thrustLoadingClimb(Vroc, WS, R_C, _cons.q_climb(Vroc)), Vroc, N_PROP_EFF
    )
    return PW - req


def c_wingspan(WS, PW):
    MTOM = _mass_loop(WS, PW)
    b = np.sqrt(AR * (MTOM * g / WS))
    return 3.0 - b


def c_cruise_prop(WS, PW):
    MTOM = _mass_loop(WS, PW)
    D_cr = K_P * ((MTOM * g) * PW / N_PROPS_CRUISE) ** 0.25
    return 0.5 - D_cr


def c_vtol_prop(WS, PW):
    MTOM = _mass_loop(WS, PW)
    vtol = VTOLProp(WS, STOT_S_W, MTOM * g, N_PROPS_VTOL)
    _, S_p, _, _ = vtol.power_required_vtol()
    D_vtol = 2 * np.sqrt(S_p / np.pi)
    return 0.5 - D_vtol


all_constraints = [
    c_stall_margin,
    c_cruise,
    c_climb,
    c_wingspan,
    c_cruise_prop,
    c_vtol_prop,
]

# ─── Build grid & mask feasibility ─────────────────────────────────────
WS_vals = np.linspace(20, 200, 60)
PW_vals = np.linspace(2, 25, 60)
WSg, PWg = np.meshgrid(WS_vals, PW_vals, indexing="xy")

feasible = np.ones_like(WSg, dtype=bool)
for fn in all_constraints:
    mask = np.vectorize(fn)(WSg, PWg) >= 0
    feasible &= mask

# ─── Plot ────────────────────────────────────────────────────────────────
plt.figure(figsize=(6, 5))
plt.contourf(
    WS_vals, PW_vals, feasible.astype(int), levels=[-0.5, 0.5, 1.5]
)  # two regions: 0=bad, 1=good
plt.xlabel("Wing loading $W/S$ (N/m²)")
plt.ylabel("Power loading $P/W$ (W/N)")
plt.title("Feasible Design Space under All Constraints")
plt.grid(linestyle="--", alpha=0.4)
plt.show()
