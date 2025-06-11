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
        "wildfire_sensor_name": "DJI Zenmuse H30T",
        "wildfire_sensor_mass": 0.92,  # kg, mass of the wildfire sensor
        "wildfire_sensor_power": 28,  # W, power consumption of the wildfire sensor
        "wildfire_sensor_voltage": 44.4,  # V, voltage of the wildfire sensor
        "wildfire_sensor_cost": 13_500,  # Cost of the wildfire sensor, if available
        
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


components_oilspills = {
    "oil_spill_camera": {
        "oil_sensor_name": "DJI Zenmuse L2",
        "oil_sensor_mass": 0.905,  # kg, mass of the oil sensor
        "oil_sensor_power": 28,  # W, power consumption of the oil sensor
        "oil_sensor_voltage": 44.4,  # V, voltage of the oil sensor
        "oil_sensor_cost": 14_280,
        "oil_sensor_length": 0.155,  # m, length of the oil sensor
        "oil_sensor_width": 0.128,  # m, width of the oil sensor
        "oil_sensor_height": 0.176,  # m, height of the oil sensor
        # Positioning:
        "oil_sensor_x": 0.08458,  # m, x-location w.r.t. front of fuselage
        "oil_sensor_y": None,  # m, y-location w.r.t. front of fuselage
        "oil_sensor_z": None,  # m, z-location w.r.t. front of fuselage
    },
    "buoy": { 
        "buoy_name": "Flyfiretech Drone Buoy",
        "buoy_mass": 0.560,  # kg, mass of the buoy, 

        # Positioning:
        "buoy_x": 0.5,  # m, x-location w.r.t. front of fuselage, #UPDATE based on position of LG
        "buoy_y": None,  # m, y-location w.r.t. front of fuselage
        "buoy_z": None  # m, z-location w.r.t. front of fuselage
    }
}
component_inputs.update(components_oilspills)


