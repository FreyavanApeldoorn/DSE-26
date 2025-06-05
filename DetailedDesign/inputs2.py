



# ~~~ Hardware ~~~ selected components


mission_inputs = {
    "mission_type": "wildfire",  # or "oil_spill"
}

uav_hardware_inputs = {
    "wildfire_sensor": {
        "wildfire_sensor_mass": 0.92,  # kg, mass of the wildfire sensor
        "wildfire_sensor_power": None,
        "wildfire_sensor_length": 0.169,  # m, length of the wildfire sensor
        "wildfire_sensor_width": 0.152,  # m, width of the wildfire sensor
        "wildfire_sensor_height": 0.110,  # m, height of the wildfire sensor
        "wildfire_sensor_x": 0.08458,  # m, x-location w.r.t. front of fuselage
        "wildfire_sensor_y": None,  # m, y-location w.r.t. front of fuselage
        "wildfire_sensor_z": None,  # m, z-location w.r.t. front of fuselage
    },
    "oil_sensor": {
        "oil_sensor_mass": 0.905,  # kg, mass of the oil sensor
        "oil_sensor_power": None,
        "oil_sensor_length": 0.155,  # m, length of the oil sensor
        "oil_sensor_width": 0.128,  # m, width of the oil sensor
        "oil_sensor_height": 0.176,  # m, height of the oil sensor
        "oil_sensor_x": 0.08458,  # m, x-location w.r.t. front of fuselage
        "oil_sensor_y": None,  # m, y-location w.r.t. front of fuselage
        "oil_sensor_z": None,  # m, z-location w.r.t. front of fuselage
    },
    "gymbal_connection": {
        "gymbal_connection_mass": 0.07,  # kg, mass of the gimbal connection
        "gymbal_connection_diameter": 0.05,  # m, diameter of the gimbal connection
        "gymbal_connection_height": 0.044,  # m, height of the gimbal connection
        "gymbal_connection_x": 0.08458,  # m, x-location w.r.t. front of fuselage
        "gymbal_connection_y": None,  # m, y-location w.r.t. front of fuselage
        "gymbal_connection_z": None,  # m, z-location w.r.t. front of fuselage
    },
    "flight_controller": {
        "flight_controller_mass": 0.100,  # kg, mass of the flight controller
        "flight_controller_length": 0.0923,  # m, length of the flight controller
        "flight_controller_width": 0.0402,  # m, width of the flight controller
        "flight_controller_height": 0.02343,  # m, height of the flight controller
        "flight_controller_x": 0.95,  # m, x-location w.r.t. front of fuselage
        "flight_controller_y": None,  # m, y-location w.r.t. front of fuselage
        "flight_controller_z": None,  # m, z-location w.r.t. front of fuselage
    },
    "OBC": {
        "OBC_mass": 0.2270,  # kg, mass of the OBC
        "OBC_length": 0.1651,  # m, length of the OBC
        "OBC_width": 0.13716,  # m, width of the OBC
        "OBC_height": 0.06985,  # m, height of the OBC
        "OBC_x": 0.2185,  # m, x-location w.r.t. front of fuselage
        "OBC_y": None,  # m, y-location w.r.t. front of fuselage
        "OBC_z": None,  # m, z-location w.r.t. front of fuselage
    },
    "GPS": {
        "GPS_mass": 0.117,  # kg, mass of the GPS
        "GPS_diameter": 0.078,  # m, diameter of the GPS
        "GPS_height": 0.022,  # m, height of the GPS
        "GPS_x": 0.3463,  # m, x-location w.r.t. front of fuselage
        "GPS_y": None,  # m, y-location w.r.t. front of fuselage
        "GPS_z": None,  # m, z-location w.r.t. front of fuselage
    },
    "Mesh_network_module": {
        "Mesh_network_module_mass": 0.060,  # kg, mass of the mesh network module
        "Mesh_network_module_length": 0.123,  # m, length of the mesh network module
        "Mesh_network_module_width": 0.077,  # m, width of the mesh network module
        "Mesh_network_module_height": 0.03,  # m, height of the mesh network module
        "Mesh_network_module_x": 0.4313,  # m, x-location w.r.t. front of fuselage
        "Mesh_network_module_y": None,  # m, y-location w.r.t. front of fuselage
        "Mesh_network_module_z": None,  # m, z-location w.r.t. front of fuselage
    },
    "SATCOM_module": {
        "SATCOM_module_mass": 0.036,  # kg, mass of the SATCOM module
        "SATCOM_module_length": 0.045,  # m, length of the SATCOM module
        "SATCOM_module_width": 0.045,  # m, width of the SATCOM module
        "SATCOM_module_height": 0.017,  # m, height of the SATCOM module
        "SATCOM_module_x": 0.4313,  # m, x-location w.r.t. front of fuselage
        "SATCOM_module_y": None,  # m, y-location w.r.t. front of fuselage
        "SATCOM_module_z": None,  # m, z-location w.r.t. front of fuselage
    },
    "Winch_motor": {
        "Winch_motor_mass": 1.117,
        "Winch_motor_length": 0.17,
        "Winch_motor_width": 0.142,
        "Winch_motor_height": 0.11,
        "Winch_motor_x": 0.95,  # m, x-location w.r.t. front of fuselage
        "Winch_motor_y": None,  # m, y-location w.r.t. front of fuselage
        "Winch_motor_z": None,  # m, z-location w.r.t. front of fuselage
    },
    "PDB": {
        "PDB_mass": 0.015,
        "PBD_power": None,
        "PDB_length": 0.116,
        "PDB_width": 0.11,
        "PDB_height": 0.025,
        "PDB_x": 0.06,  # m, x-location w.r.t. front of fuselage
        "PDB_y": None,  # m, y-location w.r.t. front of fuselage
        "PDB_z": None,  # m, z-location w.r.t. front of fuselage
    },
    "battery": {
        "battery_mass": 0.5,  # kg, mass of the battery
        "battery_length": 0.2,  # m, length of the battery
        "battery_width": 0.1,  # m, width of the battery
        "battery_height": 0.05,  # m, height of the battery
        "battery_x": None,
        "battery_y": None,
        "battery_z": None,
    },
    "buoy": {
        "buoy_mass": None,
        "buoy_length": None,
        "buoy_width": None,
        "buoy_height": None,
        "buoy_x": None,
        "buoy_y": None,
        "buoy_z": None,
    },
    "motor_cruise": {
        "motor_cruise_x": None,
        "motor_cruise_y": None,
        "motor_cruise_z": None,
    },
    "motor_VTOL": {
        ""
    },
    "payload": {
        "payload_mass": None, 
        "payload_x": None,
        "payload_y": None,
        "payload_z": None,
    },

}


nest_hardware_inputs = {

}




wildfire_components = []
oil_spill_components = []

#wildfire_hardware = Hardware(hardware_inputs, wildfire_components)
#hardware_inputs = wildfire_hardware.select_components()

#oil_spill_hardware = Hardware(hardware_inputs, oil_spill_components)
#hardware_inputs = oil_spill_hardware.select_components()
