#wing section analysis

import pandas as pd
import matplotlib.pyplot as plt

# Read the CSV file (update the path if needed)
csv_path = r"C:\Users\wiets\OneDrive\Documenten\TU Delft\BEP\DSE-26\DetailedDesign\data\elevator_effectiveness.csv"
data = pd.read_csv(csv_path, header=None, names=['x', 'y'])

# Assuming the CSV has columns 'x' and 'y'
plt.figure(figsize=(10, 4))
plt.plot(data['x'], data['y'], marker='o')
plt.title('Airfoil Shape from elevator_effectiveness.csv')
plt.xlabel('x')
plt.ylabel('y')
plt.axis('equal')
plt.grid(True)
plt.show()
