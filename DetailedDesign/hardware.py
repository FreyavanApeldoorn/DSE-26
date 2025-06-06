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

    # ~~~ Intermediate Functions ~~~

    # def select_components(self):

    #     hardware_inputs = {}
    #     for component in self.include_components:
    #         if component in self.hardware:
    #             for key, value in self.hardware[component].items():
    #                 hardware_inputs[key] = value

    #     return hardware_inputs


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
        



    # ~~~ Output functions ~~~ 

    def get_all(self) -> dict[str, float]:

        #self.outputs = self.select_components()

        self.outputs["power_scan"] = 100 # 
        self.outputs["power_deploy"] = 100 # PLACEHOLDER
        self.outputs["power_idle"] = 100 # 

        self.outputs["mass_hardware"] = self.calculate_mass_hardware()   # kg, mass of hardware components (excluding payload, propulsion, structure, etc)
        

        return self.outputs
    
if __name__ == '__main__': 
    # Perform sanity checks here
    
    from uav_inputs import components

    inputs = {}

    hardware = Hardware(inputs, components, include_components=True)
    outputs = hardware.get_all()
    for key, value in outputs.items():
        print(f"{key}: {value}")
