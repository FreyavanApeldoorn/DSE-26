'''
This is the file for the Structures subsystem. It contains a single class.
'''

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

import numpy as np

class Structures:

    def __init__(self, inputs: dict[str, float]) -> None:
        self.inputs = inputs
        self.outputs = self.inputs.copy()

        self.M_to = inputs["M_to"]

        self.mass_payload = inputs["payload_mass"]
        self.mass_hardware = inputs["mass_hardware"]
        self.mass_battery = inputs["mass_battery"]
        self.mass_propulsion = inputs["mass_propulsion"]
        
        self.wing_span = inputs["wing_span"]
                

    # ~~~ Intermediate Functions ~~~

    def example_function(self):
        '''
        This is an example intermediate function
        '''
        return True
    


    
    def total_mass(self) -> float:

        self.mass_structure = 10 # kg - THIS IS AN ESTIMATE, NEEDS TO BE UPDATED
        
        masses_nopay = np.array([self.mass_hardware, self.mass_battery, self.mass_propulsion, self.mass_structure])
        mass_nopay = np.sum(masses_nopay)

        self.leftover_for_payload = self.M_to - mass_nopay

    # ~~~ Output functions ~~~ 

    def get_all(self) -> dict[str, float]:

        # These are all the required outputs for this class. Plz consult the rest if removing any of them!
        
        self.total_mass()

        self.outputs["payload_mass"] = self.leftover_for_payload   # updated mass of the payload (with an added margin to avoid exceeding the MTOW requirement)
        self.outputs['mass_structure'] = self.mass_structure # kg

        #self.outputs["Volume_uav"] = ...

        #CG calculations:
        #self.outputs["CG"] = ...

        return self.outputs
    
if __name__ == '__main__': # pragma: no cover
    # Perform sanity checks here
    ...