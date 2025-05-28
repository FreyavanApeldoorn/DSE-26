'''
This is the inputs file, these should not be changed without communicating with the entire group. 
Only do this when your code is finished and verified, while working, use funny_inputs
'''
inputs = {}

# ~~~ Constants ~~~ 

constants_inputs = {
    'g': 9.81           # Gravitational constant [m/s2]
}
inputs.update(constants_inputs)


# ~~~ Requirements ~~~
requirements_inputs = {
    'M_to': 30,  # Maximum Takeoff Mass [kg]
    'R_max': 20 000,    # Maximum Range [m]

}    
inputs.update(requirements_inputs)


# ~~~ Mission ~~~

mission_inputs = {
    'perimeter': 1000,  # Mission perimeter [m]
    'V_cruise': 100 / 3.6,  # Cruise speed [m/s] (converted from 100 km/h)
    'h_cruise': 120,  # Mission altitude [m]
    'Rate_of_Climb': 6  # Rate of climb [m/s]

}

inputs.update(mission_inputs)

# ~~~ Deployment ~~~~

deployment_inputs = {
    'n_ferro_magnets' : 2, # nr
    'ferro_magnet_mass' : 0.5, # kg, guesstimate
    'deployment_added_mass' : 1., # kg, guesstimate

    'wire_length' : 15., # m, neglecting the split ends of the wire
    'wire_density' : 0.0149, # kg/m
    'n_wire' : 2, # nr

    'spring_mass' : 0., # kg
    'winch_mass' : 1.5, #kg
    'n_pulleys' : 4, # nr
    'pulley_mass' : 0.2, # kg, component needs to be picked
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
    'firebreak_width': 3, # m

    'fuselage_size' : 1.5, # m, guesstimate
}
inputs.update(deployment_inputs)


# ~~~ Propulsion ~~~ 

propulsion_inputs = {

}
inputs.update(propulsion_inputs)



# ~~~ Power ~~~ 

power_inputs = {

}
inputs.update(power_inputs)

# ~~~ Stability and control ~~~ 

stab_n_con_inputs = {

}
inputs.update(stab_n_con_inputs)

# ~~~ Aerodynamics ~~~

aerodynamics_inputs = {

}
inputs.update(aerodynamics_inputs)

# ~~~ Structures ~~~ 

structures_inputs = {

}
inputs.update(structures_inputs)

# ~~~ Thermal control ~~~

thermal_inputs = {

}
inputs.update()