"""
This is the inputs file, these should not be changed without communicating with the entire group.
Only do this when your code is finished and verified, while working, use funny_inputs
"""

import numpy as np

inputs = {}

# ~~~ Constants ~~~

constants_inputs = {
    "g": 9.81,  # Gravitational constant [m/s2]
    "rho_0": 1.225,  # Air density at sea level [kg/m^3]
}
inputs.update(constants_inputs)


# ~~~ Requirements ~~~
requirements_inputs = {
    "M_to": 30,  # Maximum Takeoff Mass [kg]
    "MTOW": 30 * constants_inputs["g"],  # Maximum Takeoff Weight [N]
    "R_max": 20000,  # Maximum Range [m]
    "R_min": 1000,
}
inputs.update(requirements_inputs)


# ~~~ Mission ~~~ stuff that is mission-level

mission_inputs = {
    "mission_type": "wildfire",
    "mission_perimeter": 1000,  # Mission perimeter [m]
    "number_of_UAVs": 20,  # Number of UAVs in the swarm
    "number_of_containers": 3,  # Number of containers in the nest
    "number_of_workers": 2,  # Number of workers per UAV
    "wind_speed": 30 / 3.6,  # Wind speed [m/s]
}
inputs.update(mission_inputs)


# ~~~ UAV ~~~ uav performance and design parameters
uav_inputs = {
    "V_cruise": 100 / 3.6,  # Cruise speed [m/s] (converted from 100 km/h)
    "V_stall": 19,  # Stall speed [m/s]
    "h_cruise": 120,  # Mission altitude [m]
    "ROC_VTOL": 6,  # Rate of climb for VTOL mode [m/s]
    "ROD_VTOL": 3,  # Rate of descent for VTOL mode [m/s]
    "ROC_cruise": 3,  # Rate of climb for cruise mode [m/s]'
    "h_service": 3000,  # Service ceiling [m]
    "ROC_service": 0.5,  # Service rate of climb (at max altitude) [m/s]
    "rho_service": 0.9093,  # Density at service ceiling [kg/m^3]
    "time_transition": 30,  # Time for transitioning from VTOL to cruise [s]
    "time_deploy": 5 * 60,  # Time for deploying the UAV [s]: From UAV design
    "time_scan": 60,  # Time for scanning [s]: From UAV design
}
inputs.update(uav_inputs)

# ~~~ Deployment ~~~~ deployment system parameters

deployment_inputs = {
    "payload_mass": 5.0,  # kg initialized to minimum payload mass
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
    "pulley_mass": 0.2,  # kg, component needs to be picked
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
    "power_available_cruise": 2552,  # W   # - selected from components
}
inputs.update(propulsion_inputs)


# ~~~ Power ~~~ initial inputs for power sizing

power_inputs = {
    "DOD_fraction": 0.8,  # Depth of discharge fraction
    "eta_battery": 0.8,  # Battery efficiency
    "battery_specific_energy": 275,  # Wh/kg, specific energy of the battery
    "power_deploy": 0,  # W, power usage of hardware during deploy phase, updated in "hardware.py"
    "power_scan": 0,  # W, power usage of hardware during scan phase, updated in "hardware.py"
    "power_cruise_hardware": 0,  # W, power usage of hardware during cruise phase, updated in "hardware.py"
    "power_idle": 100,  # W, power usage of hardware during idle phase, estimated
}
inputs.update(power_inputs)

# ~~~ Stability and control ~~~ initial inputs for stability and control sizing

stab_n_con_inputs = {}
inputs.update(stab_n_con_inputs)

# ~~~ Aerodynamics ~~~ initial inputs for aerodynamics sizing

aerodynamics_inputs = {
    "e": 0.7,  # Oswald efficiency factor
    "AR": 7,  # Aspect ratio
    "CL_max": 1.34,  # Maximum lift coefficient
    "CD_0": 0.040,  # Zero-lift drag coefficient
    "eff_prop": 0.83,  # Propeller efficiency
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
    "CL_max": 1.34,  # Maximum lift coefficient
    "wing_loading": 217,  # Wing loading in N/m^2
    "CL_alpha": 0.09 * 180 / np.pi * 0.85,  # Lift curve slope in 1/deg
}
inputs.update(aerodynamics_inputs)

# ~~~ Structures ~~~ initial inputs for structures sizing

structures_inputs = {
    "y_prop": 0.66
    / 2,  # m, how far out from the root chord the propeller beam is placed.
    "VTOL_boom_thickness": 0.05,  # m
    "VTOL_boom_length": 0.66 * 2,  # m, based on 1 propeller diameter between propellers
    "titanium_density": 4.43 * 1000,  # kg/m3
    "titanium_E": 110 * 10**9,  # kg/m3
    "max_deflection_VTOL_boom": 0.02,  # m, guesstimate
    "load_factor": 3.5,  # due to gusts
    "fuselage_diameter": 0.2,  # m
    "max_shear_titanium": 760 * 10**6,  # Pa
    "max_stress_titanium": 1.1 * 10**9,  # Pa
    "conductivity_alu": 138,  # W/(m*K)
    "conductivity_foam": 0.04,  # W/(m*K)
    "shear_strength_foam": 1 * 10**6,  # Pa
    "shear_strength_alu": 138 * 10**6,  # Pa
    "tensile_strength_foam": 1.7 * 10**6,  # Pa
    "tensile_strength_alu": 193 * 10**6,  # Pa
    "tensile_strength_reduction_temp": 0.9,  # - https://firesciencereviews.springeropen.com/articles/10.1186/s40038-015-0007-5#:~:text=This%20concern%20is%20exacerbated%20for,(Langhelle%20and%20Amdahl%202001).
    "mass_margin": 0.05,  # 5% mass margin for structures
    "mass_structure": 5.0,  # kg, initial mass of the structure, to be updated later
}
inputs.update(structures_inputs)


