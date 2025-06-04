#wing section analysis
#import necessary libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Path to the .DAT file
file_path = r"C:\Users\wiets\OneDrive\Documenten\TU Delft\BEP\DSE-26\DetailedDesign\data\e1212_Lednicer.DAT"

# Read lines, skip headers
with open(file_path, 'r') as f:
    lines = f.readlines()[2:]  # Skip the first two lines

# Process coordinates
coords = []
for line in lines:
    line = line.strip()
    if line == "":
        coords.append("BREAK")  # Mark the break between upper and lower surfaces
        continue
    parts = line.split()
    if len(parts) == 2:
        coords.append((float(parts[0]), float(parts[1])))

# Split at "BREAK"
if "BREAK" in coords:
    break_index = coords.index("BREAK")
    upper = coords[:break_index]
    lower = coords[break_index + 1:]
else:
    # Fallback: Find second occurrence of (0.0, 0.0)
    zero_index = [i for i, p in enumerate(coords) if p == (0.0, 0.0)]
    if len(zero_index) > 1:
        break_index = zero_index[1]
        upper = coords[:break_index]
        lower = coords[break_index:]
    else:
        raise ValueError("Could not split upper and lower surfaces.")

# Convert to DataFrames
upper_df = pd.DataFrame(upper, columns=["x", "y"])
lower_df = pd.DataFrame(lower, columns=["x", "y"])

# Parametrize spar locations (as fraction of chord)
forward_spar = 0.25  # 25% chord
aft_spar = 0.7       # 70% chord

def get_spar_points(df, spar_x):
    """Interpolate to find y at spar_x for both upper and lower surfaces."""
    if spar_x < df["x"].min() or spar_x > df["x"].max():
        return None
    y = np.interp(spar_x, df["x"], df["y"])
    return y

# Get spar y-coordinates for plotting
spar_xs = [forward_spar, aft_spar]
spar_labels = ["Forward Spar", "Aft Spar"]
colors = ["green", "purple"]

plt.figure(figsize=(10, 4))
plt.plot(upper_df["x"], upper_df["y"], label="Upper Surface", color="blue", marker='o', markersize=4)
plt.plot(lower_df["x"], lower_df["y"], label="Lower Surface", color="red", marker='o', markersize=4)

# Plot spars

for spar_x, label, color in zip(spar_xs, spar_labels, colors):
    y_upper = get_spar_points(upper_df, spar_x)
    y_lower = get_spar_points(lower_df, spar_x)
    if y_upper is not None and y_lower is not None:
        plt.plot([spar_x, spar_x], [y_lower, y_upper], color=color, linestyle="--", linewidth=2, label=label + f" ({spar_x:.2f}c)")

plt.title("EPPLER E1212 Airfoil - Upper and Lower Surfaces with Spars")
plt.xlabel("x")
plt.ylabel("y")
plt.axis("equal")
plt.grid(True)
plt.legend()
plt.show()

combined_df = pd.concat([upper_df, lower_df[::-1]], keys=["Upper", "Lower"], ignore_index=True)

# Boom idealization of the airfoil section
x_coords = combined_df["x"].values
y_coords = combined_df["y"].values
A_boom = 2  # Area of each boom (assumed constant for simplicity)

# Total area is sum of all boom areas
total_area = A_boom * len(combined_df)
# Calculate centroid for discrete booms (points)
x_centroid = np.mean(x_coords)
y_centroid = np.mean(y_coords)

print(f"Centroid of the airfoil: ({x_centroid:.4f}, {y_centroid:.4f})")

Ixx = np.sum(A_boom * (y_coords - y_centroid) ** 2)
Iyy = np.sum(A_boom * (x_coords - x_centroid) ** 2)
Ixy = np.sum(A_boom * (x_coords - x_centroid) * (y_coords - y_centroid))

plt.figure(figsize=(10, 4))
plt.plot(combined_df["x"], combined_df["y"], marker='o', linestyle='-', color='black', label='Booms')
plt.plot(x_centroid, y_centroid, 'r*', markersize=12, label='Centroid')
plt.axis("equal")
plt.grid(True)
plt.title("Boom Idealization of Airfoil Section")
plt.xlabel("x")
plt.ylabel("y")
plt.legend()
plt.show()

# Define thicknesses (in meters, for example)
skin_thickness = 0.008  # 8 mm
spar_thickness = 0.015  # 15 mm

