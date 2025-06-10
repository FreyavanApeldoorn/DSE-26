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

aerodynamics_funny_inputs = {
    "AR": 7,  # Aspect ratio of the wing
    "wing_area": 1.27,  # [m^2], Wing area
    "taper_ratio": 0.85,  # Taper ratio of the wing
    "sweep_angle": 0.0,  # Sweep angle of the wing in degrees
    "thickness_to_chord_ratio": 0.12,  # Thickness to chord ratio for the wing max
    "span_position": 0.3,  # Span position of interest main wing
    "tail_length": 1.06,  # Length betweem ac tail horizontal and wing ac in m
    "horizontal_tail_coefficient": 0.7,  # Coefficient for horizontal tail area calculation
    "taper_ratio_horizontal_tail": 0,  # Taper ratio for horizontal tail
    "sweep_angle_horizontal_tail": 0.0,  # Sweep angle of the horizontal tail in degrees
    "relative_horizontal_tail_aspect_ratio": 0.5,  # Relative aspect ratio of the horizontal tail to the wing
    "vertical_tail_length": 1.06,  # Length betweem ac tail vertical and wing ac in m
    "vertical_tail_coefficient": 0.032,  # Coefficient for vertical tail area calculation
    "taper_ratio_vertical_tail": 0.58,  # Taper ratio for vertical tail
    "sweep_angle_vertical_tail": 0.0,  # Sweep angle of the vertical tail in degrees
    "relative_vertical_tail_aspect_ratio": 0.5,  # Relative aspect ratio of the vertical tail to the wing
    "max_load_factor": 3.5,  # Maximum load factor for maneuvering
    "min_load_factor": -1.0,  # Minimum load factor for maneuvering
    "density_sea": 1.225,  # Air density in kg/m^3
    "density_3000": 0.9093,  # Air density at 3000m in kg/m^3
    "CL_max": 1.34,  # Maximum lift coefficient
    "wing_loading": 217,  # Wing loading in N/m^2
    "cruise_velocity": 100 / 3.6,  # Cruise speed in m/s
}

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
    "power_required_winch": 96.0,  # W, follows from PSDK protocol of DJI (24V/4A)
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
    "wing_area": 1.27,  # m^2, guesstimate
    "wing_span": 3.0,  # m, guesstimate
    "wing_root_chord": 0.458,  # m, guesstimate
    "wing_tip_chord": 0.39,  # m, guesstimate
    "bi": 0.5,  # m, location to the innermost point of the aileron
    "bo": 0.76,  # m, location to the outermost point of the aileron
    "delta_a_max": np.deg2rad(25),  # rad, maximum aileron deflection angle
    "aileron_differential": 0.75,  # Aileron differential, ratio of down-going to up-going aileron deflection
    "roll_rate_req": np.deg2rad(1),  # rad/s, guesstimate
    "v_ref": 20.0,  # m/s, reference velocity for roll rate requirement
    "x_cg_no_wing": 1,  # m, x-coordinate of the center of gravity without the wing
    "mass_no_wing": 22.0,  # kg, guesstimate for the mass without the
    "wing_mass": 3,  # kg, guesstimate for the mass of the wing
    "wing_cg": 0.3,  # m, x-coordinate of the center of gravity of the wing from LEMAC
    "l_fus": 1.5,  # m, length of the fuselage
    "lh": 0.5,  # m, horizontal distance from the wing ac to the horizontal tail ac
    "mac": 0.333,  # m, mean aerodynamic chord of the wing
    "x_ac_bar": 0.25,  # nondimensional (×MAC) aerodynamic centre position of the wing
    "CL_alpha_Ah": 0.08,  # finite-wing lift-curve slope [1/rad] based on XFLR5 values
    "CL_alpha_h": 0.065,  # tailplane lift-curve slope [1/rad] based on XFLR5 values
    "d_epsilon_d_alpha": 0.1,  # downwash gradient [–]
    "Vh_V": 0.85,  # ratio of tailplane to wing freestream velocity [–] based on ADSEE slides
    "Cm_ac": 0.3,  # wing moment coefficient about the aerodynamic centre [–]
    "wind_speed": 30.0 / 3.6,  # m/s, design gust/wind speed requirement
    "rpm_max": 4200,  # rpm, maximum motor speed (not directly used here)
    "T_max": 17.6 * 9.81,  # N, maximum thrust per VTOL motor
    "Propeller_diameter_VTOL": 0.30,  # m, diameter of each VTOL propeller
    "mtow": 25.0,  # kg, maximum take‐off mass of one UAV
    "n_prop_vtol": 4,  # number of VTOL propulsors per UAV
    "lvt": 6.0,  # m, distance from wing AC to AC of vertical tailplane
    "Vv": 0.6,  # Tail volume coefficient [–]
    "ARvt": 2,  # Aspect ratio of the vertical tailplane [–]
    "taper_ratio_vt": 0.5,  # Taper ratio of the vertical tailplane [–]
    "sweep_vt": np.deg2rad(5),  # Sweep angle of the vertical tailplane [rad]
    "br_bv": 0.7,  # Ratio of the rudder span to the vertical tailplane span[–]
    "delta_r_max": np.deg2rad(30),  # Maximum rudder deflection angle [rad]
    "cr_cv": 0.3,  # Ratio of the rudder chord to the vertical tailplane chord [–]
}

