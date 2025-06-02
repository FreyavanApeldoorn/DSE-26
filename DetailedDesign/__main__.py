from inputs import inputs
from deployment import Deployment
from mission import Mission
from uav import UAV

initial_inputs = inputs.copy()

'''
This is the file where the code actually gets executed.
'''

if __name__ == '__main__':
    
    """
    Inputs:
    - (design) perimeter
    - Requirements: 30kg MTOW, R_max = 200000
    - V_cruise
    - MF_payload
    - n_drones
    """

    inputs['mission_type'] = 'wildfire'
    # inputs['mission_type'] = 'oil_spill'

    deployment = ...

    mission = ...


    """
    Outputs:
    - Mission times
    - 

    """
    

    #uav = UAV()

    #nest = Nest()

    print(1234)