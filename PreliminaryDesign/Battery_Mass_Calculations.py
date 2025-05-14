# Constants

g = 9.81  # Gravitational acceleration [m/s^2]
rho = 0.9013  # Air Density [kg/m^3]
R = 60000  # Range [m]
R_C = 3  # rate of climb [m/s]

#Calculates the battery mass fraction

class BattMass:

    def __init__(
        self,
        t_hover: float,
        t_loiter: float,
        M_to: float,
        E_spec: float,
        Eta_bat: float,
        f_usable: float,
        Eta_electric: float,
        T: float,
        DL: float,
        LD_max: float,
        CL: float,
        CD: float,
        WS: float,
        h_end: float,
        h_start: float,
        P_Prop: float,
        n_props_vtol: int,
    ):

        self.t_hover = t_hover  # Duration of hover [s]
        self.t_loiter = t_loiter  # Duration of loiter (horizontal flying) [s]
        self.M_to = M_to  # Take-off Mass [kg]
        self.E_spec = E_spec  # Specific Energy Capacity
        self.Eta_bat = Eta_bat  # Battery Efficiency
        self.f_usable = f_usable  # Usable Battery Capacity
        self.Eta_electric = Eta_electric  # Efficiency of electric system
        self.T = T  # Thrust
        self.DL = DL  # Disc Loading
        self.LD_max = LD_max  # Maximum Lift-over-drag ratio
        self.CL = CL  # Coefficient of Lift
        self.CD = CD  # Coefficient of Drag
        self.WS = WS  # Wing Loading
        self.h_end = h_end  # h end
        self.h_start = h_start  # h start
        self.P_Prop = P_Prop  # power of VTOL motors
        self.n_props_vtol = n_props_vtol # Number of VTOL propellers

    def Rotor_eff(self):
        FM = 0.4742 * (self.T / self.n_props_vtol) ** (0.0793)
        return FM

    def Batt_Mass_Hover(self):
        Batt_Mass_Hover = (
            (self.t_hover * g)
            / (
                self.E_spec
                * self.Rotor_eff()
                * self.Eta_electric
                * self.Eta_bat
                * self.f_usable
            )
        ) * (self.DL / (2 * rho)) ** 0.5
        return Batt_Mass_Hover

    def Batt_Mass_Climb(self):
        t_climb = (self.h_end - self.h_start) / (R_C) *2
        Batt_Mass_Climb = (t_climb * self.P_Prop) / (
            self.M_to * self.E_spec * self.Eta_bat * self.f_usable
        )
        return Batt_Mass_Climb

    def Batt_Mass_Range(self):
        Batt_Mass_Range = (R * g) / (
            self.E_spec * self.Eta_electric * self.Eta_bat * self.f_usable * self.LD_max
        )
        return Batt_Mass_Range

    def Batt_Mass_Endurance(self):
        Batt_Mass_Endurance = (
            (self.t_loiter * g)
            / (
                self.E_spec
                * self.Eta_electric
                * self.Eta_bat
                * self.f_usable
                * ((self.CL ** (3 / 2)) / self.CD)
            )
        ) * (2 * self.WS / rho) ** 0.5
        return Batt_Mass_Endurance

    def Batt_Mass_Total(self):
        Batt_Mass_Total_Max_Range_Fraction = (
            self.Batt_Mass_Hover()
            + self.Batt_Mass_Climb()
            + self.Batt_Mass_Range()
        )
        Batt_Mass_Total_Endurance_Fraction = (
            self.Batt_Mass_Hover()
            + self.Batt_Mass_Climb()
            + self.Batt_Mass_Endurance()
        )
        return Batt_Mass_Total_Max_Range_Fraction, Batt_Mass_Total_Endurance_Fraction


if __name__ == '__main__':
    t_hover = 4*60      # s
    t_loiter = 0
    E_spec = 168  # Specific energy capacity [Wh/kg]
    Eta_bat = 0.95 # ??
    f_usable = 6000  # Usable Battery Capacity [mAh]
    Eta_electric = 0.95  # Efficiency of electric system
    LD_max = 12  # max lift to drag ratio
    CL = 1  # lift coefficient
    CD = 0.04  # drag coefficient
    T = 95  # total thrust (weight) [N]
    h_end = 100  # Hieght drone climbs to [m]
    h_start = 0  # hieght drone starts at [m]
    
    batt_mass = BattMass(
        t_hover,
        t_loiter,
        30,
        E_spec,
        Eta_bat,
        f_usable,
        Eta_electric,
        T,
        1024,
        LD_max,
        CL,
        CD,
        115,
        h_end,
        h_start,
        3398,
    )

    batt_mass_range = batt_mass.Batt_Mass_Range() 
    batt_mass_climb = batt_mass.Batt_Mass_Climb() 
    batt_mass_hover = batt_mass.Batt_Mass_Hover() 

    print(batt_mass_range, batt_mass_climb, batt_mass_hover)
