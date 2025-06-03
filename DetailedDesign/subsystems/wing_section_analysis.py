# #wing section analysis

# import pandas as pd
# import matplotlib
# import matplotlib.pyplot as plt

# # Read the CSV file (update the path if needed)
# csv_path = r"C:\Users\wiets\OneDrive\Documenten\TU Delft\BEP\DSE-26\DetailedDesign\data\e1212_Lednicer.DAT"
# data = pd.read_csv(csv_path, skiprows=2, header=None, names=['x', 'y'], delim_whitespace=True)

# plt.figure(figsize=(10, 4))
# plt.plot(data['x'], data['y'], marker='o')
# plt.title('Airfoil Shape from e1212 Lednicer Data')
# plt.xlabel('x')
# plt.ylabel('y')
# plt.axis('equal')
# plt.grid(True)
# plt.show()


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

# Plot
plt.figure(figsize=(10, 4))
plt.plot(upper_df["x"], upper_df["y"], label="Upper Surface", color="blue")
plt.plot(lower_df["x"], lower_df["y"], label="Lower Surface", color="red")
plt.title("EPPLER E1212 Airfoil - Upper and Lower Surfaces")
plt.xlabel("x")
plt.ylabel("y")
plt.axis("equal")
plt.grid(True)
plt.legend()
plt.show()
