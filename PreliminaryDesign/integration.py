from mission_profile import MissionProfile
from mass_estimation import mass_sizing
import numpy as np



inputs = {
    #"rho_min": 0.9013,              # kg/m^3, density of air at service ceiling
    #"MTOW": 30 * 9.81,          # N, maximum take-off weight 
    #"V_cruise": 100 / 3.6,      # m/s, cruise speed
    #"V_stall": 13.8,             # m/s, stall speed
    #"CD0": 0.040,               # drag coefficient at zero lift
    #"n_p": 0.85,                # propeller efficiency
    #"R_C_service": 0.5,         # service ceiling ratio
    #"CL_max": 1.34,             # maximum lift coefficient
    #"e": 0.7,                   # Oswald's efficiency factor
    #"AR": 10.3,                 # aspect ratio
    #"stot_s_w": 1.35,           # wing loading ratio
    #"eta_prop": 0.83,           # propeller efficiency
    #"U_max": 25.5,              # maximum voltage
    # "F1": 0.889,                # motor constant (kg/W^E1 * V^E2)
    # "E1": -0.288,               # exponent for power
    # "E2": 0.1588,               # exponent for voltage
    # "f_install_cruise": 1,      # cruise propulsion installation factor
    # "f_install_vtol": 1,        # VTOL propulsion installation factor
    #"n_mot_cruise": 1,          # number of cruise motors
    #"n_mot_vtol": 4,            # number of VTOL motors
    #"K_material": 0.6,          # material constant (kg/m^3)
    #"n_propellers_cruise": 1,        # number of cruise propellers
    #"n_propellers_vtol": 4,          # number of VTOL propellers
    #"n_blades_cruise": 4,       # number of blades per cruise propeller
    #"n_blades_vtol": 4,         # number of blades per VTOL propeller
    #"K_p": 0.0938,              # propeller constant (kg/W^E1 * V^E2)
    # "t_hover": 4 * 60,          # hover time in seconds
    # "t_loiter": 0,              # loiter time in seconds
    #"E_spec": 168,              # specific energy of the battery (Wh/kg)
    #"Eta_bat": 0.95,            # battery efficiency
    # "f_usable": 6000,           # usable battery capacity (Wh)
    # "Eta_electric": 0.95,       # electric system efficiency
    # "LD_max": 12,               # maximum lift-to-drag ratio
    #"CL_cruise": 0.846,                # lift coefficient
    #"CD_cruise": 0.04,                 # drag coefficient
    #"T": 30 * 9.81,             # thrust in N
    #"h_end": 100,               # end altitude in m
    #"h_start": 0,               # start altitude in m
    # "MF_struct": 0.35,          # mass fraction for structure
    # "MF_avion": 0.05,           # mass fraction for avionics
    # "MF_Subsyst": 0.07,         # mass fraction for subsystems
    #"M_payload": 5,             # payload mass in kg
}


# ================================


constants = {
    "g": 9.81,                  # gravitational acceleration in m/s^2
}

mission_definition = []   # Define the mission profile here

# Mission profile parameters: 
mission_parameters = {
    "h_ground": 0,     # ground altitude in m
    "h_cruise": 120,    # cruise altitude in m
    "rho_min": 0.9013, 
    "rho_max": 1.225, 
    "RC_service": 0.5,
    "h_service": 3000,
    "R_max": 30000, 
    "V_climb_v": 6, 
    "V_cruise": 120/3.6, 
    "V_descent": 3
    }   
inputs.update(mission_parameters)

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
    "CD_cruise": 0.05, 
    "CD0": 0.040, 
    "V_stall": 13.8, 
    "S_wing": 2.5, 
    "AR": 10.3, 
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
    "M_to": 30, 
    "M_payload": 5, 
    "M_battery": 10, 
    "M_FW": 5, 
    "M_VTOL": 5,
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



# Iteration loop 
# ==========================================

tolerance = 0.001
max_iterations = 100

def intergation_optimization(tolerance, max_iterations, inputs):
    for _ in range(max_iterations):
        print('Successful loop')
        mission = MissionProfile(inputs)
        outputs = mission.mission_profile().copy()
        outputs = mass_sizing(outputs)

        if all(abs(outputs[key] - inputs[key]) < tolerance for key in outputs if isinstance(outputs[key], float) or isinstance(outputs[key], np.float64)):
            print('Converged')
            return outputs
        
        
        inputs = outputs
    print('result did not stabilize at max iteration')
    return outputs


intergation_optimization(tolerance, max_iterations, inputs)
