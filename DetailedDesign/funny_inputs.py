"""
This is the funny_inputs file, you are allowed and supposed to change this while coding.
If your code is unfinished, please use these
"""

import numpy as np

funny_inputs = {}

# ~~~ Constants ~~~

constants_funny_inputs = {
    "g": 9.81,  # Gravitational constant [m/s2]
    "rho": 0.9093,  # Density at 3000m [kg/m^3]
    "rho_0": 1.225,  # Density at sea level [kg/m^3]
    "rho_sea": 1.225,  # Density at sea level [kg/m^3]
    "mtow": 30 * 9.81,  # maximum takeoff weight [kg]
    "MTOW": 30 * 9.81,  # maximum takeoff weight [N]
}

funny_inputs.update(constants_funny_inputs)

# ~~~ Aerodynamics ~~~

aerodynamics_funny_inputs = {}

funny_inputs.update(aerodynamics_funny_inputs)

# ~~~ Deployment ~~~~

deployment_funny_inputs = {
    "payload_mass": 5.0,  # kg
    "aerogel_width": 1.5,  # m
    "aerogel_thickness": 0.003,  # m
    "aerogel_density": 200.0,  # kg/m3
    "n_ferro_magnets": 2,  # nr
    "ferro_magnet_mass": 0.5,  # kg, guesstimate
    "deployment_added_mass": 1.0,  # kg, guesstimate
    "wire_length": 15.0,  # m, neglecting the split ends of the wire
    "wire_density": 0.0149,  # kg/m
    "n_wire": 2,  # nr
    "spring_mass": 0.0,  # kg
    "winch_mass": 1.5,  # kg
    "n_pulleys": 4,  # nr
    "pulley_mass": 0.2,  # kg, guesstimate
    "n_epms": 4,  # nr
    "epm_diameter": 0.0025,  # m
    "epm_mass": 0.039,  # kg
    "deployment_system_volume": 0.0026554,  # m3, guesstimate only incl. winch volume
    "deployment_speed": 0.3,  # m/s
    "deployment_time_margin": 30.0,  # s, guesstimate for aerogel unrolling, final positioning, and dropping
    "power_required_epm": 20.0,  # W
    "epm_duration": 8.0,  # s, maximum OFF-mode duration
    "power_required_winch": 96.0,  # W
    "deployment_accuracy": 0.5,  # m, guesstimate
    "firebreak_width": 3,  # m
    "fuselage_size": 1.5,  # m, guesstimate
}

funny_inputs.update(deployment_funny_inputs)

# ~~~ Constraints ~~~

Constraints_funny_inputs = {
    "V_stall": 19,  # m/s
    "V_max": 100 / 3.6,  # m/s
    "e": 0.7,  # -
    "AR": 7,  # -
    "CL_max": 1.34,  # -
    "CD_0": 0.040,  # -
    "eff_prop": 0.83,  # -
    "R_C_service": 0.5,  # m/s
}

funny_inputs.update(Constraints_funny_inputs)


# ~~~ Operations ~~~

operations_funny_inputs = {}

funny_inputs.update(operations_funny_inputs)

# ~~~ Propulsion and Power ~~~

prop_n_pow_funny_inputs = {
    "wing_loading": 217,  # N
    "s_tot_sw": 0.003,  # m
    "n_prop_vtol": 4,  # number of propellers in VTOL mode
    "vtol_roc": 6,  # m/s
    "ROC_VTOL": 6,  # m/s, rate of climb in VTOL mode
    "eff_prop": 0.83,  # -
    "K_p": 0.0938,  # propeller constant (kg/W^E1 * V^E2)
    "n_props_cruise": 1,  # number of propellers in cruise
    "motor_mass_cruise": (940 + 495 + 10) * 0.001,
    "motor_mass_VTOL": 0.655 + 0.170,  # kg
    "propeller_mass_VTOL": 0.073,  # kg
    "propeller_mass_cruise": 0.0100,  # kg
    "power_available_VTOL": 1418,  # W
    "power_available_cruise": 2552,  # W
    "power_required_cruise": 1849.5497559983473,  # W
    "propeller_diameter_cruise": 0.5,  # m, guesstimate	
}

funny_inputs.update(prop_n_pow_funny_inputs)

# ~~~ Stability and control ~~~

stab_n_con_funny_inputs = {
    "ca_c": 0.4,  # Aileron chord to wing chord ratio
    "cl_alpha": 5.0 * 180 / np.pi,  # Wing airfoil (E1210) lift curve slope [1/rad]
    "cd_0": 0.02,  # Wing airfoil (E1210)Zero-lift drag coefficient
    "wing_area": 1.0,  # m^2, guesstimate
    "wing_span": 3.0,  # m, guesstimate
    "wing_chord": 0.333,  # m, guesstimate
    "bi": 0.1,  # m, location to the innermost point of the aileron
    "bo": 0.9,  # m, location to the outermost point of the aileron
    "delta_a_max": np.deg2rad(25),  # rad, maximum aileron deflection angle
    "aileron_differential": 0.75,  # Aileron differential, ratio of down-going to up-going aileron deflection
    "roll_rate_req": 0.5,  # rad/s, guesstimate
    "v_ref": 20.0,  # m/s, reference velocity for roll rate requirement
    "x_cg_no_wing": 1,  # m, x-coordinate of the center of gravity without the wing
    "mass_no_wing": 22.0,  # kg, guesstimate for the mass without the
    "wing_mass": 3,  # kg, guesstimate for the mass of the wing
    "wing_cg": 0.3,  # m, x-coordinate of the center of gravity of the wing from LEMAC
    "l_fus": 1.5,  # m, length of the fuselage
    "lh": 0.5,  # m, horizontal distance from the wing ac to the horizontal tail ac
    "mac": 0.333,  # m, mean aerodynamic chord of the wing
    "x_ac_bar": 0.25,  # m, x-coordinate of the aerodynamic center relative to the leading edge of the wing
    "CL_alpha_Ah": 5.0 * 180 / np.pi,  # Finite wing lift curve slope [1/rad]
    "CL_alpha_h": -0.8,  # Horizontal tail lift curve slope [-]
    "d_epsilon_d_alpha": 0.1,  # Downwash gradient [rad/(rad*m)]
    "Vh_V": 0.5,  # Horizontal tail velocity to wing velocity ratio [-]
    "Cm_ac": 0.3,  # Moment coefficient at the aerodynamic center of the wing [-]
    "wind_speed": 30 / 3.6,  # m/s, wind speed from requirement
    "rpm_max": 4200,  # rpm
    "T_max": 17.6 * 9.81,  # N, maximum thrust per motor.
}

funny_inputs.update(stab_n_con_funny_inputs)

# ~~~ Structures ~~~

structures_funny_inputs = {
    "wing_span": 3.0,  # m, guesstimate
    "mass_battery": 2.800 , # kg
    "battery_length": 0.182, # m 
    "mass_wing": 3, #kg
    "taper_ratio": 0.83, #-
}

funny_inputs.update(structures_funny_inputs)

# ~~~ Thermal control ~~~

thermal_funny_inputs = {}

funny_inputs.update()
