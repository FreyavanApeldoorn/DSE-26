# Battery Mass Calculations

t = 0           # Duration of Mission Segment 
t_hover = 0     # Duration of hover
P = 0           # Power Required
M_to = 0        # Take-off Mass
E_spec = 0      # Specific Energy Capacity
Eta_bat = 0     # Battery Efficiency
f_usable = 0    # Usable Battery Capacity
g = 9.81        # Gravitational Acceleration


M_frac_battery = (t * P) / ( M_to * E_spec * Eta_bat * f_usable)

M_frac_battery_hover = (t_hover * g) / ( M_to * E_spec * Eta_bat * f_usable)
