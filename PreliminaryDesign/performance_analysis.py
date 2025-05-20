from integration import inputs, integration_optimization
import matplotlib.pyplot as plt
import numpy as np
from Classes.Contraints_for_mass_calculations import Constraints
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

    plt.xlabel('Range')
    plt.ylabel('Payload mass')
    plt.title('Contour Plot of Takeoff Mass')
    plt.savefig('PreliminaryDesign\Plots\payload_range.png')
    #plt.show()

if __name__ == '__main__':
    AR_range_diagram(np.arange(6, 12),np.arange(15000, 35001, 1000), integration_optimization, inputs)
    cruise_speed_mass_diagram(np.arange(int(50/3.6), int(150/3.6), 2), inputs, integration_optimization)
    payload_range_diagram(np.arange(0, 6.5, 0.5), np.arange(15000, 35001, 1000), integration_optimization, inputs)
    
    constraint_plot = Constraints(
    inputs['V_stall'],
    inputs['V_cruise'],
    inputs["e"],
    inputs["AR"],
    inputs["CL_max"],
    inputs["CD0"],
    inputs["propeller_efficiency_cruise"],
    inputs["RC_service"]
    )

    constraint_plot.plot(save=True)


