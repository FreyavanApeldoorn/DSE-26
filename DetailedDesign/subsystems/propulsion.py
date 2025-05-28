'''
This is the file for the propulsion and power subsystem. It contains a single class.
'''

class Propulsion:

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

        inputs["Power_required_VTOL"] = ...
        inputs["Power_required_cruise"] = ...
        inputs["Power_required_hover"] = ...
    
        inputs["Power_available_VTOL"] = ...
        inputs["Power_available_cruise"] = ...

        inputs["Propeller_diameter_VTOL"] = ...
        inputs["Propeller_diameter_cruise"] = ...
        
        inputs["Propulsion_system_mass"] = ...
        inputs["Motor_mass_VTOL"] = ...
        inputs["Motor_mass_cruise"] = ...
        inputs["Propeller_mass_VTOL"] = ...
        inputs["Propeller_mass_cruise"] = ...

        return self.outputs
    
if __name__ == '__main__':
    # Perform sanity checks here
    ...