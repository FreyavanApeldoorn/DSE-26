'''
This is the file for the UAV. It contains a single class.
'''

class UAV:

    def __init__(self, inputs: dict[str, float]) -> None:
        self.inputs = inputs
        self.outputs = self.inputs.copy()

    # ~~~ Intermediate Functions ~~~

    def size(self):

        #propulsion = Propulsion()
        #power = Power()
        #stab_n_con = StabnCon()
        #aero = Aero()
        #structure = Structure()
        # thermal = Thermal()

        return self.outputs

    # ~~~ Output functions ~~~ 

    def get_all(self) -> dict[str, float]:

        return self.outputs
    
if __name__ == '__main__':
    # Perform sanity checks here
    ...