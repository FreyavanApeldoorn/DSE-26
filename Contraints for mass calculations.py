import matplotlib.pyplot as plt
import numpy as np 


# Constants 
rho = 0.9013  # density at 3000m 
V_cruise = 27.77  # [m/s] cruise velocity 100km/hr
q = 0.5 * rho * V_cruise **2 # dynamic pressure 
CD0 = 0.040 + 0.2 # parasite drag + drag from rounded cylinder 
e = 0.85 # oswald efficiency factor 
AR = 4 # Aspect ratio of wing 
k =  1/ (np.pi * e * AR)
n_p = 0.85 
R_C = 3 # [m/s] rate of climb 
Vstall = 30 # stall speed [m/s]
CLmax = 5

def powerLoading(T_W, np, V): 
    P_W = T_W * V / np 
    return P_W 

def thrustLoadingCruise(W_S) : 
    T_W_cruise = q * CD0 * (W_S)**(-1) + k * 1/q  * W_S 
    return T_W_cruise 

def Vroc (W_S) : 
    Vroc = np.sqrt(2/rho * W_S * np.sqrt(k/(3*CD0)))
    return Vroc

def thrustLoadingClimb(Vroc, W_S) : 
    T_W_climb = R_C / Vroc + q/W_S * CD0 + k/q * W_S
    return T_W_climb

def WingLoading_Vstall() : 
    W_S_stall = 0.5 * Vstall **2 * rho * CLmax 
    return W_S_stall 


W_S = np.arrange(10,300,1) # [N/m^2] variable 

T_W_cruise = [] 
T_W_climb = [] 
P_W_cruise = [] 
P_W_climb = [] 
W_S_stall = [] 
T_W_service = [] # where mac rc is 0.5 m/s 

for i in W_S : 
    # calculating thrust to weight ratios 
    T_W_cruise = T_W_cruise.append(thrustLoadingCruise(i))  
    T_W_climb = T_W_climb.append(thrustLoadingClimb(Vros(i),i))
    T_W_service = T_W_climb.append(thrustLoadingClimb(Vroc,i))
    # calculating  


plt.plot()


