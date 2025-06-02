"""
This is the file for the Structures subsystem. It contains a single class.
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy import integrate

import sys
from pathlib import Path
from typing import Any


PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.append(str(PROJECT_ROOT))

from DetailedDesign.funny_inputs import funny_inputs as fi


import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

import numpy as np

class Structures:

    def __init__(self, inputs: dict[str, float]) -> None:
        self.inputs = inputs
        self.wing_span = inputs["wing_span"]
        self.mtow = self.inputs['mtow']
        self.span = self.inputs['wing_span']
        self.rho = self.inputs['rho']
        self.V_max = self.inputs['V_max']

        self.M_to = inputs["M_to"]

        self.mass_payload = inputs["payload_mass"]
        self.mass_hardware = inputs["mass_hardware"]
        self.mass_battery = inputs["mass_battery"]
        self.mass_propulsion = inputs["mass_propulsion"]
        
        self.wing_span = inputs["wing_span"]
                

    # ~~~ Intermediate Functions ~~~

    def example_function(self):
        """
        This is an example intermediate function
        """
        return True
    


    
    def total_mass(self) -> float:

        self.mass_structure = 10 # kg - THIS IS AN ESTIMATE, NEEDS TO BE UPDATED
        
        masses_nopay = np.array([self.mass_hardware, self.mass_battery, self.mass_propulsion, self.mass_structure])
        mass_nopay = np.sum(masses_nopay)

        self.leftover_for_payload = self.M_to - mass_nopay

    def NVM(self):
        """
        This function creates NVM plots for the UAV wing (hard-coded values).
        """

        half_span = self.span / 2.0
        y = np.linspace(0.0, half_span, 500)  # 0 (root) to b/2 (tip)

        # L_y = (self.mtow / (np.pi/4 * self.rho * self.V_max *self.span)) * np.sqrt(1 - (2*y / self.span)**2)
        L = ((4*self.mtow) / (np.pi*self.span)) * np.sqrt(1 - ((2*y)/self.span))

        L_y = integrate.cumulative_simpson(L, x=y)
        V = integrate.cumulative_simpson(L_y, x=y[:-1])
        M = integrate.cumulative_simpson(V, x=y[:-2])

        print(len(y), len(M))

        V = V - V[-1]
        M = M - M[-1]


        # Plot Lift, Shear and Moment on the same axes
        plt.figure(figsize=(10, 6))
        plt.plot(y[:-1], L_y, label="Lift Distribution $L(y)$ [N/m]")
        plt.plot(y[:-2], V, label="Shear Force $V(y)$ [N]")
        plt.plot(y[:-3], M, label="Bending Moment $M(y)$ [N·m]")
        plt.title("NVM for UAV Wing")
        plt.xlabel("Spanwise Position $y$ (m, 0=root to $b/2$=tip)")
        plt.ylabel("Magnitude (N or N·m)")
        plt.legend()
        plt.grid(True)
        plt.tight_layout()
        plt.savefig("DetailedDesign\subsystems\Plots\Try.png", dpi=300)

        return None

    # ~~~ Output functions ~~~

    def get_all(self) -> dict[str, float]:
        

        # These are all the required outputs for this class. Plz consult the rest if removing any of them!
        
        self.total_mass()

        self.outputs["payload_mass"] = self.leftover_for_payload   # updated mass of the payload (with an added margin to avoid exceeding the MTOW requirement)
        self.outputs['mass_structure'] = self.mass_structure # kg


        #self.outputs["Volume_uav"] = ...

        #CG calculations:
        #self.outputs["CG"] = ...

        return self.outputs

        


if __name__ == "__main__":  # pragma: no cover
    a = Structures(fi)
    a.NVM()
    # Perform sanity checks here
