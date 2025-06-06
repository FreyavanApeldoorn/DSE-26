import pprint

"""
- Sensors
- Propulsion
- Battery
- Wings
- Structure
- Deployment


"""

component_inputs = {}

components_wildfires = {
    "wildfire_camera": {
        "wildfire_sensor_mass": 0.92,  # kg, mass of the wildfire sensor
        "wildfire_sensor_power": None,  # W, power consumption of the wildfire sensor
        "wildfire_sensor_length": 0.169,  # m, length of the wildfire sensor
        "wildfire_sensor_width": 0.152,  # m, width of the wildfire sensor
        "wildfire_sensor_height": 0.110,  # m, height of the wildfire sensor
        # Positioning:
        "wildfire_sensor_x": 0.08458,  # m, x-location w.r.t. front of fuselage
        "wildfire_sensor_y": None,  # m, y-location w.r.t. front of fuselage
        "wildfire_sensor_z": None  # m, z-location w.r.t. front of fuselage
    }
    
}
component_inputs.update(components_wildfires)


components_oldspills = {
    "oil_spill_camera": {
        "oil_sensor_mass": 0.905,  # kg, mass of the oil sensor
        "oil_sensor_power": None,  # W, power consumption of the oil sensor
        "oil_sensor_length": 0.155,  # m, length of the oil sensor
        "oil_sensor_width": 0.128,  # m, width of the oil sensor
        "oil_sensor_height": 0.176,  # m, height of the oil sensor
        # Positioning:
        "oil_sensor_x": 0.08458,  # m, x-location w.r.t. front of fuselage
        "oil_sensor_y": None,  # m, y-location w.r.t. front of fuselage
        "oil_sensor_z": None,  # m, z-location w.r.t. front of fuselage
    },
    "buoy": { 
        "buoy_mass": 0.5,  # kg, mass of the buoy

        # Positioning:
        "buoy_x": 0.5,  # m, x-location w.r.t. front of fuselage
        "buoy_y": None,  # m, y-location w.r.t. front of fuselage
        "buoy_z": None  # m, z-location w.r.t. front of fuselage
    }
}
component_inputs.update(components_oldspills)


otoher_components = {
    "gymbal_connection": {
        "gymbal_connection_mass": 0.07,  # kg, mass of the gimbal connection
        "gymbal_connection_diameter": 0.05,  # m, diameter of the gimbal connection
        "gymbal_connection_height": 0.044,  # m, height of the gimbal connection
        # Positioning:
        "gymbal_connection_x": 0.08458,  # m, x-location w.r.t. front of fuselage
        "gymbal_connection_y": None,  # m, y-location w.r.t. front of fuselage
        "gymbal_connection_z": None  # m, z-location w.r.t. front of fuselage
    },
    "flight_controller": {
        "flight_controller_mass": 0.100,  # kg, mass of the flight controller
        "flight_controller_power": None,  # W, power consumption of the flight controller
        "flight_controller_length": 0.0923,  # m, length of the flight controller
        "flight_controller_width": 0.0402,  # m, width of the flight controller
        "flight_controller_height": 0.02343,  # m, height of the flight controller
        # Positioning:
        "flight_controller_x": 0.95,  # m, x-location w.r.t. front of fuselage
        "flight_controller_y": None,  # m, y-location w.r.t. front of fuselage
        "flight_controller_z": None  # m, z-location w.r.t. front of fuselage
    },
    "OBC": {
        "OBC_mass": 0.2270,  # kg, mass of the OBC
        "OBC_power": None,  # W, power consumption of the OBC
        "OBC_length": 0.1651,  # m, length of the OBC
        "OBC_width": 0.13716,  # m, width of the OBC
        "OBC_height": 0.06985,  # m, height of the OBC
        # Positioning:
        "OBC_x": 0.2185,  # m, x-location w.r.t. front of fuselage
        "OBC_y": None,  # m, y-location w.r.t. front of fuselage
        "OBC_z": None  # m, z-location w.r.t. front of fuselage
    },
    "GPS": {
        "GPS_mass": 0.117,  # kg, mass of the GPS
        "GPS_power": None,  # W, power consumption of the GPS
        "GPS_diameter": 0.078,  # m, diameter of the GPS
        "GPS_height": 0.022,  # m, height of the GPS
        # Positioning:
        "GPS_x": 0.3463,  # m, x-location w.r.t. front of fuselage
        "GPS_y": None,  # m, y-location w.r.t. front of fuselage
        "GPS_z": None  # m, z-location w.r.t. front of fuselage
    },
    "Mesh_network_module": {   
        "Mesh_network_module_mass": 0.060,  # kg, mass of the mesh network module
        "Mesh_network_module_power": None,  # W, power consumption of the mesh network module
        "Mesh_network_module_length": 0.123,  # m, length of the mesh network module
        "Mesh_network_module_width": 0.077,  # m, width of the mesh network module
        "Mesh_network_module_height": 0.03,  # m, height of the mesh network module
        # Positioning:
        "Mesh_network_module_x": 0.4313,  # m, x-location w.r.t. front of fuselage
        "Mesh_network_module_y": None,  # m, y-location w.r.t. front of fuselage
        "Mesh_network_module_z": None  # m, z-location w.r.t. front of fuselage
    },
    "SATCOM_module": {   # Satellite communication module
        "SATCOM_module_mass": 0.036,  # kg, mass of the SATCOM module
        "SATCOM_module_power": None,  # W, power consumption of the SATCOM module
        "SATCOM_module_length": 0.045,  # m, length of the SATCOM module
        "SATCOM_module_width": 0.045,  # m, width of the SATCOM module
        "SATCOM_module_height": 0.017,  # m, height of the SATCOM module
        # Positioning:
        "SATCOM_module_x": 0.4313,  # m, x-location w.r.t. front of fuselage
        "SATCOM_module_y": None,  # m, y-location w.r.t. front of fuselage
        "SATCOM_module_z": None  # m, z-location w.r.t. front of fuselage
    },
    "PBD": {   # Power distribution board
        "PDB_mass": 0.015,
        "PDB_length": 0.116,
        "PDB_width": 0.11,
        "PDB_height": 0.025,
        # Positioning:
        "PDB_x": 0.06,  # m, x-location w.r.t. front of fuselage
        "PDB_y": None,  # m, y-location w.r.t. front of fuselage
        "PDB_z": None  # m, z-location w.r.t. front of fuselage
    }

}
component_inputs.update(otoher_components)

