#wing section analysis

import pandas as pd
import matplotlib
import matplotlib.pyplot as plt

# Read the CSV file (update the path if needed)
csv_path = r"C:\Users\wiets\OneDrive\Documenten\TU Delft\BEP\DSE-26\DetailedDesign\data\e1212_Lednicer.DAT"
data = pd.read_csv(csv_path, skiprows=2, header=None, names=['x', 'y'], delim_whitespace=True)

plt.figure(figsize=(10, 4))
plt.plot(data['x'], data['y'], marker='o')
plt.title('Airfoil Shape from e1212 Lednicer Data')
plt.xlabel('x')
plt.ylabel('y')
plt.axis('equal')
plt.grid(True)
plt.show()
