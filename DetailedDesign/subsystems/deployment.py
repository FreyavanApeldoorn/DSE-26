'''
This is the file for the deployment subsystem. It contains a single class.
'''

class Deployment:

    def __init__(self, inputs: dict[str, float]) -> None:
        self.aerogel_mass = ...
        self.aerogel_width = ...
        self.aerogel_thickness = ...
        self.aerogel_length = ...

        self.wire_length = ...
        self.wire_mass = ... 

        self.deployment_system_mass = ...
        self.deployment_system_volume = ...
        self.power_required_deployment = ...

        self.cg_change_deployment = ...
        self.deployment_accuracy = ...

        self.fuselage_size = ...

    # ~~~ Intermediate Functions ~~~

    def example_function(self):
        '''
        This is an example intermediate function
        '''
        return True

    # ~~~ Output functions ~~~ 

    def get_aerogel_dimensions():
        return True
    
    def get_deployment_system_dimensions():
        return True

    def get_all(self) -> dict[str, float]:

        updated_inputs = True
        return updated_inputs
    
if __name__ == '__main__':
    # Perform sanity checks here
    ...