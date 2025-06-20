from inputs import initial_inputs
from hardware_inputs import components

from deployment import Deployment
from hardware import Hardware
from mission import Mission
from uav import UAV
from nest import Nest
from performance import Performance

'''
This is the file where the code actually gets executed.
'''

inputs = initial_inputs.copy()

print("Initial inputs: ")
for key, value in inputs.items():
    print(f"{key}: {value}")


inputs['mission_type'] = 'wildfire'
# initial_inputs['mission_type'] = 'oil_spill'

total_iterations = 3  # Define the total number of iterations
history = False



outputs = inputs.copy()  # Initialize outputs with inputs

hardware = Hardware(inputs, components)
component = hardware.get_all()


print("\nHardware outputs:")
print(component)

for _ in range(total_iterations):

    deployment = Deployment(outputs, strategy='perimeter', amt=outputs['mission_perimeter'])
    outputs = deployment.get_all()

    # hardware = Hardware(outputs, components)
    # outputs = hardware.get_all()

    mission = Mission(outputs, verbose=False)
    outputs = mission.get_all()

    uav = UAV(outputs, component, iterations=10, history=False, verbose=False)
    outputs = uav.get_all()

    nest = Nest(outputs, components, adjust_n_uavs=False, verbose=False)
    outputs = nest.get_all()


    print(f"Iteration percentage: {(_ + 1) / total_iterations * 100:.2f}%")

    if history:
        print("History is enabled, but not implemented in this run.")

#performance = Performance(outputs, components)
#outputs = performance.get_all()


print("\nFinal outputs after sizing:")
for key, value in outputs.items():
    print(f"{key}: {value}")


if False:
    print("\nCopy-pasteable final outputs dictionary:\n")
    print("final_outputs = {")
    for key, value in outputs.items():
        print(f"    {repr(key)}: {repr(value)},")
    print("}")

print(f"Payload mass: {outputs['payload_mass']} kg")
#print(f'Deployment rate {outputs["mission_deployment_rate"]*3600} m/h')