deployment_components = {
    "winch_motor": {
        "Winch_motor_mass": 1.117,
        "Winch_motor_power": None,  # W, power consumption of the winch motor
        "Winch_motor_length": 0.17,
        "Winch_motor_width": 0.142,
        "Winch_motor_height": 0.11,
        # Positioning:
        "Winch_motor_x": 0.95,  # m, x-location w.r.t. front of fuselage
        "Winch_motor_y": None,  # m, y-location w.r.t. front of fuselage
        "Winch_motor_z": None  # m, z-location w.r.t. front of fuselage
    },
    "winch_cable": {
    },
    "aerogel": {
        "payload_mass": 5 # kg, mass of the aerogel payload 
    }
}
component_inputs.update(deployment_components)

propulsion = {
    "propeller_cruise": {
        
    },
    "motor_cruise": {
        # Positioning:
        "motor_cruise_x": 2,  # m, x-location w.r.t. front of the fuselage
        "motor_cruise_y": None,  # m, y-location w.r.t. vertical centerline of the fuselage
        "motor_cruise_z": None  # m, z-location w.r.t. horizontal centerline of the fuselage
    },
    "propeller_VTOL": {

    },
    "motor_VTOL": {
        # Positioning:
        "motor_front_VTOL_x": -0.44,  # m, x-location w.r.t. leading edge of the wing
        "motor_rear_VTOL_x": 0.88,  # m, x-location w.r.t. leading edge of the wing
        "motor_left_VTOL_y": None,  # m, y-location w.r.t. root of the wing
        "motor_right_VTOL_y": None,  # m, y-location w.r.t. root of the wing
        "motor_VTOL_z": None  # m, z-location
    
    }
}
component_inputs.update(propulsion)


battery = {
    "battery_specific_energy": 275,  # Wh/kg, specific energy of the battery
    "battery_mass": 2.8*4,  # kg, mass of the battery
    "battery_length": 0.2,  # m, length of the battery
    "battery_width": 0.1,  # m, width of the battery
    "battery_height": 0.05,  # m, height of the battery

    # Positioning:
    "battery_x": 0.056,  # m, x-location w.r.t. leading edge of the wing
    "battery_y": None,  # m, y-location w.r.t. leading edge of the wing
    "battery_z": None  # m, z-location w.r.t. leading edge of the wing

}
component_inputs.update(battery)

wings = {

    # Positioning:


}
component_inputs.update(wings)

structure = {

}
component_inputs.update(structure)




components = component_inputs.copy()

if __name__ == '__main__':

    print("Wildfire components:")
    pprint.pprint(components_wildfires)
    print("\nOil spill components:")
    pprint.pprint(components_oldspills)
    print("\nOther components:")
    pprint.pprint(otoher_components)
    print("\nDeployment components:")
    pprint.pprint(deployment_components)
    print("\nPropulsion:")
    pprint.pprint(propulsion)
    print("\nBattery:")
    pprint.pprint(battery)
    print("\nWings:")
    pprint.pprint(wings)
    print("\nStructure:")
    pprint.pprint(structure)



