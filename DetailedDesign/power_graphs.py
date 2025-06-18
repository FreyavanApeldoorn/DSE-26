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

import matplotlib.pyplot as plt

uav_counts = list(range(20, 68))
power_requirements = []

# Calculate power required with 0 UAVs (no charging)
temp_outputs_zero = outputs.copy()
temp_outputs_zero['number_of_UAVs'] = 0
nest_zero = Nest(temp_outputs_zero, components, adjust_n_uavs=False, verbose=False)
temp_outputs_zero = nest_zero.get_all()
power_no_uavs = temp_outputs_zero.get("total_nest_power_required", 0) / 1000  # Convert to kW

for n_uavs in uav_counts:
    temp_outputs = outputs.copy()
    temp_outputs['number_of_UAVs'] = n_uavs

    # Re-run the nest sizing with the new number of UAVs
    nest = Nest(temp_outputs, components, adjust_n_uavs=False, verbose=False)
    temp_outputs = nest.get_all()

    power_requirements.append(temp_outputs.get("total_nest_power_required", 0) / 1000)  # Convert to kW

plt.figure(figsize=(8, 5))
plt.plot(uav_counts, power_requirements, marker='o', label='Total Nest Power Required')
plt.axhline(48, color='r', linestyle='--', label='48 kW Cutoff')
plt.axhline(power_no_uavs, color='g', linestyle='-.', label=f'No UAV Charging ({power_no_uavs:.1f} kW)')
plt.xlabel('Number of UAVs')
plt.ylabel('Total Nest Power Required (kW)')
plt.title('Number of UAVs vs. Total Nest Power Required')
plt.xlim(10, 80)
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()


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

