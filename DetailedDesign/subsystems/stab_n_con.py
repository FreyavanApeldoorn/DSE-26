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

from DetailedDesign.funny_inputs import structures_funny_inputs as fi


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
        self.inputs = inputs
        # A simple `.get` keeps the attribute block short while still failing
        # loudly if the key is missing.
        for key, value in inputs.items():
            setattr(self, key, value)

        # Make a *copy* of the inputs dict so we do not mutate the caller’s data.
        self._outputs: dict[str, Any] = inputs.copy()

    # ---------------------------------------------------------------------#
    # Main Functions                                                       #
    # ---------------------------------------------------------------------#

    # ~~~ Aileron sizing ~~~

    def size_ailerons(self) -> float | str:
        """Return the achievable steady‑state roll rate *P* [rad/s].

        If *P* is insufficient, the method currently returns the string
        ``"siuuuuuu"`` as a placeholder so that the calling script
        will not silently continue.  Replace with a proper exception once
        the sizing loop is implemented.
        """
        # Construct a span‑wise chord distribution (rectangular planform assumed).
        spanwise_stations = np.linspace(0.0, self.wing_span / 2.0, 100)
        chord = np.full_like(spanwise_stations, self.wing_chord)

        # Mask indices that lie within the aileron span.
        aileron_idx = (spanwise_stations >= self.bi) & (spanwise_stations <= self.bo)

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

        Cl_p = -(
            (4.0 * (self.cl_alpha + self.cd_0))
            / (self.wing_area * self.wing_span)
            * simpson(chord * spanwise_stations**2, spanwise_stations)
        )

        delta_a = 0.5 * self.delta_a_max * (1.0 + self.aileron_differential)

        p_achieved = (
            -(Cl_delta_a / Cl_p) * delta_a * (2.0 * self.v_ref / self.wing_span)
        )

        # TODO: insert proper loop that iterates Δa, span, or chord until P_req is met.
        if p_achieved < self.roll_rate_req:
            return "siuuuuuu"

        return p_achieved
        return

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
        """Return the control & stability curves and the non‑dimensional CG track."""
        x_lemac = np.linspace(0.0, self.l_fus - self.mac, 1000)

        x_cg = (
            self.x_cg_no_wing * self.mass_no_wing
            + (self.wing_cg + x_lemac) * self.wing_mass
        ) / (self.mass_no_wing + self.wing_mass)

        x_cg_bar = (x_cg - x_lemac) / self.mac

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
    print(f"τ (c_a/c = {stabcon.ca_c:.2f}) = {stabcon._tau_from_ca_over_c():.4f}")
    print(f"Roll rate achieved: {stabcon.size_ailerons()}")
    sh_s_control, sh_s_stability, x_cg_bar = stabcon.scissor_plot()
    plt.plot(x_cg_bar, sh_s_control, label="Control surface effectiveness")
    plt.plot(x_cg_bar, sh_s_stability, label="Stability margin")
    plt.axhline(0.0, color="black", linestyle="--", label="Neutral stability")
    plt.xlabel("Non-dimensional CG position (x_cg / MAC)")
    plt.ylabel("Sh / S")
    plt.title("Scissor Plot")
    plt.legend()
    plt.grid()
    plt.show()
    print("Scissor plot generated.")
