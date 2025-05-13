import numpy as np

from Contraints_for_mass_calculations import powerLoading, Constraints
from electric_propulsion_mass_sizing import PropMass
from vtol_propulsion_sizing import VTOLProp

# ~~~ Inputs Contraints ~~~  
V_cruise = 100 / 3.6  # [m/s] cruise velocity 100km/hr    
Vstall = 13.8 # stall speed [m/s]   

# ~~~ Inputs VTOLProp ~~~

# ~~~ Inputs PropMass ~~~
stot_s_w = 1.35 #         
rho = 0.9013  # density at 3000m 
r_c = 3 #m/s
eta_prop = 0.85

# ~~~Inputs Electric Prop mass ~~~
U_max= 12
F1 = 0.889
E1 = -0.288
E2 = 0.1588
f_install_cruise = 1 # fix later
f_install_vtol = 1 # fix later
n_mot_cruise = 1
n_mot_vtol = 4
K_material = 0.6
n_props_cruise = 1
n_props_vtol = 4
n_blades_cruise = 4
n_blades_vtol = 4
K_p = 0.0938

# ~~~ Inputs BattMass ~~~
t_hover = 4*60 # s


# ~~~ Inputs TotMass ~~~
MTOW = 30*9.81

# ~~~ First iteration ~~~

constraint_plot = Constraints(Vstall, V_cruise)
constraint_plot.plot()

w_s = float(input('please input W/s:'))
w_p = float(input('please input P/W:'))

s = MTOW / w_s
P_max_cruise = MTOW / w_p

VTOL_prop_mod = VTOLProp(w_s, stot_s_w, MTOW, eta_prop)

p_req_VTOL, S_prop = VTOL_prop_mod.power_required_vtol()
D_prop_VTOL = 2*(S_prop/np.pi)**0.5

prop_mass = PropMass(
    P_max_cruise, p_req_VTOL, U_max, F1, E1, E2, 
    f_install_cruise, f_install_vtol, n_mot_cruise, 
    n_mot_vtol, K_material, n_props_cruise, n_props_vtol, 
    n_blades_cruise, n_blades_vtol, D_prop_VTOL, K_p
    )

motor_mass_cruise, _, motor_mass_VTOL, _ = prop_mass.calculate_motor_mass()
esc_mass_cruise, _, esc_mass_VTOL, _ = prop_mass.calculate_esc_mass()
propeller_mass_cruise, _, propeller_mass_VTOL, _ = prop_mass.calculate_propeller_mass()
propulsion_mass_cruise, propulsion_mass_VTOL = prop_mass.calculate_propulsion_mass()

print(motor_mass_cruise, motor_mass_VTOL, '\n', 
      esc_mass_cruise, esc_mass_VTOL, '\n', 
      propeller_mass_cruise, propeller_mass_VTOL, '\n', 
      propulsion_mass_cruise, propulsion_mass_VTOL)
