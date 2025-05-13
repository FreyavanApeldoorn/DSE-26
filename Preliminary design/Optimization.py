import numpy as np

from Contraints_for_mass_calculations import powerLoading, Constraints
from electric_propulsion_mass_sizing import calculate_esc_mass, calculate_motor_mass, calculate_propeller_mass
from vtol_propulsion_sizing import VTOLProp

# ~~~ Inputs Contraints ~~~  
V_cruise = 100 / 3.6  # [m/s] cruise velocity 100km/hr    
Vstall = 13.8 # stall speed [m/s]   

# ~~~ Inputs VTOLProp ~~~

# ~~~ Inputs PropMass ~~~
max_volt = 12 # max voltage
stot_s_w = 1.35 #         
rho = 0.9013  # density at 3000m 
r_c = 3
eta_prop = 0.85

F1 = 0.889
E1 = -0.288
E2 = 0.1588

# ~~~ Inputs BattMass ~~~

# ~~~ Inputs TotMass ~~~
MTOW = 30*9.81

# ~~~ First iteration ~~~

constraint_plot = Constraints(Vstall, V_cruise)
constraint_plot.plot()

w_s = float(input('please input W/s:'))
w_p = float(input('please input P/W:'))

s = MTOW / w_s
p = MTOW / w_p

VTOL_prop_mod = VTOLProp(w_s, stot_s_w, MTOW, eta_prop)

p_req_VTOL, S_prop = VTOL_prop_mod.power_required_vtol()

mot_mass_cruise = calculate_motor_mass(p, max_volt, F1, E1, E2)
mot_mass_VTOL = calculate_motor_mass(p_req_VTOL, max_volt, F1, E1, E2)

esc_mass = calculate_esc_mass(p)

prop_mass_cruise = calculate_propeller_mass(0.6, 15, 1, 4, S_prop, p)

print(mot_mass_cruise/9.81, esc_mass, prop_mass_cruise, mot_mass_VTOL/9.81)