funny_inputs.update(stab_n_con_funny_inputs)

# ~~~ Structures ~~~

structures_funny_inputs = {
    "wing_span": 3.0,  # m, guesstimate
    "mass_battery": 2.800 , # kg
    "battery_length": 0.182, # m 
    "mass_wing": 3, #kg
    "taper_ratio": 0.83, #-
    "propeller_diameter_VTOL": 0.66, #m
    "mass_propulsion": 5, #kg
    "propeller_mass_VTOL": 0.073, #kg
    "y_prop": 0.66 / 2, #m, how far out from the root chord the propeller beam is placed. 
    "VTOL_boom_thickness": 0.05, #m
    "VTOL_boom_length": 0.66 * 2, #m, based on 1 propeller diameter between propellers
    "titanium_density": 4.43 * 1000, #kg/m3
    "titanium_E": 110 * 10**9, #kg/m3
    "max_deflection_VTOL_boom": 0.02, #m, guesstimate
    "load_factor": 3.5, #due to gusts
    "fuselage_diameter": 0.4, # m
    "max_shear_titanium": 760*10**6, #Pa
    "max_stress_titanium": 1.1*10**9, #Pa

    "conductivity_alu": 138, # W/(m*K)
    "conductivity_foam": 0.04, # W/(m*K)
    "shear_strength_foam": 1 * 10**6, #Pa
    "shear_strength_alu": 138 * 10**6, #Pa 
    "tensile_strength_foam": 1.7 * 10**6, #Pa
    "tensile_strength_alu": 193 * 10**6, #Pa
    "tensile_strength_reduction_temp": 0.9, #- https://firesciencereviews.springeropen.com/articles/10.1186/s40038-015-0007-5#:~:text=This%20concern%20is%20exacerbated%20for,(Langhelle%20and%20Amdahl%202001).
}

funny_inputs.update(structures_funny_inputs)

# ~~~ Thermal control ~~~

thermal_funny_inputs = {
    "T_amb_deploy": 140.0,
    "T_amb_cruise": 45.0,
    "T_int_init": 30.0,
    "T_int_cruise_set": 30.0,
    "A_heat_shell": 0.5,
    "t_shell": 0.002,
    "k_Ti": 6.7,
    "include_insulation": True,
    "t_insulation": 0.01,
    "k_insulation": 0.017,
    "heat_coeff_ext": 45.0,
    "heat_int": 200.0,
    "m_int": 10.0,
    "c_p_int": 500.0,
    "power_thermal_required": -300.0,  # Negative = cooling ; Positive = heating
    "n_battery": 4,
    "battery_capacity": 10., # Ah
    "battery_potential": 44.4, # V
    "battery_resistance": 0.015, # Ohm, based on guessing
    "processor_heat_dissipated": 40., # W, guesstimate which should eventually come from the chosen processor
    "winch_eff": 0.65, # Winch efficiency fraction (0.35=35% efficiency) used to compute the heat generated

}

funny_inputs.update(thermal_funny_inputs)

