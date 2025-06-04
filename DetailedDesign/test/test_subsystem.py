'''
This is the subsystem test file. This will test the subsystem classes  
'''
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from DetailedDesign.deployment import Deployment

from test_inputs import test_inputs, deployment_test_inputs

def test_Aerodynamics():
    assert 1==1

def test_Deployment():
    # Verified using a hand calculation

    dep = Deployment(deployment_test_inputs, 'n_aerogels', 5)
    res = dep.get_all()

    # Sanity checks

    assert res['aerogel_mass'] < res['payload_mass']
    assert res['aerogel_length'] > 0


    assert {'aerogel_mass': 3., 
            'aerogel_length': 4., 
            'aerogel_diameter': 0.15959254850813723, 
            'total_deployment_power': 180.0, 
            'total_deployment_energy': 13640.0, 
            'deployment_system_mass': 7.26, 
            'deployment_duration': 130.0}.items() <= res.items()

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