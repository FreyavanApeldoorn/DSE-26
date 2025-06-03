#wing section analysis

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

# Example loads (replace with your actual values)
N = 294.3      # Axial force in N
M_x = 70        # Bending moment about x-axis (N·m)
M_y = 50     # Bending moment about y-axis (N·m)

# Calculate normal stress at each boom (point)
sigma_normal = []
for x, y in zip(x_coords, y_coords):
    sigma_axial = N / total_structural_area
    sigma_bending = (M_y / Ixx) * (y - y_centroid) - (M_x / Iyy) * (x - x_centroid)
    sigma_total = sigma_axial + sigma_bending
    sigma_normal.append(sigma_total)

# Plot normal stress distribution
plt.figure(figsize=(10, 4))
sc = plt.scatter(x_coords, y_coords, c=sigma_normal, cmap='coolwarm', s=40)
plt.colorbar(sc, label='Normal Stress (Pa)')
plt.plot(x_centroid, y_centroid, 'r*', markersize=12, label='Centroid')
plt.axis("equal")
plt.grid(True)
plt.title("Normal Stress Distribution in Airfoil Section")
plt.xlabel("x")
plt.ylabel("y")
plt.legend()
plt.show()

# Calculate enclosed area using the shoelace formula (polygon area)
def polygon_area(x, y):
    return 0.5 * np.abs(np.dot(x, np.roll(y, 1)) - np.dot(y, np.roll(x, 1)))

enclosed_area = polygon_area(combined_df["x"].values, combined_df["y"].values)

# Example torsional moment (Nm)
T = 100  # Replace with your actual torque

# Shear flow in the skin (Bredt-Batho theory)
if enclosed_area > 0:
    shear_flow = T / (2 * enclosed_area)
    max_shear_stress = shear_flow / skin_thickness
    print(f"Torsional moment (T): {T:.2f} Nm")
    print(f"Enclosed area (A_m): {enclosed_area:.6f} m^2")
    print(f"Shear flow (q): {shear_flow:.2f} N/m")
    print(f"Maximum shear stress in skin: {max_shear_stress:.2f} Pa")
else:
    print("Enclosed area is zero, cannot compute torsional response.")