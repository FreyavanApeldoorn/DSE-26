'''
This is the test_inputs file, you are allowed and supposed to change this while coding. 
If your code is unfinished, please use these
'''

test_inputs = {}

# ~~~ Constants ~~~ 

constants_test_inputs = {
    'g': 9.81,           # Gravitational constant [m/s2]
    'rho': 0.9093,       # Density at 3000m [kg/m^3]
    'mtow': 30*9.81      # maximum takeoff weight [kg]
}

test_inputs.update(constants_test_inputs)

# ~~~ Aerodynamics ~~~

aerodynamics_test_inputs = {}

test_inputs.update(aerodynamics_test_inputs)

# ~~~ Deployment ~~~~

deployment_test_inputs = {
    'payload_mass' : 5., # kg
    'aerogel_width' : 1.5, # m
    'aerogel_thickness' : 0.005, # m
    'aerogel_density' : 100., # kg/m3

    'n_ferro_magnets' : 2, # nr
    'ferro_magnet_mass' : 0.5, # kg, guesstimate
    'deployment_added_mass' : 1., # kg, guesstimate

    'wire_length' : 15., # m, neglecting the split ends of the wire
    'wire_density' : 0.01, # kg/m
    'n_wire' : 2, # nr

    'spring_mass' : 0., # kg
    'winch_mass' : 1., #kg
    'n_pulleys' : 4, # nr
    'pulley_mass' : 0.2, # kg, guesstimate
    'n_epms' : 4, # nr
    'epm_diameter'  : 0.003, # m
    'epm_mass' : 0.04, # kg

    'deployment_system_volume' : 0.003, # m3, guesstimate only incl. winch volume
    'deployment_speed' : 0.3, # m/s
    'deployment_time_margin' : 30., # s, guesstimate for aerogel unrolling, final positioning, and dropping

    'power_required_epm' : 20., # W
    'epm_duration' : 8., # s, maximum OFF-mode duration
    'power_required_winch' : 100., # W

    'deployment_accuracy' : 0.5, # m, guesstimate
    'firebreak_width': 3, # m

    'fuselage_size' : 1., # m, guesstimate
}

test_inputs.update(deployment_test_inputs)

# ~~~ Constraints ~~~

Constraints_test_inputs = {
    'V_stall' : 19,    #m/s
    'V_max' : 100/3.6,    #m/s
    'e' : 0.7,          #-
    'AR' : 7,           #-
    'CL_max': 1.34,      #- 
    'CD_0' : 0.040,      #- 
    'eff_prop' : 0.83,   #- 
    'R_C_service': 0.5, #m/s 

}

test_inputs.update(Constraints_test_inputs)

# ~~~ Operations ~~~

operations_test_inputs = {}

test_inputs.update(operations_test_inputs)

# ~~~ Propulsion and Power ~~~ 

prop_n_pow_test_inputs = {
    'wing_loading' : 217, # N
    's_tot_sw' : 0.003, # m
    'n_prop_vtol' : 4 , # number of propellers in VTOL mode
    'vtol_roc' : 6, # m/s
    'eff_prop' : 0.83, #-
    'K_p' : 0.0938, # propeller constant (kg/W^E1 * V^E2)
    'n_props_cruise' : 1, # number of propellers in cruise
    'motor_mass_cruise' : (940+495+10)*0.001, 
    'motor_mass_VTOL' : 0.655+0.170, #kg
    'propeller_mass_VTOL' : 0.073, #kg
    'propeller_mass_cruise' : 0.0100 , #kg
    'power_available_VTOL' : 1418 , #W
    'power_available_cruise' : 2552 , #W
    
}

test_inputs.update(prop_n_pow_test_inputs)

# ~~~ Stability and control ~~~ 

stab_n_con_test_inputs = {}

test_inputs.update(stab_n_con_test_inputs)

# ~~~ Structures ~~~ 

structures_test_inputs = {}

test_inputs.update(structures_test_inputs)

# ~~~ Thermal control ~~~

thermal_test_inputs = {}

test_inputs.update()