# 1. Skin area: perimeter * skin_thickness
# Calculate perimeter (distance along upper + lower surface)
def calc_perimeter(df):
    return np.sum(np.sqrt(np.diff(df["x"])**2 + np.diff(df["y"])**2))

perimeter = calc_perimeter(upper_df) + calc_perimeter(lower_df)
skin_area = perimeter * skin_thickness

# 2. Spar area: sum of (height * spar_thickness) for each spar
spar_areas = []
for spar_x in spar_xs:
    y_upper = get_spar_points(upper_df, spar_x)
    y_lower = get_spar_points(lower_df, spar_x)
    if y_upper is not None and y_lower is not None:
        spar_height = abs(y_upper - y_lower)
        spar_areas.append(spar_height * spar_thickness)
spar_area = sum(spar_areas)

# 3. Total area
total_structural_area = skin_area + spar_area

print(f"Skin area: {skin_area:.6f}")
print(f"Spar area: {spar_area:.6f}")
print(f"Total structural area (skin + spars): {total_structural_area:.6f}")

# Loads (replace with actual values)
N = 158           # Axial force in N
M_x = -94            # Bending moment about x-axis (N·m)
M_y = 0            # Bending moment about y-axis (N·m)

# Maximum loads hover
N_hover = 158  # Maximum axial load in hover (N)
M_x_hover = -13  # Maximum bending moment about x-axis in hover (N·m) 
q_hover = -94  # Shear force in hover (N/m)
T_hover = 2 * q_hover * total_area  # Maximum bending moment about y-axis in hover (N·m)

# Maximum loads forward flight
N_cruise = -100  # Maximum axial load in forward flight (N)
M_x_cruise = 57  # Maximum bending moment about x-axis in forward flight (N·m)
q_cruise = -76  # Shear force in forward flight (N/m)
T_cruise = 2 * q_cruise * total_area # Maximum bending moment about y-axis in forward flight (N·m)

#Maximum loads VTOL
N_vtol = 4.1  # Maximum axial load in VTOL (N)
M_x_vtol = 42  # Maximum bending moment about x-axis in VTOL (N·m)
q_vtol = 63  # Shear force in VTOL (N/m)
T_vtol = 2 * q_vtol * total_area  # Maximum bending moment about y-axis in VTOL (N·m)

# Calculate axial stress
sigma_normal = []
sigma_axial = N / total_structural_area

for x, y in zip(x_coords, y_coords):
    sigma_bending = (M_y / Ixx) * (y - y_centroid) - (M_x / Iyy) * (x - x_centroid)
    sigma_total = sigma_axial + sigma_bending
    sigma_normal.append(sigma_total)
    

# Visualization
plt.figure(figsize=(10, 4))
sc = plt.scatter(x_coords, y_coords, c=sigma_normal, cmap='coolwarm', s=50, edgecolor='k')
plt.colorbar(sc, label='Normal Stress (Pa)')
plt.plot(x_centroid, y_centroid, 'r*', markersize=12, label='Centroid')
plt.title("Normal Stress Distribution in Airfoil Section")
plt.xlabel("x")
plt.ylabel("y")
plt.axis('equal')
plt.grid(True)
plt.legend()
plt.show()

# Plot bending stress only
sigma_bending_list = []
for x, y in zip(x_coords, y_coords):
    sigma_bending = (M_y / Ixx) * (y - y_centroid) - (M_x / Iyy) * (x - x_centroid)
    sigma_bending_list.append(sigma_bending)

plt.figure(figsize=(10, 4))
sc2 = plt.scatter(x_coords, y_coords, c=sigma_bending_list, cmap='RdYlGn', s=50, edgecolor='k')
plt.colorbar(sc2, label='Bending Stress (Pa)')
plt.plot(x_centroid, y_centroid, 'r*', markersize=12, label='Centroid')
plt.title("Bending Stress Distribution in Airfoil Section")
plt.xlabel("x")
plt.ylabel("y")
plt.axis('equal')
plt.grid(True)
plt.legend()
plt.show()

# #torsion
# chord_length = np.max(x_coords) - np.min(x_coords)  # Length of the chord
# x_ac = 0.25 * chord_length  # x-coordinate of aerodynamic center (as fraction of chord)

# moment_arm = x_centroid - x_ac #moment arm for the torsional moment

