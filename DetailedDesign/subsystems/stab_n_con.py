"""
Stability and Control (StabCon) subsystem.

This module provides the :class:`StabCon` class, which houses the sizing
utilities for the control surfaces and the longitudinal stability
assessment (trim & scissor‑plot) of the AeroShield UAV.
"""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

import numpy as np
from scipy.integrate import simpson
import matplotlib.pyplot as plt

PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.append(str(PROJECT_ROOT))

from DetailedDesign.funny_inputs import stab_n_con_funny_inputs as fi


class StabCon:
    """Stability & Control analysis helper for the AeroShield UAV.

    Parameters
    ----------
    inputs
        Dictionary that contains all dimensional / nondimensional input
        parameters required by the stability & control methods.
    """

    DATA_DIR = PROJECT_ROOT / "DetailedDesign" / "data"
    EFFECTIVENESS_FILE = DATA_DIR / "elevator_effectiveness.csv"

    # ---------------------------------------------------------------------#
    # Construction helpers                                                 #
    # ---------------------------------------------------------------------#

    def __init__(self, inputs: dict[str, float]) -> None:
        self.inputs = inputs.copy()  # Copy to avoid mutating caller's data

        self.wing_span = inputs["wing_span"]
        self.wing_chord = inputs["wing_chord"]
        self.wing_area = inputs["wing_area"]
        self.cl_alpha = inputs["cl_alpha"]
        self.cd_0 = inputs["cd_0"]

        self.bi = inputs["bi"]
        self.bo = inputs["bo"]

        self.v_ref = inputs["v_ref"]

        self.delta_a_max = inputs["delta_a_max"]
        self.aileron_differential = inputs["aileron_differential"]

        self.roll_rate_req = inputs["roll_rate_req"]

        self.rho_sea = inputs["rho_sea"]
        self.wind_speed = inputs["wind_speed"]
        self.Propeller_diameter_VTOL = inputs["Propeller_diameter_VTOL"]
        self.T_max = inputs["T_max"]
        self.mtow = inputs["mtow"]
        self.n_prop_vtol = inputs["n_prop_vtol"]

        self.l_fus = inputs["l_fus"]
        self.mac = inputs["mac"]
        self.x_cg_no_wing = inputs["x_cg_no_wing"]
        self.mass_no_wing = inputs["mass_no_wing"]
        self.wing_cg = inputs["wing_cg"]
        self.wing_mass = inputs["wing_mass"]
        self.x_ac_bar = inputs["x_ac_bar"]

        self.CL_alpha_h = inputs["CL_alpha_h"]
        self.CL_alpha_Ah = inputs["CL_alpha_Ah"]
        self.d_epsilon_d_alpha = inputs["d_epsilon_d_alpha"]
        self.lh = inputs["lh"]
        self.Vh_V = inputs["Vh_V"]
        self.Cm_ac = inputs["Cm_ac"]

        self.ca_c = inputs["ca_c"]

        self.lvt = inputs["lvt"]
        self.Vv = inputs["Vv"]
        self.ARvt = inputs["ARvt"]
        self.taper_ratio_vt = inputs["taper_ratio_vt"]

        # Prepare an outputs dictionary for later use
        self._outputs: dict[str, Any] = self.inputs.copy()

    # ---------------------------------------------------------------------#
    # Main Functions                                                       #
    # ---------------------------------------------------------------------#

    # ~~~ Aileron sizing ~~~

    def size_ailerons(self, step_frac: float = 0.001) -> float:
        """
        Return the achievable steady-state roll rate *p_achieved* [rad/s], by expanding
        the aileron's outer station bo until roll_rate_req is met or until bo reaches half-span.

        Args:
            step_frac (float): Fraction of half-span to increment bo on each iteration.
                               For instance, step_frac=0.01 means bo jumps by (0.01 * wing_span/2)
                               each time.

        Returns:
            p_achieved (float): The final roll rate achieved once sizing has converged.
            bo (float): The final outer aileron station after sizing.

        Raises:
            ValueError: If bo cannot be increased further (hits half-span) without meeting the requirement.
        """
        half_span = self.wing_span / 2.0

        # Sanity check: ensure 0 ≤ bi < bo ≤ half_span
        if not (0.0 <= self.bi < self.bo <= half_span):
            raise ValueError(f"Invalid aileron stations: bi={self.bi}, bo={self.bo}")

        # Precompute arrays that stay constant
        spanwise_stations = np.linspace(0.0, half_span, 1000)
        chord = np.full_like(spanwise_stations, self.wing_chord)

        # Compute Cl_p once (unchanging with bo)
        Cl_p = -(
            (4.0 * (self.cl_alpha + self.cd_0))
            / (self.wing_area * self.wing_span)
            * simpson(chord * spanwise_stations**2, spanwise_stations)
        )

        # Fixed‐increment for bo (in meters)
        delta_bo = step_frac * half_span

        while True:
            # 1) Mask stations within [bi, bo] for the current bo
            aileron_idx = (spanwise_stations >= self.bi) & (
                spanwise_stations <= self.bo
            )

            # 2) Compute Cl_delta_a for this bo
            Cl_delta_a = (
                2.0
                * self.cl_alpha
                * self._tau_from_ca_over_c()
                / (self.wing_area * self.wing_span)
                * simpson(
                    chord[aileron_idx] * spanwise_stations[aileron_idx],
                    spanwise_stations[aileron_idx],
                )
            )

            # 3) Compute delta_a (max deflection × differential factor)
            delta_a = 0.5 * self.delta_a_max * (1.0 + self.aileron_differential)

            # 4) Compute p_achieved
            p_achieved = (
                -(Cl_delta_a / Cl_p) * delta_a * (2.0 * self.v_ref / self.wing_span)
            )

            # 5) Check if requirement is met
            if p_achieved >= self.roll_rate_req:
                return p_achieved, self.bo

            # 6) If not, increase bo by one step
            new_bo = self.bo + delta_bo

            # 7) Safety: cannot exceed half-span
            if new_bo >= half_span:
                raise ValueError(
                    f"Cannot meet roll-rate requirement. "
                    f"Reached bo={self.bo:.3f} m (max half-span={half_span:.3f} m) without achieving "
                    f"{self.roll_rate_req:.3f} rad/s (max achieved: {p_achieved:.3f})."
                )

            # 8) Update bo and loop again

            self.bo = new_bo

    # ~~~ Vertical tailplane sizing ~~~

    def size_vertical_tailplane(self) -> float:
        """
        Calculate the vertical tailplane area, span, MAC, root chord, and tip chord.

        Returns:

            vertical_tailplane_area (float): Area of the vertical tailplane in square meters.
            vertical_tailplane_span (float): Span of the vertical tailplane in meters.
            vertical_tailplane_mac (float): Mean Aerodynamic Chord (MAC) of the vertical tailplane in meters.
            vertical_tailplane_root_chord (float): Root chord of the vertical tailplane in meters.
            vertical_tailplane_tip_chord (float): Tip chord of the vertical tailplane in meters.
        """

        vertical_tailplane_area = self.Vv * self.wing_span * self.wing_area / self.lvt
        vertical_tailplane_span = np.sqrt(vertical_tailplane_area * self.ARvt)
        vertical_tailplane_mac = vertical_tailplane_area / vertical_tailplane_span
        vertical_tailplane_root_chord = (
            (3 / 2)
            * vertical_tailplane_mac
            * (
                (1 + self.taper_ratio_vt)
                / (1 + self.taper_ratio_vt + self.taper_ratio_vt**2)
            )
        )
        vertical_tailplane_tip_chord = (
            vertical_tailplane_root_chord * self.taper_ratio_vt
        )

        return (
            vertical_tailplane_area,
            vertical_tailplane_span,
            vertical_tailplane_mac,
            vertical_tailplane_root_chord,
            vertical_tailplane_tip_chord,
        )
    
    def size_rudder(self):
        

    # ~~~ VTOL sizing ~~~

    def size_VTOL_arms(self) -> float:
        """
        Calculate the minimum boom arm length required for VTOL mode, based on the wind speed requirement.
        Returns the minimum boom arm length in meters, measured horizontally from the center of gravity to the propeller axis.
        """
        wind_force_wing = 0.5 * self.rho_sea * self.wind_speed**2 * self.wing_area
        wind_force_prop = (
            0.5
            * self.rho_sea
            * self.wind_speed**2
            * (self.Propeller_diameter_VTOL / 2) ** 2
            * np.pi
        )
        T_a_prop = self.T_max - (self.mtow / self.n_prop_vtol)

        minimum_boom_arm = (0.25 * self.wing_span * wind_force_wing) / (
            2 * (T_a_prop - wind_force_prop)
        )

        return minimum_boom_arm

    # ~~~ Scissor plot ~~~

    def scissor_plot(self) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
        """Return the control & stability curves and the non-dimensional CG track."""
        # Create an array with positions for lemac.
        x_lemac = np.linspace(0.0, self.l_fus - self.mac, 5)
        print(x_lemac)

        x_cg = (
            self.x_cg_no_wing * self.mass_no_wing
            + (self.wing_cg + x_lemac) * self.wing_mass
        ) / (self.mass_no_wing + self.wing_mass)

        x_cg_bar = (x_cg - x_lemac) / self.mac
        print(x_cg_bar)

        sh_s_stability = (
            1.0
            / (
                (self.CL_alpha_h / self.CL_alpha_Ah)
                * (1.0 - self.d_epsilon_d_alpha)
                * (self.lh / self.mac)
                * self.Vh_V**2
            )
            * (x_cg_bar - self.x_ac_bar - 0.05)
        )

        sh_s_control = (
            1.0
            / (
                (self.CL_alpha_h / self.CL_alpha_Ah)
                * (self.lh / self.mac)
                * self.Vh_V**2
            )
            * (x_cg_bar + self.Cm_ac / self.CL_alpha_Ah - self.x_ac_bar)
        )

        return sh_s_control, sh_s_stability, x_cg_bar

    # ---------------------------------------------------------------------#
    # Convenience getters                                                  #
    # ---------------------------------------------------------------------#

    def get_all(self) -> dict[str, Any]:
        """Return a *copy* of the output dictionary for external consumption."""
        return self._outputs.copy()

    # ---------------------------------------------------------------------#
    # Private helpers                                                      #
    # ---------------------------------------------------------------------#

    def _tau_from_ca_over_c(self) -> float:
        """Interpolate elevator effectiveness τ for the configured cₐ/c ratio."""
        data = np.loadtxt(self.EFFECTIVENESS_FILE, delimiter=",", skiprows=0)
        ca_c, tau = data.T
        return float(np.interp(self.ca_c, ca_c, tau))


