'''
This is the inputs file, these should not be changed without communicating with the entire group. 
Only do this when your code is finished and verified, while working, use funny_inputs
'''
inputs = {}

# ~~~ Constants ~~~ 

constants_inputs = {
    'g': 9.81,          # Gravitational constant [m/s2]
    'rho_0': 1.225  # Air density at sea level [kg/m^3]
}
inputs.update(constants_inputs)


# ~~~ Requirements ~~~
requirements_inputs = {
    'M_to': 30,  # Maximum Takeoff Mass [kg]
    'MTOW': 30 * constants_inputs['g'],  # Maximum Takeoff Weight [N]
    'R_max': 20000    # Maximum Range [m]

}    
inputs.update(requirements_inputs)


# ~~~ Mission ~~~ stuff that is mission-level 

mission_inputs = {
    'mission_type': 'wildfire', 
    'mission_perimeter': 1000,  # Mission perimeter [m]
    'number_of_UAVs': 20,  # Number of UAVs in the swarm
    'number_of_containers': 3, # Number of containers in the nest
    'number_of_workers': 2  # Number of workers per UAV
}
inputs.update(mission_inputs)


# ~~~ UAV ~~~ uav performance and design parameters
uav_inputs = {
    'V_cruise': 100 / 3.6,  # Cruise speed [m/s] (converted from 100 km/h)
    'V_stall': 19,  # Stall speed [m/s] 
    'h_cruise': 120,  # Mission altitude [m]
    'ROC_VTOL': 6,  # Rate of climb for VTOL mode [m/s]
    'ROD_VTOL': 3,  # Rate of descent for VTOL mode [m/s]
    'ROC_cruise': 3,  # Rate of climb for cruise mode [m/s]'
    'h_service': 3000,  # Service ceiling [m]
    "ROC_service": 0.5,  # Service rate of climb (at max altitude) [m/s]
    "rho_service": 0.9093,  # Density at service ceiling [kg/m^3]

    "time_transition": 30,  # Time for transitioning from VTOL to cruise [s]
    "time_deploy": 5*60,  # Time for deploying the UAV [s]: From UAV design
    "time_scan": 60  # Time for scanning [s]: From UAV design
}
inputs.update(uav_inputs)

# ~~~ Deployment ~~~~ deployment system parameters

deployment_inputs = {
    "payload_mass": 5.0,  # kg initialized to minimum payload mass
    "aerogel_width": 1.5,  # m
    "aerogel_thickness": 0.003,  # m
    "aerogel_density": 200.0,  # kg/m3
    
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

    'fuselage_size' : 1.5 # m, guesstimate
}
inputs.update(deployment_inputs)


# ~~~ Propulsion ~~~ initial inputs for propulsion sizing

propulsion_inputs = {
    "wing_loading": 217,  # N
    "s_tot_sw": 0.003,  # m
    "n_prop_vtol": 4,  # number of propellers in VTOL mode
    "vtol_roc": 6,  # m/s
    "eff_prop": 0.83,  # -
    "K_p": 0.0938,  # propeller constant (kg/W^E1 * V^E2)
    "n_props_cruise": 1,  # number of propellers in cruise
    "motor_mass_cruise": (940 + 495 + 10) * 0.001,  # - selected from components 
    "motor_mass_VTOL": 0.655 + 0.170,  # kg  # - selected from components 
    "propeller_mass_VTOL": 0.073,  # kg  # - selected from components 
    "propeller_mass_cruise": 0.0100,  # kg   # - selected from components 
    "power_available_VTOL": 1418,  # W    # - selected from components 
    "power_available_cruise": 2552  # W   # - selected from components 
}
inputs.update(propulsion_inputs)


# ~~~ Power ~~~ initial inputs for power sizing

power_inputs = {
    "DOD_fraction": 0.8,  # Depth of discharge fraction
    "eta_battery": 0.9,  # Battery efficiency
}
inputs.update(power_inputs)

# ~~~ Stability and control ~~~ initial inputs for stability and control sizing

stab_n_con_inputs = {

}
inputs.update(stab_n_con_inputs)

# ~~~ Aerodynamics ~~~ initial inputs for aerodynamics sizing

aerodynamics_inputs = {
    "e": 0.7,  # Oswald efficiency factor
    "AR": 7,  # Aspect ratio
    "CL_max": 1.34,  # Maximum lift coefficient
    "CD_0": 0.040,  # Zero-lift drag coefficient
    "eff_prop": 0.83  # Propeller efficiency
}
inputs.update(aerodynamics_inputs)

# ~~~ Structures ~~~ initial inputs for structures sizing

structures_inputs = {

}
inputs.update(structures_inputs)


# ~~~ Thermal control ~~~ initial inputs for thermal control sizing

thermal_inputs = {
}
inputs.update(thermal_inputs)



nest_inputs = {
    "time_wing_attachment": 10.0,
    "time_aerogel_loading": 20.0,
    "time_startup_UAV": 20.0,
    "time_between_containers": 30.0,
    "time_UAV_wrapup_check": 30.0,
    "time_UAV_turnaround_check": 30.0,
    "time_put_back_UAV": 10.0,
    "time_final_wrapup": 300.0,
    "time_between_UAV": 10.0,
    "time_startup_nest": 120.0,
    "time_battery_swapping": 10.0, 
    "margin": 5.0
}
inputs.update(nest_inputs)


# ===========================================

initial_inputs = inputs.copy()

if __name__ == '__main__':
    for key, value in inputs.items():
        print(f"{key}: {value}")