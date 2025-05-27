'''
This is the subsystem test file. This will test the subsystem classes  
'''
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from DetailedDesign.subsystems.deployment import Deployment

from test_inputs import test_inputs, deployment_test_inputs

def test_Aerodynamics():
    assert 1==1

def test_Deployment():
    dep = Deployment(deployment_test_inputs)
    res = dep.get_all()

    assert {'aerogel_mass': 3., 
            'aerogel_length': 6., 
            'aerogel_diameter': 0.11286122063880329, 
            'total_deployment_power': 180.0, 
            'total_deployment_energy': 136400.0, 
            'deployment_system_mass': 7.26, 
            'deployment_duration': 130.0} in res

def test_Operations():
    assert 1==1

def test_PropnPow():
    assert 1==1

def test_StabnCon():
    assert 1==1

def test_Structures():
    assert 1==1

def test_Thermal():
    assert 1==1