final_outputs = {
    "g": 9.81,
    "rho_0": 1.225,
    "M_to": 30,
    "MTOW": 294.3,
    "R_max": 20000,
    "mission_type": "wildfire",
    "mission_perimeter": 1000,
    "number_of_UAVs": 20,
    "number_of_containers": 3,
    "number_of_workers": 2,
    "V_cruise": 27.77777777777778,
    "V_stall": 19,
    "h_cruise": 120,
    "ROC_VTOL": 6,
    "ROD_VTOL": 3,
    "ROC_cruise": 3,
    "h_service": 3000,
    "ROC_service": 0.5,
    "rho_service": 0.9093,
    "time_transition": 30,
    "time_deploy": 130.0,
    "time_scan": 60,
    "payload_mass": np.float64(10.001411288598778),
    "aerogel_width": 1.5,
    "aerogel_thickness": 0.003,
    "aerogel_density": 200.0,
    "n_ferro_magnets": 2,
    "ferro_magnet_mass": 0.5,
    "deployment_added_mass": 1.0,
    "wire_length": 15.0,
    "wire_density": 0.0149,
    "n_wire": 2,
    "spring_mass": 0.0,
    "winch_mass": 1.5,
    "n_pulleys": 4,
    "pulley_mass": 0.2,
    "n_epms": 4,
    "epm_diameter": 0.0025,
    "epm_mass": 0.039,
    "deployment_system_volume": 0.0026554,
    "deployment_speed": 0.3,
    "deployment_time_margin": 30.0,
    "power_required_epm": 20.0,
    "epm_duration": 8.0,
    "power_required_winch": 96.0,
    "deployment_accuracy": 0.5,
    "firebreak_width": 3,
    "fuselage_size": 1.5,
    "wing_loading": 219.932391,
    "s_tot_sw": 0.003,
    "n_prop_vtol": 4,
    "vtol_roc": 6,
    "eff_prop": 0.83,
    "K_p": 0.0938,
    "n_props_cruise": 1,
    "motor_mass_cruise": 1.445,
    "motor_mass_VTOL": 0.8250000000000001,
    "propeller_mass_VTOL": 0.073,
    "propeller_mass_cruise": 0.01,
    "power_available_VTOL": 1418,
    "power_available_cruise": 2552,
    "DOD_fraction": 0.8,
    "eta_battery": 0.9,
    "e": 0.7,
    "AR": 7,
    "CL_max": 1.34,
    "CD_0": 0.04,
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
    "margin": 5.0,
    "nest_length": 5.9,
    "nest_width": 2.35,
    "nest_height": 2.39,
    "nest_empty_mass": 100.0,
    "generator_efficiency": 0.85,
    "diesel_energy_density": 9.94,
    "aerogel_mass": np.float64(8.001411288598778),
    "aerogel_length": np.float64(8.89),
    "aerogel_diameter": 0.18429950839498332,
    "power_deploy": 176.0,
    "total_deployment_energy": 13120.0,
    "wire_mass": 0.2235,
    "deployment_system_mass": np.float64(12.904411288598778),
    "nr_aerogels": np.float64(358.0),
    "power_scan": 300,
    "power_idle": 100,
    "mass_hardware": 5.0,
    "trips_for_mission": np.float64(358.0),
    "time_uav": np.float64(1930.0),
    "time_cruise": np.float64(1440.0),
    "time_cruise_min": np.float64(996.0),
    "time_ascent": np.float64(20.0),
    "time_descent": np.float64(40.0),
    "time_turnaround": 60.0,
    "time_preparation": 1345.2631578947369,
    "time_operation": np.float64(34740.0),
    "time_wrapup": 1525.2631578947369,
    "total_mission_time": np.float64(37610.52631578948),
    "true_deployment_rate": np.float64(0.026588301147495098),
    "P_W_cruise": np.float64(3.501613051736337),
    "P_W_climb": np.float64(6.284572735298496),
    "P_W_service": np.float64(3.2725245425274117),
    "power_required_cruise": np.float64(1849.5497559983473),
    "power_required_VTOL": np.float64(3475.137999774786),
    "power_required_hover": np.float64(5937.967792698869),
    "propeller_diameter_VTOL": np.float64(0.7386719243500363),
    "propeller_diameter_cruise": np.float64(0.6151334488952356),
    "mass_propulsion": 5.047,
    "power_transition": np.float64(7787.517548697217),
    "mass_battery": np.float64(0.0015887114012244931),
    "required_capacity_wh": np.float64(988.3055884737328),
    "battery_capacity": np.float64(988.3055884737328),
    "wing_area": 0.2558020925267316,
    "wing_span": 1.3381385009359537,
    "mass_structure": 9.95,
    "number_of_nests": 2,
    "nests_volume": 66.27470000000001,
    "volume_fueltank": 1.8296442000000004,
    "refills_for_mission": 0,
}
funny_inputs.update(final_outputs)


