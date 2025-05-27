'''
This is the funny_inputs file, you are allowed and supposed to change this while coding. 
If your code is unfinished, please use these
'''

funny_inputs = {}

# ~~~ Constants ~~~ 

constants_funny_inputs = {
    'g': 9.81           # Gravitational constant [m/s2]
}

funny_inputs.update(constants_funny_inputs)

# ~~~ Aerodynamics ~~~

aerodynamics_funny_inputs = {}

funny_inputs.update(aerodynamics_funny_inputs)

# ~~~ Deployment ~~~~

deployment_funny_inputs = {
    'payload_mass' : 5., # kg
    'aerogel_width' : 1.5, # m
    'aerogel_thickness' : 0.003, # m
    'aerogel_density' : 200., # kg/m3

    'n_ferro_magnets' : 2, # nr
    'ferro_magnet_mass' : 0.5, # kg, guesstimate
    'deployment_added_mass' : 1., # kg, guesstimate

    'wire_length' : 15., # m
    'wire_density' : 0.01488, # kg/m
    'n_wire' : 2, # nr

    'spring_mass' : 0., # kg
    'winch_mass' : 1.5, #kg
    'n_pulleys' : 4, # nr
    'pulley_mass' : 0.2, # kg, guesstimate
    'n_epms' : 4, # nr
    'epm_diameter'  : 0.0025, # m
    'epm_mass' : 0.039, # kg

    'deployment_system_volume' : 0.0026554, # m3, guesstimate only incl. winch volume
    'deployment_speed' : 0.3, # m/s
    'deployment_time_margin' : 30., # s, guesstimate for aerogel unrolling, final positioning, and dropping

    'power_required_epm' : 20., # W
    'epm_duration' : 8., # s, maximum OFF-mode duration
    'power_required_winch' : 96., # W

    'deployment_accuracy' : 0.5, # m, guesstimate

    'fuselage_size' : 1.5, # m, guesstimate
}

funny_inputs.update(deployment_funny_inputs)

# ~~~ Operations ~~~

operations_funny_inputs = {}

funny_inputs.update(operations_funny_inputs)

# ~~~ Propulsion and Power ~~~ 

prop_n_pow_funny_inputs = {}

funny_inputs.update(prop_n_pow_funny_inputs)

# ~~~ Stability and control ~~~ 

stab_n_con_funny_inputs = {}

funny_inputs.update(stab_n_con_funny_inputs)

# ~~~ Structures ~~~ 

structures_funny_inputs = {}

funny_inputs.update(structures_funny_inputs)

# ~~~ Thermal control ~~~

thermal_funny_inputs = {}

funny_inputs.update()