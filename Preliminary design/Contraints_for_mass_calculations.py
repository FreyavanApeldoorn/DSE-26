import matplotlib.pyplot as plt
import numpy as np 

e = 0.7 #7 oswald efficiency factor  ESTIMATION 
AR = 10.03 # Aspect ratio of wing        ESTIMATION
R_C = 3 # [m/s] rate of climb        ESTIMATION
Vstall = 13.8 # stall speed [m/s]      ESTIMATION
CLmax = 1.34  #                         ESTIMATION
k =  1/ (np.pi * e * AR)

# Constants 
rho = 0.9013  # density at 3000m 
V_cruise = 27.77  # [m/s] cruise velocity 100km/hr
q = 0.5 * rho * V_cruise **2 # dynamic pressure 
CD0 = 0.040 + 0.2 # parasite drag + drag from rounded cylinder 
n_p = 0.85 
R_C_service = 0.5 #[m/s]

def powerLoading(T_W, V): 
    P_W = T_W * V / n_p 
    return P_W 

class Constraints:
    def __init__(self, e, AR, R_C, Vstall, CLmax):
        self.e = e
        self.AR = AR
        self.R_C = R_C
        self.Vstall = Vstall
        self.CLmax = CLmax
        # self.k =  1/ (np.pi * e * AR)

        self.W_S = np.arange(10,300,1) # [N/m^2] variable 

        self.T_W_cruise = [] 
        self.T_W_climb = [] 
        self.P_W_cruise = [] 
        self.P_W_climb = []
        self.P_W_service = [] 
        self.W_S_stall = [] 
        self.T_W_service = []

    @property
    def k(self):
        return 1 / (np.pi * self.e * self.AR)

    def thrustLoadingCruise(self, W_S): 
        T_W_cruise = q * CD0 * 1/(W_S) + self.k * 1/q  * W_S 
        return T_W_cruise 

    def Vroc (self, W_S) : 
        Vroc = np.sqrt(2/rho * W_S * np.sqrt(self.k/(3*CD0)))
        return Vroc
    
    def q_climb (self, Vroc) : 
        q_climb = 0.5 * rho * Vroc ** 2 
        return q_climb

    def thrustLoadingClimb(self, Vroc, W_S, R_C, q) : 
        T_W_climb = R_C / Vroc + q/W_S * CD0 + self.k/q * W_S
        return T_W_climb

    def WingLoading_Vstall(self) : 
        W_S_stall = 0.5 * self.Vstall **2 * rho * self.CLmax 
        return W_S_stall 
    
    def plot(self):
        self.T_W_cruise = [] 
        self.T_W_climb = [] 
        self.P_W_cruise = [] 
        self.P_W_climb = []
        self.P_W_service = [] 
        self.W_S_stall = [] 
        self.T_W_service = []

        for i in self.W_S : 
            # calculating thrust to weight ratios 
            self.T_W_cruise.append(self.thrustLoadingCruise(i))  
            self.T_W_climb.append(self.thrustLoadingClimb(self.Vroc(i),i, R_C, self.q_climb(self.Vroc(i))))
            self.T_W_service.append(self.thrustLoadingClimb(self.Vroc(i),i, R_C_service, self.q_climb(self.Vroc(i))))
            # calculating wing loading stall 
            W_S_stall_value = self.WingLoading_Vstall() 
            self.W_S_stall.append(W_S_stall_value) 

        #Calculating Power loading 
        for i in range(len(self.W_S)) : 
            self.P_W_cruise.append(powerLoading(self.T_W_cruise[i], V_cruise))
            self.P_W_climb.append(powerLoading(self.T_W_climb[i], self.Vroc(self.W_S[i]) )) #self.Vroc(self.W_S[i])
            self.P_W_service.append(powerLoading(self.T_W_service[i], self.Vroc(self.W_S[i]) )) 

        plt.plot(self.W_S, self.P_W_cruise, label = "Cruise P_W", color = "blue")
        plt.fill_between(self.W_S, self.P_W_cruise,  alpha = 0.3, color = "blue")

        plt.plot(self.W_S, self.P_W_climb, label = "Climb P_W", color = "pink")
        plt.fill_between(self.W_S, self.P_W_climb, alpha = 0.3, color = "pink")
        
        plt.plot(self.W_S, self.P_W_service, label = "Serivice P_W", color = "green")
        plt.fill_between(self.W_S, self.P_W_service, alpha = 0.3, color = "green")
        
        #plt.plot(W_S, W_S_stall, label = "Stall Speed W_S")
        plt.vlines(self.WingLoading_Vstall(), 0, 100, label= "Stall Speed W_S", color = "red" )
        plt.fill_between(np.arange(self.WingLoading_Vstall(), self.W_S[-1],1) , np.arange(self.WingLoading_Vstall(), self.W_S[-1],1), alpha = 0.5, color = "red")
        
        plt.xlabel ("Wing Loading [N/m^2]")
        plt.ylabel("Power Loading [W/kg]")
        plt.title ("Constraints Diagram")
        plt.ylim(0,100)

        
        plt.legend()
        plt.show() 