# #maximum load factor in VTOL mode
# Y0 = 500 #lift generated by rotors in VTOL mode (N)
# rho_0 = 1.225  # air density at sea level (kg/m^3)  
# V_wind = 30 / 3.6  # wind speed (m/s)
# S_wing = 1.27  # wing area (m^2)
# W = 30*9.81  # weight of the UAV (N)
# c_y = 1.5 # coefficient of lift (assumed constant for simplicity)
# n_max = (Y0 + (0.5 * rho_0 * V_wind**2 * S_wing * c_y)) / (W) 
# print(f"Maximum load factor in VTOL mode: {n_max:.2f}")

# # Calculate torsional moment due to lift at aerodynamic center
# L = Y0 + (0.5 * rho_0 * V_wind**2 * S_wing * c_y)  # Total lift in VTOL mode

# # Torsional moment (torque) about the aerodynamic center
# T = L * (x_centroid - x_ac)
# print(f"Torsional moment about aerodynamic center: {T:.2f} Nm")

# --- Plot normal stress for each flight stage ---

flight_cases = [
    ("Hover", N_hover, M_x_hover, T_hover),
    ("Cruise", N_cruise, M_x_cruise, T_cruise),
    ("VTOL", N_vtol, M_x_vtol, T_vtol)
]

for case_name, N_case, M_x_case, M_y_case in flight_cases:
    sigma_normal = []
    sigma_axial = N_case / total_structural_area
    for x, y in zip(x_coords, y_coords):
        sigma_bending = (M_y_case / Ixx) * (y - y_centroid) - (M_x_case / Iyy) * (x - x_centroid)
        sigma_total = sigma_axial + sigma_bending
        sigma_normal.append(sigma_total)

    plt.figure(figsize=(10, 4))
    sc = plt.scatter(x_coords, y_coords, c=sigma_normal, cmap='coolwarm', s=50, edgecolor='k')
    plt.colorbar(sc, label='Normal Stress (Pa)')
    plt.plot(x_centroid, y_centroid, 'r*', markersize=12, label='Centroid')
    plt.title(f"Normal Stress Distribution in Airfoil Section ({case_name})")
    plt.xlabel("x")
    plt.ylabel("y")
    plt.axis('equal')
    plt.grid(True)
    plt.legend()
    plt.show()

# wing parameters
wing_loading = 217 # wing loading in N/m^2
b_wing = 3 # wing span in m
mac = 0.42 # mean aerodynamic chord in m
c_root = 0.458 # root chord in m
c_tip = 0.39 # tip chord in m
aspect_ratio = 7.1 # aspect ratio of the wing
taper_ratio = c_tip / c_root  # taper ratio of the wing

# --- Shear force and bending moment distributions for each flight stage ---

flight_cases_lift = [
    ("Hover", N_hover, q_hover),
    ("Cruise", N_cruise, q_cruise),
    ("VTOL", N_vtol, q_vtol)
]

x_span = np.linspace(0, b_wing, 100)  # spanwise locations

plt.figure(figsize=(14, 8))
for idx, (case_name, N_case, q_case) in enumerate(flight_cases_lift, 1):
    # Distributed lift per unit span for this case
    q_lift_case = q_case  # Already in N/m from your definitions

    # Calculate shear force and bending moment along the span
    shear_force = np.zeros_like(x_span)
    bending_moment = np.zeros_like(x_span)
    for i, x in enumerate(x_span):
        if x < b_wing / 2:
            shear_force[i] = q_lift_case * x
        else:
            shear_force[i] = q_lift_case * (b_wing - x)
        bending_moment[i] = np.trapz(shear_force[:i+1], x_span[:i+1])

    # Plot shear force
    plt.subplot(3, 2, 2*idx-1)
    plt.plot(x_span, shear_force, label=f'Shear Force ({case_name})', color='blue')
    plt.title(f'Shear Force Distribution - {case_name}')
    plt.xlabel('Spanwise Location (m)')
    plt.ylabel('Shear Force (N)')
    plt.grid(True)
    plt.legend()

    # Plot bending moment
    plt.subplot(3, 2, 2*idx)
    plt.plot(x_span, bending_moment, label=f'Bending Moment ({case_name})', color='orange')
    plt.title(f'Bending Moment Distribution - {case_name}')
    plt.xlabel('Spanwise Location (m)')
    plt.ylabel('Bending Moment (N·m)')
    plt.grid(True)
    plt.legend()

plt.tight_layout()
plt.show()
