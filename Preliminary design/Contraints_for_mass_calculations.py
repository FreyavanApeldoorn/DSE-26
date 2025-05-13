import matplotlib.pyplot as plt
import numpy as np 

e = 0.7 #7 oswald efficiency factor  ESTIMATION 
AR = 10.03 # Aspect ratio of wing        ESTIMATION
r_c = 3 # [m/s] rate of climb        ESTIMATION
Vstall = 13.8 # stall speed [m/s]      ESTIMATION
CLmax = 1.34  #                         ESTIMATION
k =  1/ (np.pi * e * AR)

# Constants 
rho = 0.9013  # density at 3000m 
Vmax = 27.77  # [m/s] cruise velocity 100km/hr
CD0 = 0.040 #+ 0.2 # parasite drag + drag from rounded cylinder 
n_p = 0.85 
R_C_service = 0.5 #[m/s]
k =  1/ (np.pi * e * AR)

def powerLoading(T_W, V): 
    P_W = T_W * V / n_p 
    return P_W 

class Constraints:
    def __init__(self, Vstall, Vmax):
        self.Vstall = Vstall
        self.Vmax = Vmax
        
    @property
    def q(self):
        return 0.5 * rho * self.Vmax **2

    def thrustLoadingCruise(self, W_S): 
        T_W_cruise = self.q * CD0 * 1/(W_S) + k * 1/self.q  * W_S 
        return T_W_cruise 

    def Vroc (self, W_S) : 
        Vroc = np.sqrt(2/rho * W_S * np.sqrt(k/(3*CD0)))
        return Vroc
    
    def q_climb (self, Vroc) : 
        q_climb = 0.5 * rho * Vroc ** 2 
        return q_climb

    def thrustLoadingClimb(self, Vroc, W_S, R_C, q) : 
        T_W_climb = R_C / Vroc + q/W_S * CD0 + k/q * W_S
        return T_W_climb

    def WingLoading_Vstall(self) : 
        W_S_stall = 0.5 * self.Vstall **2 * rho * CLmax 
        return W_S_stall 
    
    def plot(self):

        W_S = np.arange(0,130,1) # [N/m^2] variable 

        T_W_cruise = [] 
        T_W_climb = [] 
        P_W_cruise = [] 
        P_W_climb = []
        P_W_service = [] 
        W_S_stall = [] 
        T_W_service = []

        for i in W_S : 
            # calculating thrust to weight ratios 
            T_W_cruise.append(self.thrustLoadingCruise(i))  
            T_W_climb.append(self.thrustLoadingClimb(self.Vroc(i),i, r_c, self.q_climb(self.Vroc(i))))
            T_W_service.append(self.thrustLoadingClimb(self.Vroc(i),i, R_C_service, self.q_climb(self.Vroc(i))))
            # calculating wing loading stall 
            W_S_stall_value = self.WingLoading_Vstall() 
            W_S_stall.append(W_S_stall_value) 

        #Calculating Power loading 
        for i in range(len(W_S)) : 
            P_W_cruise.append(powerLoading(T_W_cruise[i], self.Vmax))
            P_W_climb.append(powerLoading(T_W_climb[i], self.Vroc(W_S[i]) )) #self.Vroc(self.W_S[i])
            P_W_service.append(powerLoading(T_W_service[i], self.Vroc(W_S[i]) )) 

        plt.plot(W_S, P_W_cruise, label = "Cruise P_W", color = "blue")
        plt.fill_between(W_S, P_W_cruise,  alpha = 0.3, color = "blue")

        plt.plot(W_S, P_W_climb, label = "Climb P_W", color = "pink")
        plt.fill_between(W_S, P_W_climb, alpha = 0.3, color = "pink")
        
        plt.plot(W_S, P_W_service, label = "Serivice P_W", color = "green")
        plt.fill_between(W_S, P_W_service, alpha = 0.3, color = "green")
        
        #plt.plot(W_S, W_S_stall, label = "Stall Speed W_S")
        plt.vlines(self.WingLoading_Vstall(), 0, 100, label= "Stall Speed W_S", color = "red" )
        plt.fill_between(np.arange(self.WingLoading_Vstall(), W_S[-1],1) , np.arange(self.WingLoading_Vstall(), W_S[-1],1), alpha = 0.5, color = "red")
        
        plt.xlabel ("Wing Loading [N/m^2]")
        plt.ylabel("Power Loading [N/W]")
        plt.title ("Constraints Diagram")
        plt.ylim(0,100)

        
        plt.legend()
        plt.show() 
