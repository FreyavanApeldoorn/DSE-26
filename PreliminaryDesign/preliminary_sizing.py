from mission_profile import UAVProfile, SwarmProfile
from Nest_Sizing import Nest
from mass_estimation import mass_sizing
from Classes.Contraints_for_mass_calculations import Constraints
from Battery_mass_estimation_v2 import calculate_battery_mass
import numpy as np

# =============================================
# ========== Global ===========================


verbose = True




# =============================================
# ========== Inputs ===========================

inputs = {}


constants = {
    "g": 9.81,                  # gravitational acceleration in m/s^2
}

mission_definition = []   # Define the mission profile here


mission_parameters = {
    "required_perimeter": 1000, # m, perimeter of the area to be covered
    "fire_break_width": 3,   # m, width of the fire break

    "aerogel_length": 5,  # m, length of the aerogel
    "aerogel_width": 1.5,   # m, width of the aerogel
    "aerogel_thickness": 0.1, # m, height of the aerogel

    "rho_min": 0.9013, 
    "rho_max": 1.225, 
}
inputs.update(mission_parameters)



# Swarm profile parameters:
swarm_parameters = {
    "n_drones": 20,
    "n_nests": 1,   # assumed to be 1 for initial sizing 


}
inputs.update(swarm_parameters)



# UAV profile parameters: 
uav_parameters = {
    "h_ground": 0,     # ground altitude in m
    "h_cruise": 120,    # cruise altitude in m
    "RC_service": 0.5,
    "h_service": 3000,
    "R_max": 30000, #30000
    "V_climb_v": 6, 
    "V_cruise": 120/3.6, 
    "V_descent": 3,
    "total_mission_time": 60*60, # total mission time in seconds
    "total_mission_energy": 4000, # total mission energy in Wh

    "deployment_accuracy": 0.1 # m accuracy of the deployment
    }   
inputs.update(uav_parameters)

# Mission time estimates
time_estimates = {
    "t_load": 1*60, 
    "t_transition": 30, 
    "t_scan": 60, 
    "t_deploy": 5*60, 
    "t_recharge": 5*60,
    "t_hover": 4 * 60,          # hover time in seconds
    "t_loiter": 0,              # loiter time in seconds
    }
inputs.update(time_estimates)

# Power parameters: 
power_parameters = {
    "P_load": 100, 
    "P_r_VTOL": 3500, 
    "P_r_FW": 1100, 
    "P_a_transition": 4600, 
    "P_r": 3500, 
    "P_deploy": 4000,

    "E_spec": 168,              # specific energy of the battery (Wh/kg)
    "Eta_bat": 0.95,            # battery efficiency
    "f_usable": 6000,           # usable battery capacity (Wh)
    "Eta_electric": 0.95,       # electric system efficiency
    "U_max": 25.5              # maximum voltage
    
    }
inputs.update(power_parameters)


# Fixed-wing parameters:
fw_parameters = {
    "CL_cruise": 0.846, 
    "CL_max": 1.34, 
    "LD_max": 12,               # maximum lift-to-drag ratio
    "t_w": 0,                   # Thrust-to-weight ratio (initialized to 0)
    "CD_cruise": 0.05, 
    "CD0": 0.040, 
    "V_stall": 19,             # m/s, stall speed
    "S_wing": 2.5, 
    "AR": 7, #10.3
    "b_wing": 0,                # span (initialized to 0)
    "e": 0.7,
    "n_propellers_cruise": 1,        # number of cruise propellers
    "n_blades_cruise": 4,       # number of blades per cruise propeller
    "propeller_efficiency_cruise": 0.8,
    "n_mot_cruise": 1          # number of cruise motors
    }
inputs.update(fw_parameters)


# VTOL parameters:
vtol_parameters = {
    "T_VTOL": 30 * 9.81,             # thrust in N
    "number_propellers": 4, 
    "number_motors": 4, 
    "propeller_diameter": 0.5, 
    "propeller_pitch": 0.2, 
    "n_propellers_vtol": 4,          # number of VTOL propellers
    "n_blades_vtol": 4,         # number of blades per VTOL propeller
    "propeller_efficiency_vtol": 0.8,   # VTOL propeller efficiency
    "n_mot_vtol": 4            # number of VTOL motors
    }
inputs.update(vtol_parameters)


# Mass parameters:
mass_parameters = {
    "MTOW": 30 * 9.81,
    "M_to": 30,             # take off mass in kg
    "M_payload": 5, 
    "M_battery": 0,        # initiialise to 0, will be calculated later
    #"M_FW": 5, 
    #"M_VTOL": 5,
    "MF_struct": 0.35,          # mass fraction for structure
    "MF_avion": 0.05,           # mass fraction for avionics
    "MF_Subsyst": 0.07         # mass fraction for subsystems
    }
inputs.update(mass_parameters)


# Structural parameters:
structural_parameters = {
    "K_material": 0.6,          # material constant (kg/m^3)
}
inputs.update(structural_parameters)


mass_estimation_parameters = {
    "stot_s_w": 1.35,       # wing loading ratio
    "F1": 0.889,                # motor constant (kg/W^E1 * V^E2)
    "E1": -0.288,               # exponent for power
    "E2": 0.1588,               # exponent for voltage
    "K_p": 0.0938,              # propeller constant (kg/W^E1 * V^E2)
    "f_install_cruise": 1,      # cruise propulsion installation factor
    "f_install_vtol": 1,        # VTOL propulsion installation factor
    }
inputs.update(mass_estimation_parameters)


battery_parameters = {
    "DOD_fraction": 0.8,         # Fraction of battery capacity that can be used (Depth of Discharge)
    "eta_battery": 0.95,         # Battery discharge efficiency
    }
inputs.update(battery_parameters)



if verbose:
    print("Initial Inputs:")
    for key, value in inputs.items():
        print(f"{key}: {value}")
    print("\n")


# =============================================
# ========== Sizing ============================

for i in range(100):

    print(f"Iteration {i+1}:")

    input = inputs.copy()

    swarm_profile = SwarmProfile(input)
    outputs = swarm_profile.size_swarm_profile()

    uav_profile = UAVProfile(outputs)
    outputs = uav_profile.size_uav_profile()

    battery_mass = calculate_battery_mass(
            E_required_Wh=inputs['total_mission_energy'],
            DOD_fraction=inputs['DOD_fraction'],
            eta_battery=inputs['eta_battery'],
            M_to=inputs['M_to'] 
        )
    outputs['M_battery'] = battery_mass

    outputs = mass_sizing(outputs)

    if i == 8:
        print("Intermediate:")
        for key, value in inputs.items():
            print(f"{key}: {value}")
        print("\n")


    nest = Nest(outputs)
    outputs = nest.size_nest()

    inputs.update(outputs)

print("Outputs:")
for key, value in outputs.items():
    print(f"{key}: {value}")




