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

    def __init__(self, hardware: dict[str, float], include_components) -> None:
        self.hardware = hardware
        self.include_components = include_components

    # ~~~ Intermediate Functions ~~~

    def wildfire_components(self, include_components=None):
        pass

    def oil_spill_components(self):
        pass


    def select_components(self):

        hardware_inputs = {}
        for component in self.include_components:
            if component in hardware:
                for key, value in hardware[component].items():
                    hardware_inputs[key] = value

        return hardware_inputs



    # ~~~ Output functions ~~~ 

    def get_all(self) -> dict[str, float]:

        hardware_inputs = self.structure_components()
        

        return self.outputs
    
if __name__ == '__main__': 
    # Perform sanity checks here
    ...