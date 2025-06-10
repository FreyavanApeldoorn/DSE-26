#landing gear sizing
import numpy as np

# buckling
MTOW = 30 #kg
n = 2 # load factor
F = n*MTOW*9.81/4 # force on each strut

L = 0.28 # [m] length of the strut
r = 0.012 # m, radius of the strut

A = np.pi * r**2 # cross-sectional area of the strut

# material properties - carbon fibre
E = 70e9 # Pa, Young's modulus for carbon fibre
I = np.pi*r**4/8
sigma_ult = 570e6 #Pa, ultimate compressive strength for carbon fibre




F_buck = np.pi*E*I/L**2

sigma = F/A

print('force on each strut:', F)
print('compression stress:',sigma)
print('buckling force:',F_buck)