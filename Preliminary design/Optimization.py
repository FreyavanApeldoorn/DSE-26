import numpy as np

from Contraints_for_mass_calculations import powerLoading, Mass_Est
from electric_propulsion_mass_sizing import calculate_esc_mass, calculate_motor_mass, calculate_propeller_mass
from vtol_propulsion_sizing import thrust_to_weight_vtol, power_required_vtol

e = 0.7 #7 oswald efficiency factor  ESTIMATION 
AR = 10.03 # Aspect ratio of wing        ESTIMATION
r_c = 3 # [m/s] rate of climb        ESTIMATION
Vstall = 13.8 # stall speed [m/s]      ESTIMATION
CLmax = 1.34  # 1.34                        ESTIMATION
volt = 12

k =  1/ (np.pi * e * AR)

stot_s_w = 1.35 #                   ESTIMATION

n_props = 4

# Constants 
rho = 0.9013  # density at 3000m 
V_cruise = 100 / 3.6  # [m/s] cruise velocity 100km/hr
q = 0.5 * rho * V_cruise **2 # dynamic pressure 
CD0 = 0.040 + 0.2 # parasite drag + drag from rounded cylinder 
n_p = 0.85 
R_C_service = 0.5 #[m/s]
MTOW = 25*9.81

# motor constants
F1 = 7.765
E1 = -0.632
E2 = 0.596

initial_mass_est = Mass_Est(e, AR, r_c, Vstall, CLmax)

w_s = float(input('please input W/s:'))
p_w = float(input('please input P/W:'))

t_w = thrust_to_weight_vtol(rho, w_s, r_c, stot_s_w)

s = MTOW / w_s
p = p_w * MTOW
t = t_w * MTOW

p_req, S_prop = power_required_vtol(t, MTOW, 0.7, rho, r_c)

mot_mass = calculate_motor_mass(p, volt, F1, E1, E2)

esc_mass = calculate_esc_mass(p)

prop_mass_cruise = calculate_propeller_mass(0.6, 15, 1, 4, S_prop, p)

print(mot_mass, esc_mass, prop_mass_cruise)






