
import numpy as np
import matplotlib.pyplot as plt

rho = 1.225  # kg/m^3, density of air at sea level

S_wing = 2.5  # m^2, wing area

C_D = 0.05  

#===== Preliminary Design of a Wing ==========#

v_cruise = 70

P_a = 1100 # given from P_FW

v = np.linspace(0, 100, 100)  # m/s

P_r = 0.5 * rho * v**3 * S_wing * C_D

# Find the point just before P_r crosses P_a using np.where
indices = np.where(P_r > P_a)[0]
if len(indices) > 0:
    critical_index = indices[0] - 1
    v_critical = v[critical_index]
    P_critical = P_r[critical_index]

    print(f"Velocity just before P_r crosses P_a: {v_critical} m/s or {v_critical * 3.6:.1f} km/h")
    print(f"Power required at this velocity: {P_critical} W")
else:
    print("P_r does not cross P_a within the given range.")


# Plotting the power required for different velocities

plt.figure(figsize=(10, 6))
plt.axhline(y=P_a, color='red', linestyle='--', label='Available Power (P_a)')
plt.plot(v, P_r, label='Power Required', color='blue')
plt.scatter(v_critical, P_critical, color='green', label=f'Critical Point ({v_critical:.1f} m/s, {P_critical:.1f} W)', zorder=5)
plt.title('Power Required vs Velocity')
plt.xlabel('Velocity (m/s)')
plt.ylabel('Power Required (W)')
plt.grid()
plt.legend()
plt.xlim(0, 100)
plt.ylim(0, 5000)
plt.show()
