'''
This is the unit test file, these only test small parts of the code, like individual functions. 
'''

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

import math 
from DetailedDesign.subsystems.deployment import Deployment
from DetailedDesign.subsystems.propulsion import Propulsion


from test_inputs import test_inputs, deployment_test_inputs
from DetailedDesign.funny_inputs import deployment_funny_inputs
from DetailedDesign.funny_inputs import funny_inputs


def test_Deployment_perimeter_creation():
    dep = Deployment(deployment_funny_inputs)
    
    dep.payload_mass = (dep.firebreak_width*dep.aerogel_width*dep.aerogel_thickness) * dep.aerogel_density + dep.n_ferro_magnets * dep.ferro_magnet_mass + dep.deployment_added_mass

    assert dep.perimeter_creation('nr_aerogels', 5, test = True) == ('w', 5.5)
    assert dep.perimeter_creation('perimeter', 6, test = True) == ('w', 6)

    dep.payload_mass = (2*dep.firebreak_width*dep.aerogel_width*dep.aerogel_thickness) * dep.aerogel_density + dep.n_ferro_magnets * dep.ferro_magnet_mass + dep.deployment_added_mass

    assert dep.perimeter_creation('nr_aerogels', 5, test = True) == ('l', 6)
    assert dep.perimeter_creation('perimeter', 6, test = True) == ('l', 3)


def test_thrust_to_weight_vtol(): 
    prop = Propulsion(funny_inputs)
    T_W = prop.thrust_to_weight_vtol()
    T_W_actual = 1.2  # typical t_W ratios for VTOLS

    assert (T_W_actual - T_W_actual*0.2 < T_W < T_W_actual + T_W_actual * 0.2)

def test_power_required_vtol(): 
    prop = Propulsion(funny_inputs)
    Pr_vtol , S_prop, prop_disk_loading, total_thrust = prop.power_required_vtol()
    Pr_vtol_actual = funny_inputs['mtow'] * funny_inputs['vtol_roc']
    assert  Pr_vtol_actual - Pr_vtol_actual*0.2 < Pr_vtol 

def test_power_required_cruise(): 
    prop = Propulsion(funny_inputs)
    optimal_cruise_power, D_cruise = prop.power_required_cruise()
    optimal_cruise_power_actual = ... 
    D_cruise_actual = ... 

    assert math.isclose()
    
def test_power_required_hover(): 
    ... 