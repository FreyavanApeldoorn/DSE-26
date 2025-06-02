"""
This is the file for the Structures subsystem. It contains a single class.
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import simpson

import sys
from pathlib import Path
from typing import Any


PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.append(str(PROJECT_ROOT))

from DetailedDesign.funny_inputs import stab_n_con_funny_inputs as fi


import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

import numpy as np

class Structures:

    def __init__(self, inputs: dict[str, float]) -> None:
        self.inputs = inputs
        self.wing_span = inputs["wing_span"]
        self.outputs = self.inputs.copy()

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
        import numpy as np
        import matplotlib.pyplot as plt
        from scipy.integrate import simpson
        import os

        # --- Hard-coded parameters ---
        b = self.wing_span  # Full span (m)
        mass = 25.0  # UAV mass (kg)
        load_factor = 1.0  # 1.0 for level cruise (no pull-up)
        g = 9.81  # Gravity (m/s²)

        # Total lift for design (level flight)
        L_total = mass * g * load_factor

        # Half-span discretisation
        half_span = b / 2.0
        y = np.linspace(0.0, half_span, 100)  # 0 (root) to b/2 (tip)

        # Elliptical lift distribution: L(y) [N/m]
        #   L(y) = (L_total * 2/(π * b)) * sqrt(1 - (2y/b)²)
        L_y = (L_total * 2.0 / (np.pi * b)) * np.sqrt(
            np.maximum(0.0, 1.0 - (2.0 * y / b) ** 2)
        )

        # Pre-allocate shear and moment arrays
        V = np.zeros_like(y)  # Shear force [N]
        M = np.zeros_like(y)  # Bending moment [N·m]

        # Compute V(y) and M(y) via Simpson’s rule with correct x-spacing
        for i in range(len(y)):
            yi = y[i:]  # Stations from current i to tip
            Li = L_y[i:]  # Corresponding lift values
            # Shear: V(y_i) = ∫[y_i to b/2] L(η) dη
            V[i] = -simpson(Li, yi)
            # Moment: M(y_i) = ∫[y_i to b/2] L(η) * (η − y_i) dη
            M[i] = simpson(Li * (yi - y[i]), yi)

        # Ensure “Plots” directory exists
        os.makedirs("Plots", exist_ok=True)

        # Plot Lift, Shear and Moment on the same axes
        plt.figure(figsize=(10, 6))
        plt.plot(y, L_y, label="Lift Distribution $L(y)$ [N/m]")
        plt.plot(y, V, label="Shear Force $V(y)$ [N]")
        plt.plot(y, M, label="Bending Moment $M(y)$ [N·m]")
        plt.title("NVM for UAV Wing")
        plt.xlabel("Spanwise Position $y$ (m, 0=root to $b/2$=tip)")
        plt.ylabel("Magnitude (N or N·m)")
        plt.legend()
        plt.grid(True)
        plt.tight_layout()
        plt.savefig("Plots/VM_UAV_Wing.png", dpi=300)
        plt.close()

        return None

    # ~~~ Output functions ~~~

    def get_all(self) -> dict[str, float]:
        """

        # These are all the required outputs for this class. Plz consult the rest if removing any of them!
        
        self.total_mass()

        self.outputs["payload_mass"] = self.leftover_for_payload   # updated mass of the payload (with an added margin to avoid exceeding the MTOW requirement)
        self.outputs['mass_structure'] = self.mass_structure # kg


        #self.outputs["Volume_uav"] = ...

        #CG calculations:
        #self.outputs["CG"] = ...

        return self.outputs

        """


if __name__ == "__main__":  # pragma: no cover
    a = Structures(fi)
    a.NVM()
    # Perform sanity checks here