other_components = {
    "gymbal_connection": {
        "gymbal_connection_name": "SKYPORT",
        "gymbal_connection_mass": 0.07,  # kg, mass of the gimbal connection
        "gymbal_connection_cost": None,  # Cost of the gimbal connection, if available
        
        "gymbal_connection_diameter": 0.05,  # m, diameter of the gimbal connection
        "gymbal_connection_height": 0.044,  # m, height of the gimbal connection
        # Positioning:
        "gymbal_connection_x": 0.08458,  # m, x-location w.r.t. front of fuselage
        "gymbal_connection_y": None,  # m, y-location w.r.t. front of fuselage
        "gymbal_connection_z": None  # m, z-location w.r.t. front of fuselage
    },
    "flight_controller": {
        "flight_controller_name": "",
        "flight_controller_mass": 0.100,  # kg, mass of the flight controller
        "flight_controller_power": 7.5,  # W, power consumption of the flight controller
        "flight_controller_voltage": 5,  # V, voltage of the flight controller
        "flight_controller_cost": None,  # Cost of the flight controller, if available
        
        "flight_controller_length": 0.0923,  # m, length of the flight controller
        "flight_controller_width": 0.0402,  # m, width of the flight controller
        "flight_controller_height": 0.02343,  # m, height of the flight controller
        # Positioning:
        "flight_controller_x": 0.95,  # m, x-location w.r.t. front of fuselage
        "flight_controller_y": None,  # m, y-location w.r.t. front of fuselage
        "flight_controller_z": None  # m, z-location w.r.t. front of fuselage
    },
    "OBC": {
        "OBC_name": "",
        "OBC_mass": 0.700,  # kg, mass of the OBC
        "OBC_power": 60,  # W, power consumption of the OBC
        "OBC_voltage": 12, # V, Voltage of the OBC
        "OBC_cost": None,  # Cost of the OBC, if available

        "OBC_length": 0.110,  # m, length of the OBC
        "OBC_width": 0.110,  # m, width of the OBC
        "OBC_height": 0.07165,  # m, height of the OBC
        # Positioning:
        "OBC_x": 0.2185,  # m, x-location w.r.t. front of fuselage
        "OBC_y": None,  # m, y-location w.r.t. front of fuselage
        "OBC_z": None  # m, z-location w.r.t. front of fuselage
    },
    "GPS": {
        "GPS_name": "",
        "GPS_mass": 0.117,  # kg, mass of the GPS
        "GPS_power": 1.25,  # W, power consumption of the GPS
        "GPS_voltage": 5,  # V, voltage of the GPS
        "GPS_cost": None,  # Cost of the GPS, if available
        
        "GPS_diameter": 0.078,  # m, diameter of the GPS
        "GPS_height": 0.022,  # m, height of the GPS
        # Positioning:
        "GPS_x": 0.3463,  # m, x-location w.r.t. front of fuselage
        "GPS_y": None,  # m, y-location w.r.t. front of fuselage
        "GPS_z": None  # m, z-location w.r.t. front of fuselage
    },
    "Mesh_network_module": {   
        "Mesh_network_module_name": "Mini Mesh Radio",
        "Mesh_network_module_mass": 0.0365,  # kg, mass of the mesh network module
        "Mesh_network_module_power": 5,  # W, power consumption of the mesh network module
        "Mesh_network_module_voltage": 5,  # V, voltage of the mesh network module
        "Mesh_network_module_cost": None,  # Cost of the mesh network module, if available
        
        "Mesh_network_module_length": 0.046,  # m, length of the mesh network module
        "Mesh_network_module_width": 0.051,  # m, width of the mesh network module
        "Mesh_network_module_height": 0.0065,  # m, height of the mesh network module
        # Positioning:
        "Mesh_network_module_x": 0.4313,  # m, x-location w.r.t. front of fuselage
        "Mesh_network_module_y": None,  # m, y-location w.r.t. front of fuselage
        "Mesh_network_module_z": None  # m, z-location w.r.t. front of fuselage
    },
    "SATCOM_module": {   # Satellite communication module
        "SATCOM_module_name": "",
        "SATCOM_module_mass": 0.036,  # kg, mass of the SATCOM module
        "SATCOM_module_power": 2.25,  # W, power consumption of the SATCOM module
        "SATCOM_module_voltage": 4,  # V, voltage of the SATCOM module
        "SATCOM_module_cost": None,  # Cost of the SATCOM module, if available
        
        "SATCOM_module_length": 0.045,  # m, length of the SATCOM module
        "SATCOM_module_width": 0.045,  # m, width of the SATCOM module
        "SATCOM_module_height": 0.017,  # m, height of the SATCOM module
        # Positioning:
        "SATCOM_module_x": 0.4313,  # m, x-location w.r.t. front of fuselage
        "SATCOM_module_y": None,  # m, y-location w.r.t. front of fuselage
        "SATCOM_module_z": None  # m, z-location w.r.t. front of fuselage
    },
    "4G_LTE_module":{
        "4G_LTE_module_name": "",
        "4G_LTE_module_mass": 0.020,  # kg, mass of the 4G-LTE module
        "4G_LTE_module_power": 5,  # W, power consumption of the 4G-LTE module, ESTIMATE not verified. 
        "4G_LTE_module_voltage": 5,  # V, voltage of the 4G-LTE module
        "4G_LTE_module_cost": None,  # Cost of the 4G-LTE module, if available
        "4G_LTE_module_length": 0.0545,  # m, length of the 4G-LTE module
        "4G_LTE_module_width": 0.0335,  # m, width of the 4G-LTE module
        "4G_LTE_module_height": 0.0135,  # m, height of the 4G-LTE module
        # Positioning:
        "4G_LTE_module_x": 0.4313,  # m, x-location w.r.t. front of fuselage
        "4G_LTE_module_y": None,  # m, y-location w.r.t. front of fuselage  
        "4G_LTE_module_z": None  # m, z-location w.r.t. front of fuselage
    },


    "PBD": {   # Power distribution board
        "PBD_name": "FLIGHTCORE MK2",
        "PDB_mass": 0.015,
        "PDB_power": None,  # W, does not consume power, but distributes it
        "PDB_cost": None,  # Cost of the PDB, if available
        "PDB_length": 0.116,
        "PDB_width": 0.11,
        "PDB_height": 0.025,
        # Positioning:
        "PDB_x": 0.06,  # m, x-location w.r.t. front of fuselage
        "PDB_y": None,  # m, y-location w.r.t. front of fuselage
        "PDB_z": None  # m, z-location w.r.t. front of fuselage
    }

}
component_inputs.update(other_components)

deployment_components = {
    "winch_motor": {
        "Winch_motor_name": "XD-10",
        "Winch_motor_mass": 1.117, # kg, mass of the winch motor
        "Winch_motor_power_operation": 100,  # W, power consumption of the winch motor during operation
        "Winch_motor_power_idle": 10,  # W, power consumption of the winch motor when not in operation
        "Winch_motor_voltage": 24,  # V, voltage of the winch motor
        "Winch_motor_cost": None,  # Cost of the winch motor, if available
        
        "Winch_motor_length": 0.17,
        "Winch_motor_width": 0.142,
        "Winch_motor_height": 0.11,
        # Positioning:
        "Winch_motor_x": 0.95,  # m, x-location w.r.t. front of fuselage
        "Winch_motor_y": None,  # m, y-location w.r.t. front of fuselage
        "Winch_motor_z": None  # m, z-location w.r.t. front of fuselage
    },
    "winch_cable": {
        "winch_cable_name": "",
        "winch_cable_mass": None,  # kg, mass of the winch cable
        "winch_cable_cost": None,  # Cost of the winch cable, if available

        "winch_cable_length": None,  # m, length of the winch cable
        "winch_cable_diameter": None,  # m, diameter of the winch cable
    },
    "aerogel": {
        "payload_mass": 5 # kg, mass of the aerogel payload 
    }
}
component_inputs.update(deployment_components)

