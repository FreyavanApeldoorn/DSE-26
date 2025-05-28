'''
This is the file for the propulsion and power subsystem. It contains a single class.
'''
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))


import numpy as np

from DetailedDesign.subsystems.constraints import Constraints
from DetailedDesign.funny_inputs import funny_inputs



class Propulsion:

    def __init__(self, inputs: dict[str, float]) -> None:
        self.inputs = inputs
        self.wing_loading = inputs['wing_loading']
        self.s_tot_sw = inputs['s_tot_sw'] # Total projected aircraft area to wing area ratio
        self.n_prop_vtol = inputs ['n_prop_vtol'] #number of vtol properlers
        self.rho = inputs['rho']
        self.vtol_roc = inputs ['vtol_roc']
        self.mtow = inputs ['mtow']
        self.g = inputs ['g']

        self.outputs = self.inputs.copy()
        

    # ~~~ Intermediate Functions ~~~

    def thrust_to_weight_vtol(self) -> float :
        """
        Calculate the thrust-to-weight ratio for a VTOL mode.

        Parameters:
        rho (float): Air density (kg/m^3)
        w_s (float): Wing loading (N/m^2)
        vtol_roc (float): VTOL rate of climb (m/s)
        s_tot_s_w (float): Total projected aircraft area to wing area ratio

        Returns:
        float: Thrust-to-weight ratio
        """
        return 1.2 * (1 + (1 / self.wing_loading) * self.rho * self.vtol_roc **2 * self.s_tot_sw)
    
    def power_required_vtol(self):
        """
        Calculate the power required for VTOL mode.

        Parameters:s
        T (float): Thrust (N)
        MTOW (float): Takeoff weight (N)
        n_props_vtol (int): Number of VTOL propellers
        rho (float): Air density (kg/m^3)
        r_c (float): VTOL rate of climb (m/s)

        Returns:
        float: Power required (W)
        float: Propeller area (m2)
        """
        total_thrust = self.mtow * self.thrust_to_weight_vtol()

        # Calculate the FM based on the thrust value, based on statistical relationship [FOR T = 0 - 100 N, EXTRAPOLATING OUTSIDE].
        FM = 0.4742 * (total_thrust / self.n_prop_vtol) ** 0.0793

        # Calculate propeller disc loading DL, based on statistical relationship [FOR M_TO = 0 - 20 kg, EXTRAPOLATING OUTSIDE].
        prop_disk_loading = 3.2261 * self.mtow / self.g + 74.991

        # Calculate propeller disc area S_prop
        S_prop = (self.mtow) / (prop_disk_loading * self.n_prop_vtol)

        # Calculate induced hover velocity v_h
        v_h = np.sqrt(total_thrust / (2 * self.rho * S_prop) / self.n_prop_vtol)

        # Calculate induced axial climb velocity v_i
        v_i = v_h * (-self.vtol_roc / (2 * v_h) + np.sqrt((self.vtol_roc / (2 * v_h)) ** 2 + 1))

        #calculate the total vtol power 
        vtol_power = (total_thrust * v_i) / FM

        return vtol_power , S_prop, prop_disk_loading, total_thrust

    def power_required_cruise(self): 
        constraints = Constraints(funny_inputs)
        W_S, P_W_cruise, P_W_climb, P_W_service, W_S_stall, optimal_cruise_power = constraints.form_variable_lists()
        return optimal_cruise_power
    
    # ~~~ Output functions ~~~ 

    def get_all(self) -> dict[str, float]:
        outputs = self.inputs.copy()
        vtol_power, S_prop, prop_disk_loading , total_thrust = self.power_required_vtol()
        optimal_cruise_power = self.power_required_cruise()

        # These are all the required outputs for this class. Plz consult the rest if removing any of them!
        outputs["Power_required_VTOL"] = vtol_power
        outputs["Power_required_cruise"] = optimal_cruise_power
        outputs["Power_required_hover"] = ...
    
        outputs["Power_available_VTOL"] = ...
        outputs["Power_available_cruise"] = ...

        outputs["Propeller_diameter_VTOL"] = np.sqrt(S_prop/3.14) * 2
        outputs["Propeller_diameter_cruise"] = ...
        
        outputs["Propulsion_system_mass"] = ...
        outputs["Motor_mass_VTOL"] = ...
        outputs["Motor_mass_cruise"] = ...
        outputs["Propeller_mass_VTOL"] = ...
        outputs["Propeller_mass_cruise"] = ...

        return outputs

    
if __name__ == '__main__':
    # Perform sanity checks here
    propulsion = Propulsion(funny_inputs)
    print(propulsion.get_all())

    