funny_inputs.update()

# ~~~ Hardware ~~~

hardware_funny_inputs = {
    # Wildfire Sensor
    "wildfire_sensor_mass": 0.92,  # kg, mass of the wildfire sensor
    "wildfire_sensor_length": 0.169,  # m, length of the wildfire sensor
    "wildfire_sensor_width": 0.152,  # m, width of the wildfire sensor
    "wildfire_sensor_height": 0.110,  # m, height of the wildfire sensor
    "wildfire_sensor_x": None,  # m, x-location w.r.t. front of fuselage
    "wildfire_sensor_y": None,  # m, y-location w.r.t. front of fuselage
    "wildfire_sensor_z": None,  # m, z-location w.r.t. front of fuselage
    # Oil Sensor
    "oil_sensor_mass": 0.905,  # kg, mass of the oil sensor
    "oil_sensor_length": 0.155,  # m, length of the oil sensor
    "oil_sensor_width": 0.128,  # m, width of the oil sensor
    "oil_sensor_height": 0.176,  # m, height of the oil sensor
    "oil_sensor_x": None,  # m, x-location w.r.t. front of fuselage
    "oil_sensor_y": None,  # m, y-location w.r.t. front of fuselage
    "oil_sensor_z": None,  # m, z-location w.r.t. front of fuselage
    # Gimbal Connection
    "gymbal_connection_mass": 0.07,  # kg, mass of the gimbal connection
    "gymbal_connection_diameter": 0.05,  # m, diameter of the gimbal connection
    "gymbal_connection_height": 0.044,  # m, height of the gimbal connection
    "gymbal_connection_x": None,  # m, x-location w.r.t. front of fuselage
    "gymbal_connection_y": None,  # m, y-location w.r.t. front of fuselage
    "gymbal_connection_z": None,  # m, z-location w.r.t. front of fuselage
    # Flight Controller
    "flight_controller_mass": 0.100,  # kg, mass of the flight controller
    "flight_controller_length": 0.0923,  # m, length of the flight controller
    "flight_controller_width": 0.0402,  # m, width of the flight controller
    "flight_controller_height": 0.02343,  # m, height of the flight controller
    "flight_controller_x": None,  # m, x-location w.r.t. front of fuselage
    "flight_controller_y": None,  # m, y-location w.r.t. front of fuselage
    "flight_controller_z": None,  # m, z-location w.r.t. front of fuselage
    # OBC (On-Board Computer)
    "OBC_mass": 0.2270,  # kg, mass of the OBC
    "OBC_length": 0.1651,  # m, length of the OBC
    "OBC_width": 0.13716,  # m, width of the OBC
    "OBC_height": 0.06985,  # m, height of the OBC
    "OBC_x": None,  # m, x-location w.r.t. front of fuselage
    "OBC_y": None,  # m, y-location w.r.t. front of fuselage
    "OBC_z": None,  # m, z-location w.r.t. front of fuselage
    # GPS
    "GPS_mass": 0.117,  # kg, mass of the GPS
    "GPS_diameter": 0.078,  # m, diameter of the GPS
    "GPS_height": 0.022,  # m, height of the GPS
    "GPS_x": None,  # m, x-location w.r.t. front of fuselage
    "GPS_y": None,  # m, y-location w.r.t. front of fuselage
    "GPS_z": None,  # m, z-location w.r.t. front of fuselage
    # Mesh Network Module
    "Mesh_network_module_mass": 0.060,  # kg, mass of the mesh network module
    "Mesh_network_module_length": 0.123,  # m, length of the mesh network module
    "Mesh_network_module_width": 0.077,  # m, width of the mesh network module
    "Mesh_network_module_height": 0.03,  # m, height of the mesh network module
    "Mesh_network_module_x": None,  # m, x-location w.r.t. front of fuselage
    "Mesh_network_module_y": None,  # m, y-location w.r.t. front of fuselage
    "Mesh_network_module_z": None,  # m, z-location w.r.t. front of fuselage
    # SATCOM Module
    "SATCOM_module_mass": 0.036,  # kg, mass of the SATCOM module
    "SATCOM_module_length": 0.045,  # m, length of the SATCOM module
    "SATCOM_module_width": 0.045,  # m, width of the SATCOM module
    "SATCOM_module_height": 0.017,  # m, height of the SATCOM module
    "SATCOM_module_x": None,  # m, x-location
}
