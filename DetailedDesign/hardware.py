'''
This is the file for the operations subsystem. It contains a single class.
'''

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

import numpy as np

class Hardware:

    """
    
    hardware:
    - 
    
    """

    def __init__(self, inputs, hardware: dict[str, float]) -> None:
        self.hardware = hardware
        self.outputs = inputs.copy()
        #self.include_components = include_components

        self.hardware_components = [
            "wildfire_camera",
            "oil_spill_camera",
            "buoy",
            "gymbal_connection",
            "flight_controller",
            "OBC",
            "GPS",
            "Mesh_network_module",
            "SATCOM_module",
            "PBD"
        ]

        self.wildfire_sensor_power = self.hardware["wildfire_camera"]["wildfire_sensor_power"]
        self.wildfire_sensor_voltage = self.hardware["wildfire_camera"]["wildfire_sensor_voltage"]
        self.oil_spill_sensor_power = self.hardware["oil_spill_camera"]["oil_sensor_power"]  # W, power consumption of the wildfire sensor
        self.oil_spill_sensor_voltage = self.hardware["oil_spill_camera"]["oil_sensor_voltage"]
        self.GPS_power = self.hardware["GPS"]["GPS_power"]
        self.GPS_voltage = self.hardware["GPS"]["GPS_voltage"]
        self.flight_controller_power = self.hardware["flight_controller"]["flight_controller_power"]
        self.flight_controller_voltage = self.hardware["flight_controller"]["flight_controller_voltage"]
        self.Mesh_network_module_power = self.hardware["Mesh_network_module"]["Mesh_network_module_power"]
        self.Mesh_network_module_voltage = self.hardware["Mesh_network_module"]["Mesh_network_module_voltage"]
        self.SATCOM_module_power = self.hardware["SATCOM_module"]["SATCOM_module_power"]
        self.SATCOM_module_voltage = self.hardware["SATCOM_module"]["SATCOM_module_voltage"]
        self.OBC_power = self.hardware["OBC"]["OBC_power"]
        self.OBC_voltage = self.hardware["OBC"]["OBC_voltage"]
        self.winch_motor_power_operation = self.hardware["winch_motor"]["Winch_motor_power_operation"]  # W, power consumption of the winch motor
        self.winch_motor_power_idle = self.hardware["winch_motor"]["Winch_motor_power_idle"]  # W, power consumption of the winch motor in idle state
        self.winch_motor_voltage = self.hardware["winch_motor"]["Winch_motor_voltage"]  # V, voltage of the winch motor
        self.battery_maximum_peak_current = self.hardware["battery_maximum_peak_current"]  # A, maximum peak current of the battery
        self.LTE_module_power = self.hardware["4G_LTE_module"]["4G_LTE_module_power"] 
        self.LTE_module_voltage = self.hardware["4G_LTE_module"]["4G_LTE_module_voltage"]
    # ~~~ Intermediate Functions ~~~

    # def select_components(self):

    #     hardware_inputs = {}
    #     for component in self.include_components:
    #         if component in self.hardware:
    #             for key, value in self.hardware[component].items():
    #                 hardware_inputs[key] = value

    #     return hardware_inputs

    def add_component_to_inputs(self):

        def flatten_and_add(d):
            for key, value in d.items():
                if isinstance(value, dict):
                    flatten_and_add(value)
                else:
                    self.outputs[key] = value
    
        for comp in self.hardware:
            value = self.hardware[comp]
            if isinstance(value, dict):
                flatten_and_add(value)
            else:
                self.outputs[comp] = value
    
        return self.outputs


    def calculate_mass_hardware(self) -> float:
        """
        Calculates the total mass of the selected hardware components.
        Sums all values in self.outputs whose keys end with '_mass' and are not None.
        """
        total_mass = 0.0
        for comp in self.hardware_components:
            comp_dict = self.hardware.get(comp, {})
            if isinstance(comp_dict, dict):
                for key, value in comp_dict.items():
                    if key.endswith("_mass") and value is not None:
                        total_mass += value
                    else:
                        print(f"Warning: {key} in {comp} does not end with '_mass' or is None. Skipping this component.")
        return total_mass
    
    def calculate_power_hardware(self) -> float:

        total_power = 0.0
        for comp in self.hardware_components:
            comp_dict = self.hardware.get(comp, {})
            if isinstance(comp_dict, dict):
                for key, value in comp_dict.items():
                    if key.endswith("_power") and value is not None:
                        total_power += value
                    else: 
                        print(f"Warning: {key} in {comp} does not end with '_power' or is None. Skipping this component.")
        return total_power
    
    def calculate_power_hardware_during_scan(self) -> float:
        """
        Calculates the total power consumption of the hardware components during the scan phase.

        """
        power_hardware_scan = (
            self.wildfire_sensor_power + 
            self.GPS_power + 
            self.flight_controller_power + 
            self.Mesh_network_module_power + 
            self.SATCOM_module_power + 
            self.LTE_module_power +
            self.OBC_power 
        ) 
        total_amperage_scan = (
            self.wildfire_sensor_power / self.wildfire_sensor_voltage + 
            self.GPS_power / self.GPS_voltage+ 
            self.flight_controller_power / self.flight_controller_voltage + 
            self.Mesh_network_module_power / self.Mesh_network_module_voltage + 
            self.SATCOM_module_power / self.SATCOM_module_voltage + 
            self.LTE_module_power / self.LTE_module_voltage +
            self.winch_motor_power_idle / self.winch_motor_voltage +
            self.OBC_power / self.OBC_voltage
        )
        # Check if the battery can handle the total amperage during the scan phase
        if total_amperage_scan > self.battery_maximum_peak_current:
            print(f"Total amperage during scan phase exceeds battery limit A")

        else:
            print(f"Total amperage during scan phase is within battery limit: {total_amperage_scan} A")

        return power_hardware_scan
    
    def calculate_power_hardware_during_deploy(self) -> float:
        """
        Calculates the total power consumption of the hardware components during the deploy phase.
        """

        power_hardware_deploy = ( 
            self.wildfire_sensor_power + 
            self.GPS_power + 
            self.flight_controller_power + 
            self.Mesh_network_module_power + 
            self.SATCOM_module_power + 
            self.OBC_power + 
            self.winch_motor_power_operation 
            
        )
        total_amperage_deploy = (
            self.wildfire_sensor_power / self.wildfire_sensor_voltage + 
            self.GPS_power / self.GPS_voltage + 
            self.flight_controller_power / self.flight_controller_voltage + 
            self.Mesh_network_module_power / self.Mesh_network_module_voltage + 
            self.SATCOM_module_power / self.SATCOM_module_voltage + 
            self.OBC_power / self.OBC_voltage + 
            self.winch_motor_power_operation / self.winch_motor_voltage
        )
        # Check if the battery can handle the total amperage during the deploy phase
        if total_amperage_deploy > self.battery_maximum_peak_current:
            print(f"Total amperage during deploy phase exceeds battery limit A")
        else:
            print(f"Total amperage during deploy phase is within battery limit: {total_amperage_deploy} A")
        
        return power_hardware_deploy
    
    def calculate_power_hardware_cruise(self) -> float:
        """
        Calculates the total power consumption of the hardware components during the cruise phase.
        """
        power_hardware_cruise = (
        self.GPS_power + 
        self.flight_controller_power + 
        self.Mesh_network_module_power + 
        self.SATCOM_module_power + 
        self.OBC_power +
        self.LTE_module_power +
        self.winch_motor_power_idle + 
        10 * 12 + # servo motors running at 12V and 2.4 A
        30/52  # camera for sensing
        )
        total_amperage_cruise = (
            self.GPS_power / self.GPS_voltage + 
            self.flight_controller_power / self.flight_controller_voltage + 
            self.Mesh_network_module_power / self.Mesh_network_module_voltage + 
            self.SATCOM_module_power / self.SATCOM_module_voltage + 
            self.OBC_power / self.OBC_voltage + 
            self.LTE_module_power / self.LTE_module_voltage +
            self.winch_motor_power_idle / self.winch_motor_voltage + 
            2.4 
        )
        # Check if the battery can handle the total amperage during the cruise phase
        if total_amperage_cruise > self.battery_maximum_peak_current:
            print(f"Total amperage during cruise phase exceeds battery limit A")
        else:
            print(f"Total amperage during cruise phase is within battery limit: {total_amperage_cruise} A")
        
        return power_hardware_cruise
    
    def calculate_power_hardware_cruise_return(self) -> float:
        """
        Calculates the total power consumption of the hardware components during the cruise phase for return to base."""
        
        power_hardware_cruise_return = (
            self.GPS_power + 
            self.flight_controller_power + 
            self.Mesh_network_module_power + 
            self.SATCOM_module_power + 
            self.OBC_power +
            self.LTE_module_power 
            
        )  # No winch motor on the return to base

        return power_hardware_cruise_return
    
          


    # ~~~ Output functions ~~~ 

    def get_all(self) -> dict[str, float]:


        self.outputs = self.add_component_to_inputs()

        #self.outputs = self.select_components()

        self.outputs["power_scan"] = self.calculate_power_hardware_during_scan()  # W, power consumption of the hardware during the scan phase
        self.outputs["power_deploy"] = self.calculate_power_hardware_during_deploy()
        #self.outputs["power_idle"] =   # W, power consumption of the hardware during the cruise phase
        self.outputs["power_cruise_hardware"] = self.calculate_power_hardware_cruise()  # W, power consumption of the hardware during the cruise phase
        self.outputs["mass_hardware"] = self.calculate_mass_hardware()   # kg, mass of hardware components (excluding payload, propulsion, structure, etc)
        

        return self.outputs
    
if __name__ == '__main__': 
    # Perform sanity checks here
    
    from hardware_inputs import components

    inputs = {}

    hardware = Hardware(inputs, components)
    outputs = hardware.get_all()
    for key, value in outputs.items():
        print(f"{key}: {value}")


