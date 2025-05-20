from integration import inputs, integration_optimization
import matplotlib.pyplot as plt
import numpy as np
from Classes.Contraints_for_mass_calculations import Constraints
from mission_profile import SwarmProfile, UAVProfile
# ~~~ AR, Range diagram ~~~

def AR_range_diagram(AR_range: list, range_range: list, mass_calculation: callable, inputs: dict):
    mass_range = []
    grid = []
    for AR in AR_range:
        for r in range_range:
            current_inputs = inputs.copy()
            current_inputs['R_max'] = r
            current_inputs['AR'] = AR

            res = mass_calculation(1, 100, current_inputs)
            mass_range.append(res['M_to'])
            grid.append((AR, r))
            print((AR, r, res['M_to']))


    AR_vals = sorted(set([pt[0] for pt in grid]))
    range_vals = sorted(set([pt[1] for pt in grid]))

    Z = np.array(mass_range).reshape(len(AR_vals), len(range_vals))
    X, Y = np.meshgrid(range_vals, AR_vals)  # X: range, Y: AR

    plt.figure(figsize=(8, 6))
    cp = plt.contourf(X, Y, Z, cmap='plasma')
    plt.colorbar(cp, label='Takeoff Mass (M_to)')
    plt.vlines(30000, AR_range[0], AR_range[-1], label="Required Range", color="red")

    plt.xlabel('Range')
    plt.ylabel('Aspect Ratio (AR)')
    plt.title('Contour Plot of Takeoff Mass')
    plt.savefig('PreliminaryDesign\Plots\AR_range.png')
    #plt.show()

def cruise_speed_mass_diagram(V_range, inputs, mass_function):
    mass_results = []
    for V in V_range:
        current_inputs = inputs.copy()
        current_inputs['V_cruise'] = V
        current_inputs['V_stall'] = 0.5 * V

        res = mass_function(1, 100, current_inputs)
        mass_results.append(res['M_to'])
        print(V, res['M_to'])

    plt.figure(figsize=(10, 6))
    plt.plot(V_range, mass_results, label='Takeoff Mass vs Cruise Speed', color='blue')
    plt.xlabel('Cruise Speed (m/s)')
    plt.ylabel('Takeoff Mass (kg)')
    plt.title('Takeoff Mass vs Cruise Speed')
    plt.grid(True)
    plt.legend()
    plt.savefig('PreliminaryDesign\Plots\cruise_mass.png')
    #plt.show()

def payload_range_diagram(payload_range: list, range_range: list, mass_calculation: callable, inputs: dict):
    mass_range = []
    grid = []
    for p in payload_range:
        for r in range_range:
            current_inputs = inputs.copy()
            current_inputs['R_max'] = r
            current_inputs['M_payload'] = p

            res = mass_calculation(1, 100, current_inputs)
            mass_range.append(res['M_to'])
            grid.append((p, r))
            print((p, r, res['M_to']))


    p_vals = sorted(set([pt[0] for pt in grid]))
    range_vals = sorted(set([pt[1] for pt in grid]))

    Z = np.array(mass_range).reshape(len(p_vals), len(range_vals))
    X, Y = np.meshgrid(range_vals, p_vals)  # X: range, Y: AR

    plt.figure(figsize=(8, 6))
    cp = plt.contourf(X, Y, Z, cmap='plasma')
    plt.colorbar(cp, label='Takeoff Mass (M_to)')
    plt.vlines(30000, payload_range[0], payload_range[-1], label="Required Range", color="red")
    plt.hlines(5, range_range[0], range_range[-1], color='red', label='Required Payload')

    plt.xlabel('Range')
    plt.ylabel('Payload mass')
    plt.title('Contour Plot of Takeoff Mass')
    plt.savefig('PreliminaryDesign\Plots\payload_range.png')
    #plt.show()

def swarm_deployment_plot(V_range, l_range, inputs):
    '''
    Deployment rate as a function of V_cruise and aerogel length
    '''
    grid = []
    res = []
    for V in V_range:
        for l in l_range:
            current_inputs = inputs.copy()
            current_inputs['aerogel_length'] = l
            current_inputs['V_cruise'] = V

            current_UAV = UAVProfile(current_inputs)

            current_inputs = current_UAV.size_uav_profile()

            current_swarm = SwarmProfile(current_inputs)

            current_swarm.mission_performance()

            grid.append((V, l))
            res.append(current_swarm.deployment_rate*60*60)

    V_vals = sorted(set([pt[0] for pt in grid]))
    l_vals = sorted(set([pt[1] for pt in grid]))

    Z = np.array(res).reshape(len(V_vals), len(l_vals))
    X, Y = np.meshgrid(l_vals, V_vals)  # X: range, Y: AR

    plt.figure(figsize=(8, 6))
    cp = plt.contourf(X, Y, Z, cmap='plasma')
    plt.colorbar(cp, label='Deployment Rate')

    plt.xlabel('Aerogel Length [m]')
    plt.ylabel('Cruise speed [m/s]')
    plt.title('Contour Plot of Deployment rate [m/h]')
    plt.savefig('PreliminaryDesign\Plots\swarm_deployment.png')





if __name__ == '__main__':
    # AR_range_diagram(np.arange(6, 13),np.arange(15000, 35001, 1000), integration_optimization, inputs)
    # cruise_speed_mass_diagram(np.arange(int(50/3.6), int(150/3.6), 2), inputs, integration_optimization)
    # payload_range_diagram(np.arange(0, 6.5, 0.5), np.arange(15000, 35001, 1000), integration_optimization, inputs)
    
    swarm_deployment_plot(np.arange(int(60/3.6), int(150/3.6), 5), np.arange(0, 6, 0.5), inputs)


