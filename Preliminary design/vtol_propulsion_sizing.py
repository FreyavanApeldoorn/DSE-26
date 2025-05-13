import numpy as np

rho = 0.9013
r_c = 3


class VTOLProp:

    def __init__(self, w_s, stot_sw, MTOW, eta_prop):
        self.w_s = w_s
        self.stot_sw = stot_sw
        #        self.T = T
        self.MTOW = MTOW
        self.eta_prop = eta_prop

    def thrust_to_weight_vtol(self):
        """
        Calculate the thrust-to-weight ratio for a VTOL mode.

        Parameters:
        rho (float): Air density (kg/m^3)
        w_s (float): Wing loading (N/m^2)
        r_c (float): VTOL rate of climb (m/s)
        s_tot_s_w (float): Total projected aircraft area to wing area ratio

        Returns:
        float: Thrust-to-weight ratio
        """
        return 1.2 * (1 + (1 / self.w_s) * rho * r_c**2 * self.stot_sw)

    def power_required_vtol(self):
        """
        Calculate the power required for VTOL mode.

        Parameters:s
        T (float): Thrust (N)
        M_TO (float): Takeoff weight (kg)
        eta_prop (float): Propeller efficiency
        rho (float): Air density (kg/m^3)
        r_c (float): VTOL rate of climb (m/s)

        Returns:
        float: Power required (W)
        float: Propeller area (m2)
        """
        T = self.MTOW * self.thrust_to_weight_vtol()

        # Calculate the FM based on the thrust value, based on statistical relationship [FOR T = 0 - 100 N, EXTRAPOLATING OUTSIDE].
        FM = 0.4742 * T**0.0793

        # Calculate propeller disc loading DL, based on statistical relationship [FOR M_TO = 0 - 20 kg, EXTRAPOLATING OUTSIDE].
        DL = 3.2261 * self.MTOW + 74.991

        # Calculate propeller disc area S_prop
        S_prop = (self.MTOW * 9.81) / (DL * self.eta_prop)

        # Calculate induced hover velocity v_h
        v_h = np.sqrt(T / (2 * rho * S_prop))

        # Calculate induced axial climb velocity v_i
        v_i = v_h * (-r_c / (2 * v_h) + np.sqrt((r_c / (2 * v_h)) ** 2 + 1))

        return (T * v_i) / FM, S_prop
