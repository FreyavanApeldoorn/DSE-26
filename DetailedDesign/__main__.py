from inputs import initial_inputs
from deployment import Deployment
from mission import Mission
from uav import UAV
from nest import Nest

'''
This is the file where the code actually gets executed.
'''

inputs = initial_inputs.copy()

print("Initial inputs: ")
for key, value in inputs.items():
    print(f"{key}: {value}")


total_iterations = 10  # Define the total number of iterations
history = False

for _ in range(total_iterations):

    inputs['mission_type'] = 'wildfire'
    # initial_inputs['mission_type'] = 'oil_spill'

    outputs = inputs.copy()

    deployment = Deployment(outputs, strategy='perimeter', amt=outputs['mission_perimeter'])
    outputs = deployment.get_all()

    mission = Mission(outputs, verbose=False)
    outputs = mission.get_all()

    uav = UAV(outputs, iterations=10, history=False, verbose=False)
    outputs = uav.get_all()

    #nest = Nest(outputs)
    #outputs = nest.get_all()

    if history:
        print("History is enabled, but not implemented in this run.")

print("\nFinal outputs after sizing:")
for key, value in outputs.items():
    print(f"{key}: {value}")

print(f'Deployment rate {outputs["true_deployment_rate"]*3600} m/h')

