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