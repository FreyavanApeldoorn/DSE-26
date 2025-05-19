
# Calculate battery mass
def calculate_battery_mass(E_required_Wh, DOD_fraction, eta_battery, M_to):
    

    E_battery = E_required_Wh / 3600 / (eta_battery * DOD_fraction) # convert J to Wh and consider efficiency and depth of discharge
    
    #Use formula from research paper to determine battery mass
    #a = 4.04
    #b = 139
    #c = 0.0155
    
    #discriminant = b**2 - 4 * a * (c - E_battery)

    #if discriminant < 0:
    #   raise ValueError("No real solution for the given energy input.")

    #M_battery = (-b + (discriminant)**(1/2)) / (2 * a)
    M_battery = E_battery / 240  # assume different specific energy density of 240 Wh/kg

    max_battery_frac = 0.35
    max_battery_mass = max_battery_frac * M_to # Maximum battery mass is 40% of MTOW
    battery_mass = min(M_battery, max_battery_mass)           
    return battery_mass

