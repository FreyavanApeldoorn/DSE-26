'''
This is the file for the propulsion and power subsystem. It contains a single class.
'''

class Power:

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

        inputs["Battery_mass"] = ...
        inputs["Battery_volume"] = ...
        inputs["Battery_capacity"] = ...

        return self.outputs
    
if __name__ == '__main__':
    # Perform sanity checks here
    ...