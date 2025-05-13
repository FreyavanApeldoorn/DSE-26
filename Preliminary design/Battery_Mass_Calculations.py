# Constants

g = 9.81          # Gravitational acceleration [m/s^2]
rho = 0.9013      # Air Density [kg/m^3]
R = 60000         # Range [m]
R_C = 3           # rate of climb [m/s]





class BattMass:

    def __init__(self, t_hover: float, t_loiter:float, M_to:float, E_spec:float, Eta_bat: float,
                 f_usable:float, Eta_electric:float, T:float, DL:float, LD_max:float, CL:float, 
                   CD:float, WS:float, h_end:float, h_start:float, P_Prop:float  ):         
        self.t_hover = t_hover             # Duration of hover [s]
        self.t_loiter = t_loiter           # Duration of loiter (horizontal flying) [s]
        self.M_to = M_to                   # Take-off Mass [kg]
        self.E_spec = E_spec               # Specific Energy Capacity 
        self.Eta_bat = Eta_bat             # Battery Efficiency
        self.f_usable = f_usable           # Usable Battery Capacity
        self.Eta_electric = Eta_electric   # Efficiency of electric system
        self.T = T                         # Thrust
        self.DL = DL                       # Disc Loading
        self.LD_max = LD_max               # Maximum Lift-over-drag ratio
        self.CL = CL                       # Coefficient of Lift
        self.CD = CD                       # Coefficient of Drag
        self.WS = WS                       # Wing Loading
        self.h_end = h_end                 # h end 
        self.h_start = h_start             # h start
        self.P_Prop = P_Prop               # power of VTOL motors


    def Rotor_eff(self): 
        FM = 0.4742*self.T**(0.0793)          
        return FM 

    def Batt_Mass_Hover(self) : 
        Batt_Mass_Hover = ((self.t_hover * g) / ( self.E_spec * self.Rotor_eff() * self.Eta_electric * self.Eta_bat * self.f_usable))*(self.DL/(2*rho))**0.5
        return Batt_Mass_Hover

    def Batt_Mass_Climb(self): #includes descent
        t_climb = (self.h_end-self.h_start)/(R_C) *2
        Batt_Mass_Climb = (t_climb * self.P_Prop) / ( self.M_to * self.E_spec * self.Eta_bat * self.f_usable)
        return Batt_Mass_Climb
    
    def Batt_Mass_Range(self): 
        Batt_Mass_Range = (R * g) / ( self.E_spec * self.Eta_electric * self.Eta_bat * self.f_usable * self.LD_max)
        return Batt_Mass_Range

    def Batt_Mass_Endurance(self): 
        Batt_Mass_Endurance = ((self.t_loiter * g) / ( self.E_spec * self.Eta_electric * self.Eta_bat * self.f_usable * ((self.CL**(3/2)) / self.CD)))*(2*self.WS/rho)**0.5
        return Batt_Mass_Endurance
    
    def Batt_Mass_Total(self): 
        Batt_Mass_Total_Max_Range = self.Rotor_eff() + self.Batt_Mass_Hover() + self.Batt_Mass_Climb() + self.Batt_Mass_Range() 
        Batt_Mass_Total_Endurance = self.Rotor_eff() + self.Batt_Mass_Hover() + self.Batt_Mass_Climb() + self.Batt_Mass_Endurance()
        return Batt_Mass_Total_Max_Range, Batt_Mass_Total_Endurance

#if __name__ == '__main__':