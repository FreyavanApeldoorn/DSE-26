import numpy as np

from Contraints_for_mass_calculations import powerLoading, Constraints
from electric_propulsion_mass_sizing import PropMass
from vtol_propulsion_sizing import VTOLProp
from Battery_Mass_Calculations import BattMass

# ~~~ Overall variables ~~~
rho = 0.9013  # density at 3000m
MTOW = 30 * 9.81

# ~~~ Inputs Contraints ~~~
V_cruise = 100 / 3.6  # [m/s] cruise velocity 100km/hr
Vstall = 13.8  # stall speed [m/s]

CD0 = 0.040  # + 0.2 # parasite drag + drag from rounded cylinder
n_p = 0.85  # Propeller Efficiency
R_C_service = 0.5  # [m/s]
CLmax = 1.34  #                         ESTIMATION
e = 0.7  # 7 oswald efficiency factor  ESTIMATION
AR = 10.03  # Aspect ratio of wing        ESTIMATION

# ~~~ Inputs VTOLProp ~~~
stot_s_w = 1.35  #
eta_prop = 0.85

# ~~~Inputs Electric Prop mass ~~~
U_max = 25.5
F1 = 0.889
E1 = -0.288
E2 = 0.1588
f_install_cruise = 1  # fix later
f_install_vtol = 1  # fix later
n_mot_cruise = 1
n_mot_vtol = 4
K_material = 0.6
n_props_cruise = 1
n_props_vtol = 4
n_blades_cruise = 4
n_blades_vtol = 4
K_p = 0.0938

# ~~~ Inputs BattMass ~~~
# https://maxamps.com/products/lipo-6000-6s-22-2v-battery-pack
t_hover = 4 * 60  # s
t_loiter = 0
E_spec = 168  # Specific energy capacity [Wh/kg]
Eta_bat = 0.95  # ??115
f_usable = 6  # Usable Battery Capacity [Ah]
Eta_electric = 0.95  # Efficiency of electric system
LD_max = 12  # max lift to drag ratio
CL = 1  # lift coefficient
CD = 0.04  # drag coefficient
T = 30 * 9.81  # total thrust (weight) [N]
h_end = 100  # Hieght drone climbs to [m]
h_start = 0  # hieght drone starts at [m]


# ~~~ Inputs TotMass ~~~
M_Payload = 5
M_struct = 0.35
M_avion = 0.05
M_Subsyst = 0.07
M_payload = 5

# ~~~ First iteration ~~~
constraint_plot = Constraints(Vstall, V_cruise, e, AR, CLmax, CD0, n_p, R_C_service)
constraint_plot.plot()

w_s = float(input("please input W/S: "))
p_w = float(input("please input P/W: "))

s = MTOW / w_s
P_max_cruise = MTOW * p_w

VTOL_prop_mod = VTOLProp(w_s, stot_s_w, MTOW, n_props_vtol)

p_req_VTOL, S_prop, DL, T = VTOL_prop_mod.power_required_vtol()

# Print powers
print("Power required for VTOL: ", p_req_VTOL)
print("Power required for cruise: ", P_max_cruise)
D_prop_VTOL = 2 * (S_prop / np.pi) ** 0.5

prop_mass = PropMass(
    P_max_cruise,
    p_req_VTOL,
    U_max,
    F1,
    E1,
    E2,
    f_install_cruise,
    f_install_vtol,
    n_mot_cruise,
    n_mot_vtol,
    K_material,
    n_props_cruise,
    n_props_vtol,
    n_blades_cruise,
    n_blades_vtol,
    D_prop_VTOL,
    K_p,
)

motor_mass_cruise, _, motor_mass_VTOL, _ = prop_mass.calculate_motor_mass()
esc_mass_cruise, _, esc_mass_VTOL, _ = prop_mass.calculate_esc_mass()
propeller_mass_cruise, _, propeller_mass_VTOL, _ = prop_mass.calculate_propeller_mass()
M_FW_Prop, M_Vtol_Prop = prop_mass.calculate_propulsion_mass()


batt_mass = BattMass(
    t_hover,
    t_loiter,
    MTOW / 9.81,
    E_spec,
    Eta_bat,
    f_usable,
    Eta_electric,
    T,
    DL,
    LD_max,
    CL,
    CD,
    w_s,
    h_start,
    h_end,
    p_req_VTOL,
)

M_Batt, battery_mass_endurance = batt_mass.Batt_Mass_Total()

# TOTAL MASS CALCULATIONS
print(M_struct, M_avion, M_Subsyst, M_Batt, M_Vtol_Prop, M_FW_Prop, M_payload)

M_TO = (M_Vtol_Prop + M_FW_Prop + M_payload) / (
    1 - (M_Batt + M_struct + M_Subsyst + M_avion)
)
