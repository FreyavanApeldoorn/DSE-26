'''
This is the file for the thermal subsystem. It contains a single class.
'''

class Costs:

    def __init__(self, inputs: dict[str, float], hardware) -> None:
        self.inputs = inputs
        self.outputs = self.inputs.copy()
        self.hardware = hardware

    # ~~~ Intermediate Functions ~~~

    def cost_breakdown(self):
        '''
        This is an example intermediate function
        '''
        

    # ~~~ Output functions ~~~ 

    def get_all(self) -> dict[str, float]:

        return self.outputs
    
if __name__ == '__main__':
    # Perform sanity checks here
    ...