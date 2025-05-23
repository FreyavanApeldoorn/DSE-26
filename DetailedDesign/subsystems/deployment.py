'''
This is the file for the deployment subsystem. It contains a single class.
'''

class Deployment:
    '''
    The deployment class contains the aerogel sizing and the deployment subsystem sizing. 
    '''

    def __init__(self, inputs: dict[str, float]) -> None:
        self.inputs = inputs
        self.outputs = self.inputs.copy()

        self.payload_mass = inputs['payload_mass']

        self.aerogel_mass = inputs['aerogel_mass']
        self.aerogel_width = inputs['aerogel_width']
        self.aerogel_thickness = inputs['aerogel_thickness']
        self.aerogel_length = ...
        self.aerogel_density = inputs['aerogel_density']

        self.n_ferro_magnets = inputs['n_ferro_magnets']
        self.ferro_magnet_mass = inputs['ferro_magnet_mass']
        self.deployment_added_mass = inputs['deployment_added_mass']

        self.n_wire = inputs['n_wire']
        self.wire_length = inputs['wire_length']
        self.wire_density = inputs['wire_density']
        self.wire_mass = inputs['wire_mass']

        self.spring_mass = inputs['spring_mass']
        self.winch_mass = inputs['winch_mass']
        self.n_pulleys = inputs['n_pulleys']
        self.pulley_mass = inputs['pulley_mass']
        self.n_epms = inputs['n_epms']
        self.epm_mass = inputs['epm_mass']
        self.epm_diameter = inputs['epm_diameter']

        self.deployment_system_mass = inputs['deployment_system_mass']
        self.deployment_system_volume = inputs['deployment_system_volume']
        self.power_required_deployment = inputs['power_required_deployment']
        self.deployment_speed = inputs['deployment_speed']

        self.cg_change_deployment = inputs['cg_change_deployment']
        self.deployment_accuracy = inputs['deployment_accuracy']

        self.fuselage_size = inputs['fuselage_size']

    # ~~~ Intermediate Functions ~~~

    def determine_aerogel_size(self):
        '''
        This is an example intermediate function
        '''
        return True
    
    def determine_wire_mass(self):
        ...

    def determine_deployment_system_mass(self):
        ...

    

    # ~~~ Output functions ~~~ 

    def get_aerogel_dimensions():
        return True
    
    def get_deployment_system_dimensions():
        return True

    def get_all(self) -> dict[str, float]:

        return self.outputs
    
if __name__ == '__main__':
    # Perform sanity checks here
    ...