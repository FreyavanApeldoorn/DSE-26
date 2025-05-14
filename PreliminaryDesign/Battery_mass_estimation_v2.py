# Step 1: Define input parameters
inputs = {
    "E_required_Wh": 1499,       # Energy required for the mission in Wh
    "DOD_fraction": 0.8,         # Fraction of battery capacity that can be used (Depth of Discharge)
    "eta_battery": 0.95,         # Battery discharge efficiency
}

# Calculate battery mass
def calculate_battery_mass(inputs):
    E_required_Wh = inputs["E_required_Wh"]
    DOD_fraction = inputs["DOD_fraction"]
    eta_battery = inputs["eta_battery"]

    E_battery = E_required_Wh / (eta_battery * DOD_fraction)
    battery_mass = (E_battery + 0.0422) / 138.18 #statistical relation based on research paper for battery sizing

    return battery_mass

print("Battery mass (kg):", calculate_battery_mass(inputs))
