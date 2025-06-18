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
        "propeller_cruise_name": "G26*8.5 inch",
        "propeller_cruise_mass": 68,
        "propeller_cruise_cost": None,  # Cost of the propeller, if available
        "propeller_cruise_diameter": 0.66,  # m, diameter of the propeller
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
    #"battery_name": "",
    "battery_specific_energy": 275,  # Wh/kg, specific energy of the battery
    "battery_cost": None, 
    "battery_maximum_peak_current": 17*2*3,  # A, maximum current of the battery, 3C continious discharge rate
    "battery_capacity": 17*2,  # Ah, capacity of the battery
    "battery_voltage": 52,  # V, voltage of the battery
    "battery_DOD_fraction": 0.8,  # Depth of discharge fraction of the battery
    
    "battery_mass": 3.619*2,  # kg, mass of the battery
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


nest_components = {
    "container": {
        "container_name": "ISO Container",
        "container_tare_mass": 2250,  # kg, tare mass of the container
        "container_max_payload": 28350,  # kg, maximum payload of the container
        "container_cost": 5200,  # € Cost of the container

        "container_length": 5.90,  # m, inner length of the container
        "container_width": 2.35,  # m, inner width of the container
        "container_height": 2.39,  # m, inner height of the container
        "container_door_height": 2.28,  # m, height of the container door
        "container_door_width": 2.335  # m, width of the container door    
    },
    "ventilation_system": {
        "ventilation_system_name": "VEVOR Exhaust Fan",
        "ventilation_system_mass": 3.66,  # kg
        "ventilation_system_power": 40,  # W
        "ventilation_system_cost": 99.99,  # €

        "ventilation_system_length": 0.380,  # m
        "ventilation_system_width": 0.380,  # m
        "ventilation_system_height": 0.190,  # m
        "ventilation_system_x": None,
        "ventilation_system_y": None,
        "ventilation_system_z": None
    },
    "heating_system": {
        "heating_system_name": "Dyna-Glo 4800W Heater",
        "heating_system_mass": 13 * 0.453592,  # kg
        "heating_system_power": 4800,  # W
        "heating_system_cost": 230,  # $

        "heating_system_length": 0.267,  # m
        "heating_system_width": 0.245,  # m
        "heating_system_height": 0.281,  # m

        "heating_system_x": None,
        "heating_system_y": None,
        "heating_system_z": None
    },
    "thermal_sensor": {
        "thermal_sensor_name": "TEMPer1F USB Temperature Sensor",
        "thermal_sensor_mass": 0.015,  # kg
        "thermal_sensor_power": 0.1,  # W
        "thermal_sensor_cost": 10,  # $

        "thermal_sensor_length": 0.025,  # m
        "thermal_sensor_width": 0.025,  # m
        "thermal_sensor_height": 0.025,  # m

        "thermal_sensor_x": None,
        "thermal_sensor_y": None,
        "thermal_sensor_z": None
    },
    "battery_charger": {
        "battery_charger_name": "Tattu TA1000",
        "battery_charger_mass": 1.7,  # kg
        "battery_charger_power": 500,  # W
        "battery_charger_cost": 260,  # $

        "battery_charger_length": 0.186,  # m
        "battery_charger_width": 0.174,  # m
        "battery_charger_height": 0.095,  # m
        "battery_charger_x": None,
        "battery_charger_y": None,
        "battery_charger_z": None
    },
    "generator": {
        "generator_name": "GENPOWERUSA GPR-J50-60T4iF-002",
        "generator_mass": 1514,  # kg
        "generator_fuel_tank": 662,  # L
        
        "generator_power_output": 60000,  # W
        "generator_power_factor": 0.8,
        "generator_efficiency": 0.3,
        
        "generator_cost": 53500,  # $
        "generator_length": 2.440,  # m
        "generator_width": 0.971,  # m
        "generator_height": 1.856,  # m
        "generator_x": None,
        "generator_y": None,
        "generator_z": None
    },
    "PDU": {
        "PDU_name": "Tripp Lite PDUMH15ATNET",
        "PDU_mass": 4.99,  # kg
        "PDU_power_capacity": 1440,  # W
        "PDU_cost": 183,  # €

        "PDU_length": 0.4445,  # m
        "PDU_width": 0.1143,  # m
        "PDU_height": 0.0445,  # m
        "PDU_x": None,
        "PDU_y": None,
        "PDU_z": None
    },
    "UPS": {
        "UPS_name": "APC Smart-UPS C 1500VA",
        "UPS_mass": 24.09,  # kg
        "UPS_power": 900,  # W output
        "UPS_cost": 820,  # $

        "UPS_length": 0.439,  # m
        "UPS_width": 0.171,  # m
        "UPS_height": 0.219,  # m
        "UPS_x": None,
        "UPS_y": None,
        "UPS_z": None
    },
    "computer": {
        "computer_name": "Lambda Scalar MGX AMD",
        "computer_mass": 30.6,  # kg
        "computer_power": 8000,  # W
        "computer_cost": 103749,  # $

        "computer_length": 0.737,  # m
        "computer_width": 0.437,  # m
        "computer_height": 0.2225,  # m
        "computer_x": None,
        "computer_y": None,
        "computer_z": None
    },
    "switch": {
        "switch_name": "UniFi Switch 8 150W",
        "switch_mass": 1.7,  # kg
        "switch_power": 150,  # W max
        "switch_cost": 199,  # $

        "switch_length": 0.204,  # m
        "switch_width": 0.235,  # m
        "switch_height": 0.043,  # m
        "switch_x": None,
        "switch_y": None,
        "switch_z": None
    },
    "firewall": {
        "firewall_name": "MikroTik CCR1009-7G-1C-1S+",
        "firewall_mass": 4.54,  # kg
        "firewall_power": 39,  # W
        "firewall_cost": 495,  # $

        "firewall_length": 0.443,  # m
        "firewall_width": 0.175,  # m
        "firewall_height": 0.044,  # m
        "firewall_x": None,
        "firewall_y": None,
        "firewall_z": None
    },
    "RF_antenna": {
        "RF_antenna_name": "OmniLOG® PRO H",
        "RF_antenna_mass": 0.6,  # kg
        "RF_antenna_power": 100,  # W
        "RF_antenna_cost": 398,  # €

        "RF_antenna_length": 0.084,  # m
        "RF_antenna_width": 0.084,  # m
        "RF_antenna_height": 0.096,  # m
        "RF_antenna_x": None,
        "RF_antenna_y": None,
        "RF_antenna_z": None
    },
    "mesh_base": {
        "mesh_base_name": "Doodle Labs EK-2450-11N3",
        "mesh_base_mass": 0.026,  # kg
        "mesh_base_power": 8,  # W peak
        "mesh_base_cost": 207.50,  # $

        "mesh_base_length": 0.047,  # m
        "mesh_base_width": 0.028,  # m
        "mesh_base_height": 0.0065,  # m
        "mesh_base_x": None,
        "mesh_base_y": None,
        "mesh_base_z": None
    },
    "4G_antenna": {
        "4G_antenna_name": "Panorama B4BE",
        "4G_antenna_mass": 0.39,  # kg
        "4G_antenna_power": 30,  # W
        "4G_antenna_cost": 45.91,  # €

        "4G_antenna_length": 0.048,  # m
        "4G_antenna_width": 0.048,  # m
        "4G_antenna_height": 0.164,  # m
        "4G_antenna_x": None,
        "4G_antenna_y": None,
        "4G_antenna_z": None
    },
    "router": {
        "router_name": "TELTONIKA RUTX11",
        "router_mass": 0.456,  # kg
        "router_power": 16,  # W
        "router_cost": 350.00,  # €

        "router_length": 0.115,  # m
        "router_width": 0.095,  # m
        "router_height": 0.044,  # m

        "router_x": None,
        "router_y": None,
        "router_z": None
    },
    "Satellite_antenna": {
        "Satellite_antenna_name": "Selfsat H30D",
        "Satellite_antenna_mass": 1.1,  # kg
        "Satellite_antenna_power": 2.85,  # W
        "Satellite_antenna_cost": 94,  # €

        "Satellite_antenna_length": 0.547,  # m
        "Satellite_antenna_width": 0.277,  # m
        "Satellite_antenna_height": 0.058,  # m
        "Satellite_antenna_x": None,
        "Satellite_antenna_y": None,
        "Satellite_antenna_z": None
    },
    "Satellite_modem": {
        "Cobham_EXPLORER_323_name": "Cobham EXPLORER 323",
        "Cobham_EXPLORER_323_mass": 3.5,  # kg
        "Cobham_EXPLORER_323_power": 35,  # W
        "Cobham_EXPLORER_323_cost": 3800,  # €
        "Cobham_EXPLORER_323_length": 0.321,  # m (diameter)
        "Cobham_EXPLORER_323_width": 0.321,   # m (diameter)
        "Cobham_EXPLORER_323_height": 0.097,  # m
        "Cobham_EXPLORER_323_x": None,
        "Cobham_EXPLORER_323_y": None,
        "Cobham_EXPLORER_323_z": None
    },
    "cables": {
        "cables_name": "RF & Coax Cables",
        "cables_mass": 0.1,  # kg total
        "cables_length": None,  # varied
        "cables_cost": 125,  # $
        "cables_x": None,
        "cables_y": None,
        "cables_z": None
    },
    "rails": {
        "rails_name": "ISO Container Rails",
        "rails_mass": 14.9,  # kg, mass of the rails
        "rails_cost": 160,  # $ Cost of the rails

        "rails_length": 2.2,  # m, length of the rails
        "rails_width": 0.02,  # m, width of the rails
        "rails_height": 0.02,  # m, height of the rails

        "rails_x": None,  # m, x-location w.r.t. front of the container
        "rails_y": None,  # m, y-location w.r.t. front of the container
        "rails_z": None  # m, z-location w.r.t. front of the container

    }
}
component_inputs.update(nest_components)

components = component_inputs.copy()


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



