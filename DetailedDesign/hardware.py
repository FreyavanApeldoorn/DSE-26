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

    def __init__(self, inputs: dict[str, float]) -> None:
        self.inputs = inputs
        self.outputs = self.inputs.copy()

    # ~~~ Intermediate Functions ~~~

    def wildfire_components(self):
    

        hardware = {
            "wildfire_sensor": {
                "wildfire_sensor_mass": None,
                "wildfire_sensor_power": None
            },
            "propeller": {
                "propeller_diameter_VTOL": None,
                "propeller_diameter_cruise": None
            },
            "VTOL_motor": {
                "VTOL_motor_mass": None,
            }
        }


        include_components = ["wildfire_sensor", "propeller"]


        hardware_inputs = {}
        for component in include_components:
            if component in hardware:
                for key, value in hardware[component].items():
                    hardware_inputs[key] = value

        return hardware_inputs


    def oil_spill_components(self):
        pass


    def structure_components(self):

        if self.mission_type == "wildfire":
            hardware_inputs = self.wildfire_components()
        elif self.mission_type == "oil_spill":
            hardware_inputs = self.oil_spill_components()
        else:
            raise ValueError("Unsupported mission type. Please choose 'wildfire' or 'oil_spill'.")

        required_components = {
            "propeller_diameter_VTOL": None,
            "propeller_diameter_cruise": None
        }

        for key in hardware_inputs:
            if key in wildfire_inputs:
                required_components[key] = wildfire_inputs[key]

    # ~~~ Output functions ~~~ 

    def get_all(self) -> dict[str, float]:

        self.outputs["power_scan"] = 300 # W - THIS IS AN ESTIMATE, NEEDS TO BE UPDATED
        self.outputs["power_idle"] = 100 # W - THIS IS AN ESTIMATE, NEEDS TO BE UPDATED


        self.outputs["mass_propulsion"]
        self.outputs["mass_hardware"] = 5.0 # kg - THIS IS AN ESTIMATE, NEEDS TO BE UPDATED
        

        return self.outputs
    
if __name__ == '__main__': 
    # Perform sanity checks here
    ...