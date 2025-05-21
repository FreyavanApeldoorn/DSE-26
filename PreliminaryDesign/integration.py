from mission_profile import UAVProfile, SwarmProfile
from Nest_Sizing import Nest
from mass_estimation import mass_sizing
from Classes.Contraints_for_mass_calculations import Constraints
from Battery_mass_estimation_v2 import calculate_battery_mass
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
    "R_max": 20000, #30000
    "V_climb_v": 6, 
    "V_cruise": 100/3.6, 
    "V_descent": 3,
    "required_perimeter": 1000, # m
    "deployment_accuracy": 0.5, # m (uncertainty of the deployment)
    "fire_break_width": 3, # m
    "n_drones": 20,
    "n_nests": 1,
    "aerogel_length": 3.32,
    "aerogel_width": 1.5,
    "aerogel_diameter": 0.2,
    "aerogel_thickness": 0.006,
    "total_mission_time": 60*60, # total mission time in seconds
    "total_mission_energy": 4000 # total mission energy in Wh
    }   
inputs.update(mission_parameters)

nest_parameters = {
    "FW_height": 0.3,
    "FW_width": 2.25,

    "generator_efficiency": 0.3,
    "diesel_energy_density": 9.94,
    "nest_energy": 1000,  # in Wh
    "nest_length": 5.9,
    "nest_width": 2.35,
    "nest_height": 2.39
}
inputs.update(nest_parameters)

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

V_range = np.arange(40, 70, 2)


# Iteration loop 
# ==========================================

tolerance = 1
max_iterations = 200
relevant = ['M_to', 'S_wing', 'b_wing', 'R_max', 'propeller_diameter', 'M_battery', 'swarm_deployment_rate', 'swarm_deployment_rate_mass', 'P_r_VTOL', 'P_r_FW']

doesnt_converge = set()
def integration_optimization(tolerance: float, max_iterations: int, inputs: dict[str, float | int]) -> tuple[dict[str, float | int], dict[str, list[float]]]:
    '''
    Combines the mass estimation, battery calculation and mission profile calculations and iterates until convergence or max iterations.

    Parameters:
    tolerance (float): The tolerance for convergence.   
    max_iterations (int): The maximum number of iterations to perform.
    inputs (dict): A dictionary containing the input parameters for the calculations.
    '''
    for i in range(max_iterations):
        
        current_inputs = inputs.copy()

        swarm_sizing = SwarmProfile(current_inputs)
        outputs = swarm_sizing.size_swarm_profile()

        uav_profile = UAVProfile(outputs)
        outputs = uav_profile.size_uav_profile()
        

        # Calculate the mass of the battery
        battery_mass = calculate_battery_mass(
            E_required_Wh=inputs['total_mission_energy'],
            DOD_fraction=inputs['DOD_fraction'],
            eta_battery=inputs['eta_battery'],
            M_to=inputs['M_to'] 
        )
    
        
       
        outputs['M_battery'] = battery_mass

        outputs = mass_sizing(outputs)

        print(f'span: {outputs["b_wing"]}, wing area: {outputs["S_wing"]}, battery mass: {battery_mass}, MTOW: {inputs["MTOW"]}, M_battery: {inputs["M_battery"]}')

        nest_sizing = Nest(outputs, verbose=False)
        outputs = nest_sizing.size_nest()
        
        if all(abs(outputs[key] - inputs[key]) < tolerance for key in outputs if isinstance(outputs[key], float) or isinstance(outputs[key], np.float64)):
            print('Converged')
            return outputs
        
        if i > max_iterations-3:       
            for key in outputs:
                if isinstance(outputs[key], float) or isinstance(outputs[key],  np.float64):
                    if abs(outputs[key] - inputs[key]) > tolerance:
                        doesnt_converge.add(key)

        inputs = outputs
    # print('result did not stabilize at max iteration')
    return outputs


if __name__ == '__main__':
    result = integration_optimization(1, 100, inputs)

    for i in result:
        if i in relevant:
            if i == 'swarm_deployment_rate':
                print(i, result[i]*60*60)
            else:
                print(i, result[i])

    
    # Constraints(
    #     inputs["V_stall"],
    #     inputs["V_cruise"],
    #     inputs["e"],
    #     inputs["AR"],
    #     inputs["CL_max"],
    #     inputs["CD0"],
    #     inputs["propeller_efficiency_cruise"],
    #     inputs["RC_service"]
    #     ).plot(save=True)





    """
    DEar Freya, plz plot
    - inputs["n_nests] vs inputs["n_drones"] vs inputs["swarm_deployment_rate"]
    
    """