# ---------------------------------------------------------------------------#
# Basic sanity check                                                         #
# ---------------------------------------------------------------------------#
if __name__ == "__main__":  # pragma: no cover
    stabcon = StabCon(fi)
    stabcon.size_ailerons()
    print("Ailerons sized successfully.")
    p_achieved, bo = stabcon.size_ailerons()
    print(
        f"Achieved roll rate: {np.rad2deg(p_achieved):.3f} deg/s with bo = {bo:.3f} m"
    )

    plt.plot(stabcon.scissor_plot()[2], stabcon.scissor_plot()[0], label="Control")
    plt.plot(stabcon.scissor_plot()[2], stabcon.scissor_plot()[1], label="Stability")
    plt.xlabel("Non-dimensional CG position (x_cg_bar)")
    plt.ylabel("Sh/S")
    plt.title("Scissor Plot")
    plt.axhline(0, color="black", linestyle="--", linewidth=0.5)
    plt.axvline(0, color="black", linestyle="--", linewidth=0.5)
    plt.legend()
    plt.grid()
    plt.show()
    print("Scissor plot generated successfully.")

    print(stabcon.size_vertical_tailplane())
    print("Vertical tailplane area: ", stabcon.size_vertical_tailplane()[0])
    print("Vertical tailplane span: ", stabcon.size_vertical_tailplane()[1])
    print("Vertical tailplane MAC: ", stabcon.size_vertical_tailplane()[2])
    print("Vertical tailplane root chord: ", stabcon.size_vertical_tailplane()[3])
    print("Vertical tailplane tip chord: ", stabcon.size_vertical_tailplane()[4])
