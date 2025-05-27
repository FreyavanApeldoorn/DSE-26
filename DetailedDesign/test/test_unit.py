'''
This is the unit test file, these only test small parts of the code, like individual functions. 
'''

import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from DetailedDesign.subsystems.deployment import Deployment

from test_inputs import test_inputs, deployment_test_inputs
from DetailedDesign.funny_inputs import deployment_funny_inputs

def test_Deployment_perimeter_creation():
    dep = Deployment(deployment_funny_inputs)
    
    dep.payload_mass = (dep.firebreak_width*dep.aerogel_width*dep.aerogel_thickness) * dep.aerogel_density + dep.n_ferro_magnets * dep.ferro_magnet_mass + dep.deployment_added_mass

    assert dep.perimeter_creation('nr_aerogels', 5, test = True) == ('w', 5.5)
    assert dep.perimeter_creation('perimeter', 6, test = True) == ('w', 6)

    dep.payload_mass = (2*dep.firebreak_width*dep.aerogel_width*dep.aerogel_thickness) * dep.aerogel_density + dep.n_ferro_magnets * dep.ferro_magnet_mass + dep.deployment_added_mass

    assert dep.perimeter_creation('nr_aerogels', 5, test = True) == ('l', 6)
    assert dep.perimeter_creation('perimeter', 6, test = True) == ('l', 3)