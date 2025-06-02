"""
This is the file for stability and control subsystem. It contains a single class.
"""

import numpy as np
from scipy.integrate import simpson
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

class StabCon:

    def __init__(self, inputs: dict[str, float]) -> None:
        self.inputs = inputs
        self.ca_c = self.inputs["ca_c"]  # Aileron chord to wing chord ratio
        self.delta_a_max = self.inputs[
            "delta_a_max"
        ]  # Maximum deflection angle of the ailerons
        self.aileron_differential = self.inputs["aileron_differential"]
        self.wing_area = self.inputs["wing_area"]  # Wing area
        self.wing_span = self.inputs["wing_span"]  # Wing span
        self.wing_chord = self.inputs["wing_chord"]  # Wing chord
        self.bi = self.inputs["bi"]  # Location to the innermost point of the aileron
        self.bo = self.inputs["bo"]
        self.roll_rate_req = self.inputs["roll_rate_req"]  # Roll rate requirement
        self.cl_alpha = self.inputs["cl_alpha"]
        self.cd_0 = self.inputs["cd_0"]
        self.wind_speed = self.inputs['wind_speed']
        self.rho_sea = self.inputs['rho_sea']
        self.Propeller_diameter_VTOL = self.inputs["Propeller_diameter_VTOL"]

        self.T_max = self.inputs['T_max']
        self.wing_area = self.inputs['wing_area']
        self.n_prop_vtol = self.inputs['n_prop_vtol']
        self.mtow = self.inputs['mtow']

        self.outputs = self.inputs.copy()

    # ~~~ Intermediate Functions ~~~

    def tau_from_ca_over_c(self):
        """
        Calculate elevator effectiveness (τ) from the ratio of control-surface chord to lifting-surface chord (cₐ/c).

        Returns
        -------
        float
            The effectiveness parameter τ corresponding to self.iinputs["ca_c"], by linear interpolation of the data in data/elevator_effectiveness.csv.
        """
        # Load two columns (ca/c , τ) from the CSV, skipping the header
        data = np.loadtxt(
            "DetailedDesign\data\elevator_effectiveness.csv", delimiter=",", skiprows=0
        )

        # Split into x-values (ca/c) and y-values (τ)
        x = data[:, 0]
        tau = data[:, 1]

        # Interpolate τ at the desired ratio
        return np.interp(self.ca_c, x, tau)

    def size_ailerons(self):
        """
        Calculate the size of the ailerons, based on:
        - The elevator effectiveness (τ) calculated from the ratio of control-surface chord to lifting-surface chord (cₐ/c).
        - The maximum deflection angle of the ailerons (delta_a_max).
        - The aileron differential (aileron_differential).
        - The wing area (wing_area).
        - The wing span (wing_span).
        - The wing chord (wing_chord).
        - The location to the innermost point of the aileron (bi).
        - The location to the outermost point of the aileron (bo).
        - The roll rate requirement (roll_rate_req).
        - The lift curve slope of the wing airfoil (cl_alpha).
        - The zero-lift drag coefficient of the wing airfoil (cd_0).


        Returns
        -------

        """
        ### TEMPORARY CREATE WING CHORD ARRAY AS A FUNCTION OF WING SPAN ASSUMING NON-TAPERED WING###
        y = np.linspace(0, self.wing_span / 2, 100)  # Half span
        c = self.inputs["wing_chord"] * y

        # Mask for the aileron span
        mask = (y >= self.bi) & (y <= self.bo)
        ### END TEMPORARY WING CHORD ARRAY CREATION ###

        # Calculate control derivative Cl_a
        Cl_a = (
            (2 * self.cl_alpha * self.tau_from_ca_over_c())
            / (self.wing_area * self.wing_span)
        ) * simpson(c[mask] * y[mask], y[mask])

        # Calculate stability derivative Cl_p
        Cl_p = -(
            (4 * (self.cl_alpha * self.cd_0)) / (self.wing_area * self.wing_span)
        ) * simpson(c * y**2, y[mask])

        return
    
    def size_VTOL_arms(self) -> float:
        '''
        Calculate the minimum boom arm length required for VTOL mode, based on the wind speed requirement.
        Returns the minimum boom arm length in meters, measured horizontally from the center of gravity to the propeller axis.
        '''
        wind_force_wing = 0.5*self.rho_sea*self.wind_speed**2 * self.wing_area
        wind_force_prop = 0.5*self.rho_sea*self.wind_speed**2 * (self.Propeller_diameter_VTOL/2)**2 * np.pi
        T_a_prop = self.T_max - (self.mtow / self.n_prop_vtol)

        minimum_boom_arm = (0.25*self.wing_span*wind_force_wing) / (2*(T_a_prop - wind_force_prop))

        return minimum_boom_arm
        

    # ~~~ Output functions ~~~

    def get_all(self) -> dict[str, float]:
        """
        # These are all the required outputs for this class. Plz consult the rest if removing any of them!

        outputs["Power_required"] = (
            ...
        )  # New requirement for power in order to get the right control authority

        outputs["Propeller_arm_length"] = ...
        outputs["Tail_arm"] = ...
        outputs["Tail_area"] = ...

        outputs["CG_x_max"] = ...
        outputs["CG_y_max"] = ...
        outputs["CG_x_min"] = ...
        outputs["CG_y_min"] = ...

        # something about control surfaces
        """
        return "self.outputs"

        return self.outputs


if __name__ == "__main__":  # pragma: no cover
    # Perform sanity checks here
    from funny_inputs import stab_n_con_funny_inputs as fi

    A = StabCon(fi)

    print(A.size_VTOL_arms())
