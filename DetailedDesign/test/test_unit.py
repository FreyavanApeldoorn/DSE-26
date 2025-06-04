'''
This is the unit test file, these only test small parts of the code, like individual functions. 
'''

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

import math 
from DetailedDesign.deployment import Deployment
from DetailedDesign.subsystems.propulsion import Propulsion
from DetailedDesign.subsystems.constraints import Constraints
from DetailedDesign.subsystems.structures import Structures


from test_inputs import test_inputs, deployment_test_inputs

# Turn on visual inspection if you want to show the plots, off otherwise
visual_inspection = True

def test_Deployment_perimeter_creation():
    dep = Deployment(deployment_test_inputs, 'nr_aerogels', 5)
    
    dep.payload_mass = (dep.firebreak_width*dep.aerogel_width*dep.aerogel_thickness) * dep.aerogel_density + dep.n_ferro_magnets * dep.ferro_magnet_mass + dep.deployment_added_mass

    assert dep.perimeter_creation('nr_aerogels', 5, test = True) == ('w', 5.5)
    assert dep.perimeter_creation('perimeter', 6, test = True) == ('w', 6)

    dep.payload_mass = (2*dep.firebreak_width*dep.aerogel_width*dep.aerogel_thickness) * dep.aerogel_density + dep.n_ferro_magnets * dep.ferro_magnet_mass + dep.deployment_added_mass

    assert dep.perimeter_creation('nr_aerogels', 5, test = True) == ('l', 6)
    assert dep.perimeter_creation('perimeter', 6, test = True) == ('l', 3)

def test_deployment_get_functions():
    dep = Deployment(test_inputs)

    assert isinstance(dep.get_aerogel_dimensions(), dict)
    assert isinstance(dep.get_deployment_duration(), dict)
    assert isinstance(dep.get_deployment_power(), dict)
    assert isinstance(dep.get_deployment_system_mass(), dict)

def test_constraints_get_function():
    con = Constraints(test_inputs)

    assert isinstance(con.get_all(), dict)


def test_thrust_to_weight_vtol(): 
    prop = Propulsion(test_inputs)
    T_W = prop.thrust_to_weight_vtol()
    T_W_actual = 1.2                       # https://medcraveonline.com/AAOAJ/AAOAJ-02-00047.pdf page 166

    assert math.isclose(T_W, T_W_actual, rel_tol=0.5)

def test_power_required_vtol(): 
    prop = Propulsion(test_inputs)
    Pr_vtol , _, _, _ = prop.power_required_vtol()
    Pr_vtol_actual = test_inputs['mtow'] * test_inputs['vtol_roc']
    assert  math.isclose(Pr_vtol, Pr_vtol_actual, rel_tol=1000)

def test_power_required_cruise(): 
    prop = Propulsion(test_inputs)
    optimal_cruise_power, D_cruise = prop.power_required_cruise()
    optimal_cruise_power_actual = 2000       # https://www.ijert.org/design-and-analysis-of-a-vtol-fixed-wing-uav?
    D_cruise_actual = 0.45                   # https://www.ijert.org/design-and-analysis-of-a-vtol-fixed-wing-uav?

    assert math.isclose(optimal_cruise_power, optimal_cruise_power_actual, rel_tol=500)
    assert math.isclose(D_cruise, D_cruise_actual, rel_tol=0.5)
    
def test_power_required_hover(): 
    P_req_hover = Propulsion(test_inputs).power_required_hover()
    P_req_hover_actual = 5000                # https://www.ijert.org/design-and-analysis-of-a-vtol-fixed-wing-uav?
    assert math.isclose(P_req_hover, P_req_hover_actual, rel_tol=1000)

def test_get_all_prop():
    res = Propulsion(test_inputs).get_all()
    assert isinstance(res, dict)

def test_NVM_diagrams():
    s = Structures(test_inputs)

    if visual_inspection:
        s.NVM_VTOL()
        s.NVM_cruise()
        s.NVM_propeller_boom()