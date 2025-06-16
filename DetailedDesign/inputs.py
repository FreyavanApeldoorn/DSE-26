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
    "nu": 0.00001702,  # m^2/s, kinematic viscosity of air at ~300K
    "alpha": 0.00002346,  # m^2/s, thermal diffusivity of air at ~300K
    "k_air": 0.02662,  # W/(mK), thermal conductivity of air at ~300K
    "h_air_forced": 100.0,  # W/m^2, forced air convection coefficient
    "epsilon": 0.85,  # -, emissivity of the heat sink surface
    "sigma": 5.67e-8,  # W/(mK^4), Stefan–Boltzmann constant
    "Prandtl": 0.7268,  # Prandtl number for air at 35C
}
inputs.update(constants_inputs)


# ~~~ Requirements ~~~
requirements_inputs = {
    "M_to": 30,  # Maximum Takeoff Mass [kg]
    "MTOW": 30 * constants_inputs["g"],  # Maximum Takeoff Weight [N]
    "R_max": 20000,  # Maximum Range [m]
    "R_min": 2000,
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
    "wing_eff_area": 0.75,  # m, effective surface area for conduction
    "fuselage_eff_area": 2.01,  # 7.04, # m, effective surface area for conduction
    "T_amb_onsite": 140.0 + 273.15,  # K, temperature in the onsite deployment zone
    "T_amb_enroute": 35.0 + 273.15,  # K, ambient temperature outside of deployment zone
    "T_int": 40.0 + 273.15,  # K, temperature inside the fuselage+wing structure
    "T_equi_pcm": 48.0
    + 273.15,  # K, temperature at which the PCM starts changing phase
    # "sink_length": 0.3, # m, length of the base of the heat sink parallel to fins axes
    "sink_height": 0.02,  # m, height of heat sink fins
    "sink_thickness": 0.001,  # m, thickness of heat sink fins
    "sink_base": 0.0005,  # m, thickness of heat sink base
    "sink_density": 2710.0,  # kg/m^3
    "sink_time_margin": 30,  # s, this is extra downtime for the UAVs on ground to reduce heat sink size
    "thickness_foam_wing": 0.0,  # 0.03, # m, thickness of the foam inbetween the aluminium shell
    "thickness_alu_wing": 0.00078,  # m, thickness of one layer of the aluminium shell structure
    "thickness_foam_fuselage": 0.0,  # 0.03, # m
    "thickness_alu_fuselage": 0.00026,  # m
    "conductivity_alu": 0.36,  # 237., # W / (mK)
    "conductivity_foam": 0.0,  # 0.03, # W / (mK)
    "conductivity_insulation": 0.012,  # W / (mK)
    "insulation_density": 30,  # kg/m^3
    "pcm_latent_heat": 197000.0,  # J/kg
    "n_battery": 2,
    "battery_resistance": 0.015,  # Ohm, based on guessing
    "processor_heat_diss": 40.0,  # W, guesstimate which should eventually come from the chosen processor
    "winch_eff": 0.65,  # Winch efficiency fraction (0.35=35% efficiency) used to compute the heat generated
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
    # ───────────────────────────────────────────────────────────────────────
    # Aerodynamic & control-surface parameters
    # ───────────────────────────────────────────────────────────────────────
    "cl_alpha": 0.1 * 180 / np.pi,  # [1/rad] Wing lift-curve slope (E1233)
    "cd_0": 0.11,  # Zero-lift drag coefficient (E1233)
    "ca_c": 0.3,  # Aileron chord / wing chord ratio
    "delta_a_max": np.deg2rad(25),  # [rad] Max aileron deflection
    "aileron_differential": 0.75,  # Down-/up-going deflection ratio
    "roll_rate_req": np.deg2rad(35),  # [rad/s] Required roll rate
    "v_ref": 72 * 0.8 / 3.6,  # [m/s] Reference velocity (80% of 72 km/h)
    # ───────────────────────────────────────────────────────────────────────
    # Wing geometry
    # ───────────────────────────────────────────────────────────────────────
    "wing_area": 1.27,  # [m²] planform area (estimate)
    "wing_span": 3.0,  # [m] span (estimate)
    "wing_root_chord": 0.458,  # [m] root chord (estimate)
    "wing_tip_chord": 0.39,  # [m] tip chord (estimate)
    "bi": 0.875,  # [m] inboard aileron start
    "bo": 0.91,  # [m] outboard aileron end
    # ───────────────────────────────────────────────────────────────────────
    # Mass & CG placeholders
    # ───────────────────────────────────────────────────────────────────────
    "fuselage_structural_mass": 3.166,  # [kg] fuselage structure mass
    "fuselage_structural_x_cg": 2.15 / 2,  # [m] fuselage CG location
    "wing_structural_mass": (2.24 + 0.255 + 0.047*4) * 2,  # [kg] wing structure mass
    "wing_structural_x_cg": 0.42 * 0.25,  # [m] wing CG location (25% MAC)
    "tailplane_structural_mass": 1.656,  # [kg] tailplane structure mass
    "tailplane_structural_x_cg": 2.15 - 0.35 * 0.75,  # [m] tailplane CG location,
    # → wildfire
    "wildfire_sensor_mass": 0.92,  # [kg] wildfire sensor mass
    "wildfire_sensor_x": 0.174,  # [m] wildfire sensor CG location
    "wildfire_fuselage_mass": 0.0,  # [kg] wildfire fuselage mass
    "wildfire_fuselage_x": 0.0,  # [m] wildfire fuselage CG location
    "wildfire_wing_mass": 0.0,  # [kg] wildfire wing mass
    "wildfire_wing_x": 0.0,  # [m] wildfire wing CG location
    # → oil spill
    "oil_spill_sensor_mass": 0.905,  # [kg] oil spill sensor mass
    "oil_spill_sensor_x": 0.174,  # [m] oil spill sensor CG location
    "oil_spill_fuselage_mass": 0.0,  # [kg] oil spill fuselage mass
    "oil_spill_fuselage_x": 0.0,  # [m] oil spill fuselage CG location
    "oil_spill_wing_mass": 0.0,  # [kg] oil spill wing mass
    "oil_spill_wing_x": 0.0,  # [m] oil spill wing CG location
    # → no payload
    "no_payload_fuselage_mass": 0.0,  # [kg] no payload fuselage mass
    "no_payload_fuselage_x_cg": 0.0,  # [m] no payload fuselage CG location
    # ───────────────────────────────────────────────────────────────────────
    # Payload & sensor modules
    # ───────────────────────────────────────────────────────────────────────
    "payload_mass": 5.0,  # [kg] payload mass (aerogel blanket)
    "payload_x": 1.15,  # [m] payload CG location (initially set to oil-spill buoy location)
    "buoy_mass": 0.140*4,  # [kg] Oil-spill buoy mass (4 buoys)
    "buoy_x": 1.08,  # [m] Buoy CG location (initially set to oil-spill buoy location)
    # ───────────────────────────────────────────────────────────────────────
    # Fuselage-mounted avionics & structure
    # ───────────────────────────────────────────────────────────────────────
    "gymbal_connection_mass": 0.070,  # [kg] mass of the gymbal connection
    "gymbal_connection_x": 0.174,  # [m] CG location of the gymbal connection
    "flight_controller_mass": 0.032,  # [kg] mass of the flight controller
    "flight_controller_x": 0.415,  # [m] CG location of the flight controller
    "OBC_mass": 0.7,  # [kg] mass of the on-board computer
    "OBC_x": 0.223,  # [m] CG location of the on-board computer
    "GPS_mass": 0.012,  # [kg] mass of the GPS module
    "GPS_x": 0.321,  # [m] CG location of the GPS module
    "Mesh_network_module_mass": 0.0365,  # [kg] mass of the mesh network module
    "Mesh_network_module_x": 0.080,  # [m] CG location of the mesh network module
    "SATCOM_module_mass": 0.033,  # [kg] mass of the SATCOM module
    "SATCOM_module_x": 0.036,  # [m] CG location of the SATCOM module
    "Winch_motor_mass": 1.17,  # [kg] mass of the winch motor
    "Winch_motor_x": 0.537,  # [m] CG location of the winch motor
    "CUAV_airlink_mass": 0.052,  # [kg] mass of the CUAV airlink module
    "CUAV_airlink_x": 0.138,  # [m] CG location of the CUAV airlink module
    # ───────────────────────────────────────────────────────────────────────
    # Propulsion & energy-storage
    # ───────────────────────────────────────────────────────────────────────
    # — Cruise motor + prop
    "motor_mass_cruise": 0.280,  # [kg] mass of the cruise motor
    "motor_esc_cruise_mass": 0.110,  # [kg] mass of the cruise motor ESC
    "motor_esc_cruise_x": 2.150,  # [m] x-location of the cruise motor
    "propeller_mass_cruise": 0.097,  # [kg] mass of the cruise propeller
    "motor_cruise_x": 2.150,  # [m] x-location of the cruise motor
    # — VTOL lift motors + props
    "motor_mass_VTOL": 0.280,  # [kg] mass of each VTOL motor
    "propeller_mass_VTOL": 0.097,  # [kg] mass of each VTOL propeller
    "motor_esc_VTOL_mass": 0.110,  # [kg] mass of the cruise motor ESC
    "motor_front_VTOL_x": -0.551,  # [m] x-location of the front VTOL motor
    "motor_rear_VTOL_x": 0.974,  # [m] x-location of the rear VTOL motor
    # — Battery & power distribution
    "battery_mass": 3.619 * 2,  # [kg] mass of the battery (2 batteries)
    "battery_x": 0.173,  # [m] x-location of the battery w.r.t leading edge wing
    "PDB_mass": 0.156,  # [kg] mass of the power distribution board
    "PDB_x": 0.173,  # [m] x-location of the power distribution board w.r.t leading edge wing
    "thermal_control_mass": 1.75,  # [kg] mass of the thermal control system
    "thermal_control_x": 0.173,  # [m] x-location of the thermal control system w.r.t leading edge wing
    # ───────────────────────────────────────────────────────────────────────
    # Longitudinal stability & tailplane
    # ───────────────────────────────────────────────────────────────────────
    "l_fus": 2.15,  # [m] fuselage length
    "fuselage_diameter": 0.4,  # [m] fuselage diameter
    "lh": 0.831,  # [m] wing AC → tail AC
    "mac": 0.42,  # [m] mean aerodynamic chord
    "x_ac_bar_wing": 0.25,  # [-] wing AC from LE (25% MAC)
    "CL_alpha_Ah": 0.08 * 180 / np.pi,  # [1/rad] finite wing lift-curve slope
    "CL_alpha_h": 0.06 * 180 / np.pi,  # [1/rad] tail lift-curve slope
    "d_epsilon_d_alpha": 0.3,  # downwash gradient [rad/rad]
    "Vh_V": 0.9**2,  # tail/wing velocity ratio
    "Cm_ac_wing": -0.017,  # moment coeff. at wing AC
    "AR_h": 3.5,  # tail aspect ratio
    "CL_A_h": 0.55,  # C_L aircraft minus tail at cruise
    # ───────────────────────────────────────────────────────────────────────
    # Lateral/directional & vertical tail
    # ───────────────────────────────────────────────────────────────────────
    "lvt": 6.0,  # [m] wing AC → vertical tail AC
    "Vv": 0.1,  # volume coeff. vertical tail
    "ARvt": 3.5,  # vertical tail aspect ratio
    "taper_ratio_vt": 0.5,  # vertical tail taper
    "sweep_vt": np.deg2rad(5),  # vertical tail sweep [rad]
    "br_bv": 0.9,  # rudder span ratio
    "delta_r_max": np.deg2rad(30),  # max rudder deflection [rad]
    "cr_cv_init": 0.3,  # rudder chord ratio
    "ce_cht_init": 0.3,  # elevator chord ratio
    "delta_e_max_up": np.deg2rad(20),  # max elevator deflection [rad]
    "delta_e_max_down": np.deg2rad(25),  # max elevator deflection [rad]
    "alpha_h": np.deg2rad(5),  # [rad] angle of attack at cruise
    # ───────────────────────────────────────────────────────────────────────
    # Environmental & propulsion limits
    # ───────────────────────────────────────────────────────────────────────
    "wind_speed": 30 / 3.6,  # [m/s] requirement gust
    "gust_speed": 30 / 3.6,  # [m/s] gust speed
    "rpm_max": 4200,  # [rpm] motor limit
    "T_max": 17.6 * 9.81,  # [N] thrust per motor
    # ───────────────────────────────────────────────────────────────────────
    # CG Range
    # ───────────────────────────────────────────────────────────────────────
    "most_forward_cg": 0.1,  # [-] most forward CG location (as fraction of fuselage length)
    "most_aft_cg": 0.9,  # [-] most aft CG location (as fraction of fuselage length)
}

inputs.update(stab_n_con_inputs)


# ===========================================

initial_inputs = inputs.copy()

if __name__ == "__main__":
    for key, value in inputs.items():
        print(f"{key}: {value}")
