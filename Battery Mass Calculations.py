# Battery Mass Calculations

t = 0           # Duration of Mission Segment 
t_hover = 0     # Duration of hover
t_loiter = 0    # Duration of loiter (horizontal flying)
P = 0           # Power Required
M_to = 0        # Take-off Mass
E_spec = 0      # Specific Energy Capacity
Eta_bat = 0     # Battery Efficiency
f_usable = 0    # Usable Battery Capacity
g = 9.81        # Gravitational Acceleration
Eta_electric = 0    # Efficiency of electric system
T = 0           # Thrust
DL = 0          # Disc Loading
rho = 0         # Air Density
R = 0           # Range
LD_max = 0      # Maximum Lift-over-drag ratio
CL = 0          # Coefficient of Lift
CD = 0          # Coefficient of Drag
WS = 0          # Wing Loading



FM = 0.4742*T**(0.0793)          # Rotor Efficiency

M_frac_battery = (t * P) / ( M_to * E_spec * Eta_bat * f_usable)

M_frac_battery_hover = ((t_hover * g) / ( E_spec * FM * Eta_electric * Eta_bat * f_usable))*(DL/(2*rho))**0.5

M_frac_max_range = (R * g) / ( E_spec * Eta_electric * Eta_bat * f_usable * LD_max)

M_frac_max_endu = ((t_loiter * g) / ( E_spec * Eta_electric * Eta_bat * f_usable * ((CL**(3/2)) / CD)))*(2*WS/rho)**0.5

# M_frac_total = Sum of battery fractions for all mission segments