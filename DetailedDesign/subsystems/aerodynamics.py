'''
This is the file for the aerodynamics subsystem. It contains a single class.
'''

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

import numpy as np

class Aerodynamics:

    def __init__(self, inputs: dict[str, float]) -> None:
        self.inputs = inputs
        self.outputs = self.inputs.copy()

        self.mtow = inputs["MTOW"]

        self.wing_loading = inputs["wing_loading"]
        self.wing_aspect_ratio = inputs["AR"]



    # ~~~ Intermediate Functions ~~~
    
    
    def wing_3D(self) -> float:
        
        self.wing_span = self.mtow / self.wing_loading
        self.wing_area = self.wing_span**2 / self.wing_aspect_ratio
        

    # ~~~ Output functions ~~~ 

    def get_all(self) -> dict[str, float]:

        # These are all the required outputs for this class. Plz consult the rest if removing any of them!

        self.wing_3D()

        #self.outputs["CL_cruise"] = ...
        #self.outputs["CD_cruise"] = ...
        #self.outputs["CL_max"] = ...
        #self.outputs["CD_max"] = ...

        self.outputs["wing_area"] = self.wing_area
        self.outputs["wing_span"] = self.wing_span
        #self.outputs["wing_aspect_ratio"] = ...
        #self.outputs["wing_taper_ratio"] = ...
        #self.outputs["wing_chord"] = ...
        #outputs["Wing_sweep"] = ...

        # potentially something about coefficients for control 
        # something about aerodynamic force during deployment for control



        return self.outputs
    
if __name__ == '__main__': # pragma: no cover
    # Perform sanity checks here
    ...