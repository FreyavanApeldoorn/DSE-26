import numpy as np
import pandas as pd

# ~~~ Battery Sizing ~~~
# paramters for battery sizing
W = 30 * 9.81  # maximum takeoff weight [N]
rho = 0.9093  # density at 3000m [kg/m^3]
rho_sea = 1.225  # density at sea level [kg/m^3]
b = 10.0  # wingspan [m]
S = 0.5  # wing area [m^2]
eta_total = 0.8  # total battery efficiency [-]
V = 24 # battery voltage [V]
battery_energy_density = 250  # battery density [Wh/kg]
e = 0.7  # Oswald efficiency factor [-]
A = b^2 / S  # aspect ratio [-]
k = 1/ (np.pi * A * e) #induced drag coefficient [-]
