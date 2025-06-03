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

    def sensors(self):
    
        self.wildfire_sensor = {
            "name": "Wildfire Sensor",
            "mass": 0.1,  # kg - THIS IS AN ESTIMATE, NEEDS TO BE UPDATED
            "power": 0.5,  # W - THIS IS AN ESTIMATE, NEEDS TO BE UPDATED
            "length": 0.2,  # m - THIS IS AN ESTIMATE, NEEDS TO BE UPDATED
            "width": 0.1,  # m - THIS IS AN ESTIMATE, NEEDS TO BE UPDATED
            "height": 0.05,  # m - THIS IS AN ESTIMATE, NEEDS TO BE UPDATED
        }

        self.oil_sensor = {
            "name": "Oil Sensor",
            "mass": 0.2,  # kg - THIS IS AN ESTIMATE, NEEDS TO BE UPDATED
            "power": 0.3,  # W - THIS IS AN ESTIMATE, NEEDS TO BE UPDATED
            "length": 0.15,  # m - THIS IS AN ESTIMATE, NEEDS TO BE UPDATED
            "width": 0.1,  # m - THIS IS AN ESTIMATE, NEEDS TO BE UPDATED
            "height": 0.05,  # m - THIS IS AN ESTIMATE, NEEDS TO BE UPDATED
        }

    # ~~~ Output functions ~~~ 

    def get_all(self) -> dict[str, float]:

        self.outputs["power_scan"] = 300 # W - THIS IS AN ESTIMATE, NEEDS TO BE UPDATED
        self.outputs["power_idle"] = 100 # W - THIS IS AN ESTIMATE, NEEDS TO BE UPDATED

        self.outputs["mass_hardware"] = 5.0 # kg - THIS IS AN ESTIMATE, NEEDS TO BE UPDATED
        

        return self.outputs
    
if __name__ == '__main__': 
    # Perform sanity checks here
    ...