propulsion = {
    "propeller_cruise": {
        "propeller_cruise_name": "",
        "propeller_cruise_mass": None,
        "propeller_cruise_cost": None,  # Cost of the propeller, if available

        "propeller_cruise_efficiency": None
        
    },
    "motor_cruise": {
        "motor_cruise_name": "",
        "motor_cruise_mass": None,
        "motor_cruise_power_available": None,
        "motor_cruise_cost": None,  # Cost of the motor, if available

        # Positioning:
        "motor_cruise_x": 2,  # m, x-location w.r.t. front of the fuselage
        "motor_cruise_y": None,  # m, y-location w.r.t. vertical centerline of the fuselage
        "motor_cruise_z": None  # m, z-location w.r.t. horizontal centerline of the fuselage
    },
    "propeller_VTOL": {
        "propeller_VTOL_name": "",
        "propeller_vtol_mass": None,
        "propeller_VTOL_cost": None,  # Cost of the propeller, if available

        "propeller_vtol_efficiency": None

    },
    "motor_VTOL": {
        "motor_VTOL_name": "",
        "motor_VTOL_mass": None,  # kg, mass of the VTOL
        "motor_VTOL_power_available": None,  # W, power available for VTOL
        "motor_VTOL_cost": None,  # Cost of the motor, if available

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
    "battery_name": "",
    "battery_specific_energy": 275,  # Wh/kg, specific energy of the battery
    "battery_cost": None, 
    "battery_maximum_peak_current": 100,  # A, maximum current of the battery
    
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

wing_group = {
    "aileron_actuation":{
        "aileron_actuation_mass":0.025,  # kg, mass of the aileron actuation system
        "aileron_actuation_power": None,  # W, power consumption of the aileron actuation system
        # Positioning:
        "aileron_actuation_x": 0.2,  # m, x-location w.r.t. leading edge of the wing
        "aileron_actuation_y": None,  # m, y-location w.r.t. leading edge of the wing
        "aileron_actuation_z": None,  # m, z-location w.r.t. leading edge of the wing
    },

    "wing_lights":{
        "wing_lights_mass": None,  # kg, mass of the wing lights
        "wing_lights_power": None, # W, power consumption of the wing lights
        # Positioning:
        "wing_lights_x": 0.0,  # m, x-location w.r.t. leading edge of the wing
        "wing_lights_y": None,  # m, y-location w.r.t. leading edge of the wing
        "wing_lights_z": None,  # m, z-location w.r.t. leading edge of the wing
    }

}
component_inputs.update(wing_group)

structure = {

}
component_inputs.update(structure)




components = component_inputs.copy()


nest_components = {
    "container": {
        "container_name": "ISO Container",
        "container_mass": None,
        "container_cost": None,  # Cost of the container, if available
        "container_length": None,  # m, length of the container
        "container_width": None,  # m, width of the container
        "container_height": None  # m, height of the container
    },
    
    "generator": {
        "generator_name": "CAT DE65 GC",
        "generator_mass": None,
        "generator_power": None,  # W, power output of the generator
        "generator_cost": None,  # Cost of the generator, if available
        "generator_length": None,  # m, length of the generator
        "generator_width": None,  # m, width of the generator
        "generator_height": None,  # m, height of the generator
        # Positioning:
        "generator_x": None,  # m, x-location w.r.t. front of fuselage
        "generator_y": None,  # m, y-location w.r.t. front of fuselage
        "generator_z": None  # m, z-location w.r.t. front of fuselage
    },

    "fuel_tank": {
        "fuel_tank_name": "",
        "fuel_tank_mass": None,
        "fuel_tank_capacity": None,  # L, fuel capacity of the tank
        "fuel_tank_cost": None,  # Cost of the fuel tank, if available
        "fuel_tank_length": None,  # m, length of the fuel tank
        "fuel_tank_width": None,  # m, width of the fuel tank
        "fuel_tank_height": None,  # m, height of the fuel tank
        # Positioning:
        "fuel_tank_x": None,  # m, x-location w.r.t. front of fuselage
        "fuel_tank_y": None,  # m, y-location w.r.t. front of fuselage
        "fuel_tank_z": None  # m, z-location w.r.t. front of fuselage
    },
    
}


if __name__ == '__main__':

    print("Wildfire components:")
    pprint.pprint(components_wildfires)
    print("\nOil spill components:")
    pprint.pprint(components_oilspills)
    print("\nOther components:")
    pprint.pprint(other_components)
    print("\nDeployment components:")
    pprint.pprint(deployment_components)
    print("\nPropulsion:")
    pprint.pprint(propulsion)
    print("\nBattery:")
    pprint.pprint(battery)
    print("\nWings:")
    pprint.pprint(wing_group)
    print("\nStructure:")
    pprint.pprint(structure)



