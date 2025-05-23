'''
This is the file for the deployment subsystem. It contains a single class.
'''

import numpy as np

def compute_outer_diameter(length, thickness, internal_diameter):
    a = internal_diameter / 2
    b = thickness / (2 * np.pi)
    def arc_length(theta):
        r = a + b * theta
        return np.sqrt(r**2 + b**2)
    
    s = 0
    theta = 0
    dtheta = 0.01

    while s < length:
        s += arc_length(theta) * dtheta
        theta += dtheta

    r_final = a + b * theta
    outer_diameter = 2 * r_final
    return outer_diameter

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

        self.deployment_system_volume = inputs['deployment_system_volume']
        self.deployment_speed = inputs['deployment_speed']

        self.power_required_epm = inputs['power_required_epm']
        self.epm_duration = inputs['epm_duration']
        self.power_required_winch = inputs['power_required_winch']

        self.cg_change_deployment = inputs['cg_change_deployment']
        self.deployment_accuracy = inputs['deployment_accuracy']

        self.fuselage_size = inputs['fuselage_size']

    # ~~~ Intermediate Functions ~~~

    def determine_aerogel_size(self):
        '''
        This is an example intermediate function
        '''
        aerogel_mass = self.payload_mass - self.ferro_magnet_mass*self.n_ferro_magnets - self.deployment_added_mass
        aerogel_length = self.aerogel_mass / (self.aerogel_width*self.aerogel_thickness)
        aerogel_diameter = compute_outer_diameter(self.aerogel_length, self.aerogel_thickness, self.epm_diameter)

        return aerogel_mass, aerogel_length, aerogel_diameter
    
    def determine_wire_mass(self):
        return self.wire_length*self.wire_density

    def determine_deployment_system_mass(self):
        return self.winch_mass + self.spring_mass*self.n_wire + self.wire_mass*self.n_wire + self.payload_mass +self.n_pulleys*self.pulley_mass +self.n_epms*self.epm_mass

    def determine_deployment_energy(self):
        ...

    def determine_cg_change(self):
        ...

    # ~~~ Output functions ~~~ 

    def get_aerogel_dimensions():
        return True
    
    def get_deployment_system_dimensions():
        return True
    
    def get_cg_change():
        ...

    def get_all(self) -> dict[str, float]:

        return self.outputs
    
if __name__ == '__main__':
    # Perform sanity checks here
    ...