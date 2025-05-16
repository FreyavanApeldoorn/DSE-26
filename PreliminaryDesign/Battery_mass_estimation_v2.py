

# Step 1: Define input parameters
inputs = {
    "E_required_Wh": 1499,       # Energy required for the mission in Wh
    "DOD_fraction": 0.8,         # Fraction of battery capacity that can be used (Depth of Discharge)
    "eta_battery": 0.95,         # Battery discharge efficiency
}

# Calculate battery mass
def calculate_battery_mass(E_required_Wh, DOD_fraction, eta_battery):
    

    E_battery = E_required_Wh / (eta_battery * DOD_fraction)
    
    #Use formula from research paper to determine battery mass
    a = 4.04
    b = 139
    c = 0.0155
    
    discriminant = b**2 - 4 * a * (c - E_battery)

    if discriminant < 0:
        raise ValueError("No real solution for the given energy input.")

    M_battery = (-b + (discriminant)**(1/2)) / (2 * a)
    return M_battery

