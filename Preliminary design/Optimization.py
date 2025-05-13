import numpy as np

from Contraints_for_mass_calculations import powerLoading, Constraints
from electric_propulsion_mass_sizing import calculate_esc_mass, calculate_motor_mass, calculate_propeller_mass
from vtol_propulsion_sizing import thrust_to_weight_vtol, power_required_vtol

# ESTIMATIONS
e = 0.7 #7 oswald efficiency factor  
AR = 10.03 # Aspect ratio of wing        
r_c = 3 # [m/s] rate of climb        
Vstall = 13.8 # stall speed [m/s]      
CLmax = 1.34  # 1.34                     
max_volt = 12 # max voltage

k =  1/ (np.pi * e * AR)

stot_s_w = 1.35 #         

n_props = 4

# Constants 
rho = 0.9013  # density at 3000m 
V_cruise = 100 / 3.6  # [m/s] cruise velocity 100km/hr
q = 0.5 * rho * V_cruise **2 # dynamic pressure 
CD0 = 0.040 + 0.2 # parasite drag + drag from rounded cylinder 
n_p = 0.85 
R_C_service = 0.5 #[m/s]
MTOW = 30*9.81

# motor constants
F1 = 0.889
E1 = -0.288
E2 = 0.1588

initial_mass_est = Constraints(e, AR, r_c, Vstall, CLmax)
initial_mass_est.plot()

w_s = float(input('please input W/s:'))
w_p = float(input('please input P/W:'))

t_w_VTOL = thrust_to_weight_vtol(rho, w_s, r_c, stot_s_w)

s = MTOW / w_s
p = MTOW / w_p
t_VTOL = t_w_VTOL * MTOW

p_req_VTOL, S_prop = power_required_vtol(t_VTOL, MTOW/9.81, 0.7, rho, r_c)

mot_mass_cruise = calculate_motor_mass(p, max_volt, F1, E1, E2)
mot_mass_VTOL = calculate_motor_mass(p_req_VTOL, max_volt, F1, E1, E2)

esc_mass = calculate_esc_mass(p)

prop_mass_cruise = calculate_propeller_mass(0.6, 15, 1, 4, S_prop, p)

print(mot_mass_cruise/9.81, esc_mass, prop_mass_cruise, mot_mass_VTOL/9.81)