'''
This is the file for the UAV. It contains a single class.
'''

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))


from subsystems.propulsion import Constraints
from subsystems.propulsion import Propulsion
from subsystems.power import Power
from subsystems.stab_n_con import StabCon
from subsystems.aerodynamics import Aerodynamics
from subsystems.structures import Structures
#from subsystems.thermal import Thermal


class UAV:

    def __init__(self, inputs: dict[str, float], hardware: dict[str, float], iterations: int, history: bool = False, verbose : bool = False) -> None:
        self.inputs = inputs
        self.outputs = self.inputs.copy()
        self.hardware = hardware
        self.iterations = iterations
        self.verbose = verbose
    

        self.history = history
        if self.history:
            self.history_data = self.outputs.copy()
    
    # ~~~ Intermediate Functions ~~~

    def size(self):

        for _ in range(self.iterations):
            
            outputs = self.inputs.copy()

            constraints = Constraints(outputs, self.hardware)
            outputs = constraints.get_all()
            
            propulsion = Propulsion(outputs, self.hardware)
            outputs = propulsion.get_all()

            power = Power(outputs, self.hardware)
            outputs = power.get_all()

            #stab_n_con = StabnCon()
            
            # aerodynamics = Aerodynamics(outputs, self.hardware)
            # outputs = aerodynamics.get_all()

            # structures = Structures(outputs, self.hardware)
            # outputs = structures.get_all()

            #thermal = Thermal(outputs)
            #outputs = thermal.get_all()

            if self.history:
                self.history_data.update(outputs)  

        # performance = Performance(outputs) # - potentially add the final performance metrics here
        # outputs = structures.get_all()

        if self.verbose:
            print("UAV sizing completed after", self.iterations, "iterations.")

        return outputs

    # ~~~ Output functions ~~~ 

    def get_all(self) -> dict[str, float]:

        self.outputs = self.size()

        return self.outputs
    
if __name__ == '__main__':
    # Perform sanity checks here
    from inputs import initial_inputs
    inputs = initial_inputs.copy()

    uav = UAV(inputs, iterations=10)
    outputs = uav.size()

    for key, value in outputs.items():
        print(f"{key}: {value}")


    