# ~~~ Thermal control ~~~ initial inputs for thermal control sizing

thermal_inputs = {
    "power_thermal_required": 10,  # W, power required for thermal control (initialized to a small value)
    "mass_thermal": 0.5,
    # inputs to be added to structures:
    "T_amb_deploy": 140.0,
    "T_amb_cruise": 45.0,
    "T_int_init": 30.0,
    "T_int_cruise_set": 30.0,
    "A_heat_shell": 0.5,
    "t_shell": 0.002,
    "k_Ti": 6.7,
    "include_insulation": True,
    "t_insulation": 0.01,  # THIS SHOULD BE MOVED TO SIZING IN THERMAL
    "k_insulation": 0.017,
    "heat_coeff_ext": 45.0,
    "heat_int": 200.0,
    "m_int": 10.0,  # COMES FROM HARDWARE
    "c_p_int": 500.0,
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
    "margin": 5.0,
    "nest_length": 5.9,
    "nest_width": 2.35,
    "nest_height": 2.39,
    "nest_empty_mass": 100.0,
    "generator_efficiency": 0.85,
    "diesel_energy_density": 9.94,
}
inputs.update(nest_inputs)


stab_n_con_inputs = {
    "ca_c": 0.3,  # Aileron chord to wing chord ratio
    "cl_alpha": 5.0 * 180 / np.pi,  # Wing airfoil (E1210) lift curve slope [1/rad]
    "cd_0": 0.02,  # Wing airfoil (E1210)Zero-lift drag coefficient
    "wing_area": 1.27,  # m^2, guesstimate
    "wing_span": 3.0,  # m, guesstimate
    "wing_root_chord": 0.458,  # m, guesstimate
    "wing_tip_chord": 0.39,  # m, guesstimate
    "bi": 0.75,  # m, location to the innermost point of the aileron
    "bo": 0.76,  # m, location to the outermost point of the aileron
    "delta_a_max": np.deg2rad(25),  # rad, maximum aileron deflection angle
    "aileron_differential": 0.75,  # Aileron differential, ratio of down-going to up-going aileron deflection
    "roll_rate_req": np.deg2rad(20),  # rad/s, guesstimate
    "v_ref": 72 * 0.8 / 3.6,  # m/s, reference velocity for roll rate requirement
    "wildfire_fuselage_x_cg": 0,  # m, initially set to 0 and updated later
    "oil_spill_fuselage_x_cg": 0,  # m, initially set to 0 and updated later
    "wildfire_wing_x_cg": 0,  # m, initially set to 0 and updated later
    "oil_spill_wing_x_cg": 0,  # m, initially set to 0 and updated later
    "wildfire_fuselage_mass": 0,  # kg, initially set to 0 and updated later
    "oil_spill_fuselage_mass": 0,  # kg, initially set to 0 and updated later
    "wildfire_wing_mass": 0,  # kg, initially set to 0 and updated later
    "oil_spill_wing_mass": 0,  # kg, initially set to 0 and updated later
    "no_payload_fuselage_x_cg": 0,  # m, x-location of the center of gravity without payload
    "no_payload_fuselage_mass": 0,  # kg, mass of the fuselage without payload
    # control and stability curve parameters
    "l_fus": 2,  # m, length of the fuselage
    "fuselage_diameter": 0.4,  # m, diameter of the fuselage
    "lh": 1.2,  # m, horizontal distance from the wing ac to the horizontal tail ac
    "mac": 0.333,  # m, mean aerodynamic chord of the wing
    "x_ac_bar_wing": 0.24,  # m, x-coordinate of the aerodynamic center relative to the leading edge of the wing, based on ADSEE estimation lecture 8
    "CL_alpha_Ah": 0.08,  # Finite wing lift curve slope [1/rad]
    "CL_alpha_h": 0.06,  # Horizontal tail lift curve slope [-]
    "d_epsilon_d_alpha": 0.3,  # Downwash gradient [rad/(rad*m)]
    "Vh_V": 0.85,  # Horizontal tail velocity to wing velocity ratio [-]
    "Cm_ac_wing": -0.11,  # Moment coefficient at the aerodynamic center of the wing at zero lift [-] based on XFLR5
    "AR_h": 3.5,  # Aspect ratio of the horizontal tail [-]
    "CL_A-h": 0.62,  # Lift coefficient of the aircraft - tail at cruise conditions [-]
    # other parameters
    "wind_speed": 30 / 3.6,  # m/s, wind speed from requirement
    "rpm_max": 4200,  # rpm
    "T_max": 17.6 * 9.81,  # N, maximum thrust per motor.
    "gust_speed": 30 / 3.6,  # m/s, gust speed
    "lvt": 6.0,  # m, distance from wing AC to AC of vertical tailplane
    "Vv": 0.1,  # Tail volume coefficient [–]
    "ARvt": 3.5,  # Aspect ratio of the vertical tailplane [–]
    "taper_ratio_vt": 0.5,  # Taper ratio of the vertical tailplane [–]
    "sweep_vt": np.deg2rad(5),  # Sweep angle of the vertical tailplane [rad]
    "br_bv": 0.9,  # Ratio of the rudder span to the vertical tailplane span[–]
    "delta_r_max": np.deg2rad(30),  # Maximum rudder deflection angle [rad]
    "cr_cv_init": 0.3,  # Ratio of the rudder chord to the vertical tailplane chord [–]
}
inputs.update(stab_n_con_inputs)


# ===========================================

initial_inputs = inputs.copy()

if __name__ == "__main__":
    for key, value in inputs.items():
        print(f"{key}: {value}")
