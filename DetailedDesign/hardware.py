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

    def example_function(self):
        '''
        This is an example intermediate function
        '''
        return True

    # ~~~ Output functions ~~~ 

    def get_all(self) -> dict[str, float]:

        self.outputs["power_scan"] = 300 # W - THIS IS AN ESTIMATE, NEEDS TO BE UPDATED
        self.outputs["power_idle"] = 100 # W - THIS IS AN ESTIMATE, NEEDS TO BE UPDATED

        self.outputs["mass_hardware"] = 5.0 # kg - THIS IS AN ESTIMATE, NEEDS TO BE UPDATED
        

        return self.outputs
    
if __name__ == '__main__': 
    # Perform sanity checks here
    ...