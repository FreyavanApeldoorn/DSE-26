'''
This is the file for the deployment subsystem. It contains a single class. Perimeter_creation takes external inputs. 
'''
import numpy as np
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from DetailedDesign.funny_inputs import funny_inputs


def compute_outer_diameter(length: float, thickness:float, internal_diameter:float) -> float:
    '''
    Archimedes spiral
    '''

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

        self.payload_mass = inputs['payload_mass']

        self.aerogel_width = inputs['aerogel_width']
        self.aerogel_thickness = inputs['aerogel_thickness']
        self.aerogel_density = inputs['aerogel_density']

        self.n_ferro_magnets = inputs['n_ferro_magnets']
        self.ferro_magnet_mass = inputs['ferro_magnet_mass']
        self.deployment_added_mass = inputs['deployment_added_mass']

        self.n_wire = inputs['n_wire']
        self.wire_length = inputs['wire_length']
        self.wire_density = inputs['wire_density']

        self.spring_mass = inputs['spring_mass']
        self.winch_mass = inputs['winch_mass']
        self.n_pulleys = inputs['n_pulleys']
        self.pulley_mass = inputs['pulley_mass']
        self.n_epms = inputs['n_epms']
        self.epm_mass = inputs['epm_mass']
        self.epm_diameter = inputs['epm_diameter']

        self.deployment_system_volume = inputs['deployment_system_volume']
        self.deployment_speed = inputs['deployment_speed']
        self.deployment_time_margin = inputs['deployment_time_margin']

        self.power_required_epm = inputs['power_required_epm']
        self.epm_duration = inputs['epm_duration']
        self.power_required_winch = inputs['power_required_winch']

        self.deployment_accuracy = inputs['deployment_accuracy']
        self.firebreak_width = inputs['firebreak_width']

        self.fuselage_size = inputs['fuselage_size']

    # ~~~ Intermediate Functions ~~~

    def aerogel_size(self) -> float:
        '''
        Aerogel dimensions and mass based on available payload mass
        '''
        aerogel_mass = self.payload_mass - self.ferro_magnet_mass*self.n_ferro_magnets - self.deployment_added_mass
        aerogel_length = aerogel_mass / (self.aerogel_width*self.aerogel_thickness*self.aerogel_density)
        aerogel_diameter = compute_outer_diameter(aerogel_length, self.aerogel_thickness, self.epm_diameter)

        return aerogel_mass, aerogel_length, aerogel_diameter
    
    def wire_mass(self) -> float:
        '''
        Wire mass
        '''
        return self.wire_length*self.wire_density

    def deployment_system_mass(self) -> float:
        '''
        Deployment system mass based on the number of wires, springs, winch, pulleys and EPMs
        '''
        return self.winch_mass + self.spring_mass*self.n_wire + self.wire_mass()*self.n_wire + self.payload_mass +self.n_pulleys*self.pulley_mass +self.n_epms*self.epm_mass
    
    def deployment_duration(self) -> float:
        '''
        Deployment duration
        '''
        return (self.wire_length / self.deployment_speed) * 2 + self.deployment_time_margin # This concerns the time that the winch is activated and using power

    def deployment_energy(self) -> tuple[float, float]:
        '''
        Total deployment power and energy required, conservative estimates
        '''
        total_deployment_power = self.power_required_epm * self.n_epms + self.power_required_winch # Conservative estimate, as usually only 2 out of 4 EPMs are powered at the same time
        total_deployment_energy =  self.power_required_winch * self.deployment_duration() + self.power_required_epm * self.n_epms * self.epm_duration # If winch is fully extended during deployment, then the deployment duration should not include the deployment time margin

        return total_deployment_power, total_deployment_energy

    def cg_change(self):
        ...

    def perimeter_creation(self, strategy: str, amt: float, verbose = False):
        '''
        
        Definitions:
            -> Lengthwise: the aerogel is deployed along its length, i.e. the long side of the aerogel is parallel to the perimeter direction
            -> Widthwise: the aerogel is deployed along its width, i.e. the short side of the aerogel is parallel to the perimeter direction
            -> Firebreak width: also the 'depth' of the firebreak, i.e. the distance between the 'fire' and 'no fire' sides of the firebreak

        Inputs:
        strategy: either 'nr_aerogels' OR 'perimeter' 
            -> nr_aerogels: the amount of aerogels is set and you maximise perimeter
            -> perimeter: perimeter length is set and you minimise the amount of aerogels
        amt: depending on the strategy
            -> nr_aerogels: the amount of aerogels available
            -> perimeter: the required perimeter length

        Outputs:
        depending on the strategy
            -> nr_aerogels: total perimeter length ('per_length') 
            -> perimeter: total aerogels needed ('nr_aerogels')
        n_layers: the number of aerogel layers needed to cover the required firebreak width

        '''
        _, aerogel_length, _ = self.aerogel_size()

        # Decide whether the aerogels will be deployed length or widthwise.

        # Lengthwise
        n_layers_l = np.ceil(((self.firebreak_width - self.aerogel_width) / (self.aerogel_width - self.deployment_accuracy)) + 1) # Number of layers needed to cover the firebreak width 
        eff_length_l = (aerogel_length - self.deployment_accuracy) / n_layers_l # Effective added perimeter length by adding one column of aerogels in the direction of the perimeter

        # Widthwise
        n_layers_w = np.ceil(((self.firebreak_width - aerogel_length) / (aerogel_length - self.deployment_accuracy)) + 1) # Number of layers needed to cover the firebreak width
        eff_length_w = (self.aerogel_width - self.deployment_accuracy) / n_layers_w # Effective added perimeter length by adding one column of aerogels in the direction of the perimeter

        if eff_length_l > eff_length_w: # This chooses the most efficient deployment direction
            initial = aerogel_length / n_layers_l
            eff_length = eff_length_l
            if verbose:
                print('The aerogel is deployed lengthwise, number of layers is: ', n_layers_l,
                      '\n effective length:', eff_length)
        else:
            initial = self.aerogel_width / n_layers_w
            eff_length = eff_length_w
            if verbose:
                print('The aerogel is deployed widthwise, number of layers is: ', n_layers_w, 
                      '\n effective length:', eff_length)

        if strategy == 'nr_aerogels':
            per_length = initial + (eff_length)*(amt - 1)
            return per_length
        elif strategy == 'perimeter':
            nr_aerogels = (amt - initial)/(eff_length) + 1
            return nr_aerogels
        else:
            print('Not a valid strategy option')
        

    # ~~~ Output functions ~~~ 

    def get_aerogel_dimensions(self) -> dict[str, float]:
        '''
        Outputs:

        aerogel mass:               The mass of the aerogel part of te payload
        aerogel length:             The length of the aerogel sheet
        aerogel diameter:           The diameter of the rolled up aerogel sheet
        '''
        outputs = self.inputs.copy()
        aerogel_mass, aerogel_length, aerogel_diameter = self.aerogel_size()
        outputs['aerogel_mass'] = aerogel_mass
        outputs['aerogel_length'] = aerogel_length
        outputs['aerogel_diameter'] = aerogel_diameter
        return outputs
    
    def get_deployment_power(self) -> dict[str, float]:
        '''
        Outputs:

        total deployment power:     The total power needed by the deployment system while in operation
        total deployment energy:    The total energy used by the deployment system
        '''
        outputs = self.inputs.copy()
        total_deployment_power, total_deployment_energy = self.deployment_energy()
        outputs['total_deployment_power'] = total_deployment_power
        outputs['total_deployment_energy'] = total_deployment_energy
        return outputs

    def get_deployment_system_mass(self) -> dict[str, float]:
        '''
        Outputs:

        deployment system mass:     The total mass of the deployment subsystem
        wire mass:                  The mass of the wires used in the deployment system
        '''
        outputs = self.inputs.copy()
        outputs['deployment_system_mass'] = self.deployment_system_mass()
        outputs['aerogel_mass'], _, _ = self.aerogel_size()
        outputs['wire_mass'] = self.wire_mass()
        return outputs
    
    def get_deployment_duration(self) -> dict[str, float]:
        '''
        Outputs:

        deployment duration:        The total duration of the deployment
        '''

        outputs = self.inputs.copy()
        outputs['deployment_duration'] = self.deployment_duration()
        return outputs

    
    def get_cg_change(self):
        ...

    def get_all(self) -> dict[str, float]:
        '''
        Outputs:

        aerogel mass:               The mass of the aerogel part of te payload
        aerogel length:             The length of the aerogel sheet
        aerogel diameter:           The diameter of the rolled up aerogel sheet

        total deployment power:     The total power needed by the deployment system while in operation
        total deployment energy:    The total energy used by the deployment system

        deployment system mass:     The total mass of the deployment subsystem
        wire mass:                  The mass of the wires used in the deployment system

        deployment duration:        The total duration of the deployment
        '''
        outputs = self.inputs.copy() 

        aerogel_mass, aerogel_length, aerogel_diameter = self.aerogel_size()
        outputs['aerogel_mass'] = aerogel_mass
        outputs['aerogel_length'] = aerogel_length
        outputs['aerogel_diameter'] = aerogel_diameter

        total_deployment_power, total_deployment_energy = self.deployment_energy()
        outputs['total_deployment_power'] = total_deployment_power
        outputs['total_deployment_energy'] = total_deployment_energy

        outputs['wire_mass'] = self.wire_mass()
        outputs['deployment_system_mass'] = self.deployment_system_mass()

        outputs['deployment_duration'] = self.deployment_duration()

        return outputs
    
    def __str__(self):
        return 'Its the deployment system!'
    
if __name__ == '__main__':
    # Perform sanity checks here
    funny_inputs['payload_mass'] = 8
    test = Deployment(funny_inputs)



    print(test.perimeter_creation('perimeter', 50, True))