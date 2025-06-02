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

    # ~~~ Intermediate Functions ~~~

    def example_function(self):
        '''
        This is an example intermediate function
        '''
        return True

    # ~~~ Output functions ~~~ 

    def get_all(self) -> dict[str, float]:

        # These are all the required outputs for this class. Plz consult the rest if removing any of them!

        outputs["Mass_structure"] = ...
        outputs["Mass_payload"] = ...   # updated mass of the payload (with an added margin to avoid exceeding the MTOW requirement)
        

        outputs["Volume_uav"] = ...

        #CG calculations:
        outputs["CG_"]

        return self.outputs
    
if __name__ == '__main__': # pragma: no cover
    # Perform sanity checks here
    ...