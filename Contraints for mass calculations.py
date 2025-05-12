import matplotlib.pyplot as plt
import numpy as np 


# Constants 
rho = 0.9013  # density at 3000m 
V_cruise = 27.77  # [m/s] cruise velocity 100km/hr
q = 0.5 * rho * V_cruise **2 # dynamic pressure 
CD0 = 0.040 + 0.2 # parasite drag + drag from rounded cylinder 
e = 0.7 #7 oswald efficiency factor  ESTIMATION 
AR = 10.03 # Aspect ratio of wing        ESTIMATION
k =  1/ (np.pi * e * AR)
n_p = 0.85 
R_C = 3 # [m/s] rate of climb        ESTIMATION
Vstall = 13.8 # stall speed [m/s]      ESTIMATION
R_C_service = 0.5 #[m/s]
CLmax = 1.34  #                         ESTIMATION

def powerLoading(T_W, V): 
    P_W = T_W * V / n_p 
    return P_W 

def thrustLoadingCruise(W_S) : 
    T_W_cruise = q * CD0 * 1/(W_S) + k * 1/q  * W_S 
    return T_W_cruise 

def Vroc (W_S) : 
    Vroc = np.sqrt(2/rho * W_S * np.sqrt(k/(3*CD0)))
    return Vroc

def thrustLoadingClimb(Vroc, W_S, R_C) : 
    T_W_climb = R_C / Vroc + q/W_S * CD0 + k/q * W_S
    return T_W_climb

def WingLoading_Vstall() : 
    W_S_stall = 0.5 * Vstall **2 * rho * CLmax 
    return W_S_stall 


W_S = np.arange(10,300,1) # [N/m^2] variable 

T_W_cruise = [] 
T_W_climb = [] 
P_W_cruise = [] 
P_W_climb = []
P_W_service = [] 
W_S_stall = [] 
T_W_service = [] # where mac rc is 0.5 m/s 

for i in W_S : 
    # calculating thrust to weight ratios 
    T_W_cruise.append(thrustLoadingCruise(i))  
    T_W_climb.append(thrustLoadingClimb(Vroc(i),i, R_C))
    T_W_service.append(thrustLoadingClimb(Vroc(i),i, R_C_service))
    # calculating wing loading stall 
    W_S_stall_value = WingLoading_Vstall() 
    W_S_stall.append(W_S_stall_value) 

#Calculating Power loading 
for i in range(len(W_S)) : 
    P_W_cruise.append(powerLoading(T_W_cruise[i], V_cruise))
    P_W_climb.append(powerLoading(T_W_climb[i], Vroc(W_S[i]) )) 
    P_W_service.append(powerLoading(T_W_service[i], Vroc(W_S[i]) )) 

def plot_contraints() : 
    plt.plot(W_S, P_W_cruise, label = "Cruise P_W")
    plt.plot(W_S, P_W_climb, label = "Climb P_W")
    plt.plot(W_S, P_W_service, label = "Serivice P_W")
    #plt.plot(W_S, W_S_stall, label = "Stall Speed W_S")
    plt.vlines(WingLoading_Vstall(), 0,100, label= "Stall Speed W_S" )
    plt.xlabel ("Wing Loading [N/m^2]")
    plt.ylabel("Power Loading [W/kg]")
    plt.title ("Constraints Diagram")
    plt.ylim(0,100)
    plt.legend()

    return plt.show() 

plot_contraints()



