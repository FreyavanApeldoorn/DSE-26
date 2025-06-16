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

    def __init__(self, inputs: dict[str, float], hardware=None) -> None:
        self.inputs = inputs.copy()
        self.hardware = hardware
        self._outputs = inputs.copy()

        # Dynamically assign all inputs to instance attributes
        for key, value in self.inputs.items():
            setattr(self, key, value)

    # ---------------------------------------------------------------------#
    # Main Functions                                                      #
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
        chord = (
            self.wing_root_chord
            - ((self.wing_root_chord - self.wing_tip_chord) / half_span)
            * spanwise_stations
        )

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
                * self._tau_from_ca_over_c(self.ca_c)
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
                return p_achieved, self.bo, Cl_delta_a, Cl_p

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

    # ~~~ Rudder sizing (static-trim gust criterion, τr varies with cr/cv) ~~~
    def size_rudder_for_gust(self, step_frac: float = 0.02) -> tuple[float, float]:
        """
        Iterate the rudder-to-fin chord ratio (cr/cv) until the rudder can
        *trim* the sideslip created by a design gust.

        Returns
        -------
        cr_over_cv : float
            Final chord ratio.
        sr_over_sv : float
            Rudder-area / fin-area ratio for bookkeeping.
        """
        # ── 1.  Gust-induced sideslip ────────────────────────────────────
        beta_0 = self.gust_speed / self.v_ref  # [rad]

        # ── 2.  Directional stability derivative (fin only) ─────────────
        CL_alpha_v = (
            np.pi * self.ARvt / (1 + np.sqrt(1 + (self.ARvt / 2) ** 2))
        )  # [1/rad]
        Cn_beta = -0.8 * CL_alpha_v * self.Vv  # < 0 (restoring)
        print(f"Cl: {CL_alpha_v}")

        # Required control power, per rad of deflection
        Cn_req = abs(Cn_beta * beta_0) / self.delta_r_max

        # ── 3.  Vertical-tail reference area & constants ────────────────
        S_v = self.Vv * self.wing_area * self.wing_span / self.lvt
        V_v = self.Vv  # alias for clarity
        br_bv = self.br_bv

        # ── 4.  Iterate on cr/cv ────────────────────────────────────────
        cr_cv = self.cr_cv_init
        max_cr_cv = 0.9
        dcr = step_frac * max_cr_cv

        while True:
            # ♦ Effectiveness grows with chord ratio ♦
            tau_r = self._tau_from_ca_over_c(cr_cv)

            S_r = cr_cv * br_bv * S_v
            Cn_dr = tau_r * CL_alpha_v * V_v * (S_r / S_v)

            if Cn_dr >= Cn_req:  # ✅ requirement met
                self.cr_over_cv = cr_cv
                self.rudder_area = S_r
                self.Cn_delta_r = Cn_dr
                self._outputs.update(
                    {"cr_over_cv": cr_cv, "rudder_area": S_r, "Cn_delta_r": Cn_dr}
                )
                return cr_cv, S_r / S_v

            cr_cv += dcr  # ➜ try a larger chord

            if cr_cv > max_cr_cv:
                raise ValueError(
                    f"Cannot meet gust-trim requirement: need Cnδr={Cn_req:.4f}, "
                    f"achieved {Cn_dr:.4f} at cr/cv={max_cr_cv:.2f}."
                )

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

    # ~~~ C.G Calculation ~~~

    def calculate_UAV_cg(self) -> dict:
        """Calculate the center of gravity (c.g.) of the UAV for different configurations."""

        results = {}
        for configuration in ["wildfire", "oil_spill", "no_payload"]:
            if configuration == "wildfire":
                sensor_mass = self.wildfire_sensor_mass
                sensor_x = self.wildfire_sensor_x
                sensor_y = self.wildfire_sensor_y
                sensor_z = self.wildfire_sensor_z
                payload_mass = self.payload_mass
                buoy_mass = 0
                buoy_x = 0
                buoy_y = 0
                buoy_z = 0
            elif configuration == "no_payload":
                sensor_mass = self.wildfire_sensor_mass
                sensor_x = self.wildfire_sensor_x
                sensor_y = self.wildfire_sensor_y
                sensor_z = self.wildfire_sensor_z
                payload_mass = 0
                buoy_mass = 0
                buoy_x = 0
                buoy_y = 0
                buoy_z = 0
            else:  # oil_spill
                sensor_mass = self.oil_sensor_mass
                sensor_x = self.oil_sensor_x
                sensor_y = self.oil_sensor_y
                sensor_z = self.oil_sensor_z
                buoy_mass = self.buoy_mass
                buoy_x = self.buoy_x
                buoy_y = self.buoy_y
                buoy_z = self.buoy_z

            # Calculate the c.g of the fuselage group
            numerator_x_fuselage = (
                sensor_mass * sensor_x
                + self.gymbal_connection_mass * self.gymbal_connection_x
                + self.flight_controller_mass * self.flight_controller_x
                + self.OBC_mass * self.OBC_x
                + self.GPS_mass * self.GPS_x
                + self.Mesh_network_module_mass * self.Mesh_network_module_x
                + self.SATCOM_module_mass * self.SATCOM_module_x
                + self.Winch_motor_mass * self.Winch_motor_x
                + (self.motor_mass_cruise + self.propeller_mass_cruise)
                * self.motor_cruise_x
                + payload_mass * self.payload_x
                + buoy_mass * buoy_x
                # add structure, tail, landing gear
            )

            # numerator_y_fuselage = (
            #     sensor_mass * sensor_y +
            #     self.oil_sensor_mass * self.oil_sensor_y +
            #     self.gymbal_connection_mass * self.gymbal_connection_y +
            #     self.flight_controller_mass * self.flight_controller_y +
            #     self.OBC_mass * self.OBC_y +
            #     self.GPS_mass * self.GPS_y +
            #     self.Mesh_network_module_mass * self.Mesh_network_module_y +
            #     self.SATCOM_module_mass * self.SATCOM_module_y +
            #     self.Winch_motor_mass * self.Winch_motor_y +
            #     (self.motor_mass_cruise + self.propeller_mass_cruise) * self.motor_cruise_y +

            #     self.payload_mass * self.payload_y +
            #     buoy_mass * buoy_y
            #     # add structure, tail, landing gear
            # )

            # numerator_z_fuselage = (
            #     sensor_mass * sensor_z +
            #     self.oil_sensor_mass * self.oil_sensor_z +
            #     self.gymbal_connection_mass * self.gymbal_connection_z +
            #     self.flight_controller_mass * self.flight_controller_z +
            #     self.OBC_mass * self.OBC_z +
            #     self.GPS_mass * self.GPS_z +
            #     self.Mesh_network_module_mass * self.Mesh_network_module_z +
            #     self.SATCOM_module_mass * self.SATCOM_module_z +
            #     self.Winch_motor_mass * self.Winch_motor_z +
            #     (self.motor_mass_cruise + self.propeller_mass_cruise) * self.motor_cruise_z +

            #     self.payload_mass * self.payload_z +
            #     buoy_mass * buoy_z
            #     # add structure, tail, landing gear
            # )

            fuselage_mass = (
                sensor_mass
                + self.gymbal_connection_mass
                + self.flight_controller_mass
                + self.OBC_mass
                + self.GPS_mass
                + self.Mesh_network_module_mass
                + self.SATCOM_module_mass
                + self.Winch_motor_mass
                + payload_mass
                + buoy_mass
                + self.motor_mass_cruise
                + self.propeller_mass_cruise
                # add structure, tail, landing gear
            )
            # print("numerator_x_fuselage =", numerator_x_fuselage)
            # print("fuselage_mass =", fuselage_mass)

            fuselage_x_cg = numerator_x_fuselage / fuselage_mass
            # print("fuselage_x_cg =", fuselage_x_cg)
            # fuselage_y_cg = numerator_y_fuselage / fuselage_mass
            # fuselage_z_cg = numerator_z_fuselage / fuselage_mass

            # Wing group
            numerator_x_wing = (
                2
                * (self.motor_mass_VTOL + self.propeller_mass_VTOL)
                * self.motor_front_VTOL_x
                + 2
                * (self.motor_mass_VTOL + self.propeller_mass_VTOL)
                * self.motor_rear_VTOL_x
                + self.battery_mass * self.battery_x
                + self.PDB_mass * self.PDB_x
                # add wing structure here
            )

            wing_mass = (
                4 * self.motor_mass_VTOL
                + self.battery_mass
                + self.PDB_mass
                # add wing structure here
            )

            wing_x_cg = numerator_x_wing / wing_mass

            # Save result for this configuration
            results[configuration] = {
                "fuselage_mass": fuselage_mass,
                "wing_mass": wing_mass,
                "fuselage_x_cg": fuselage_x_cg,
                # "fuselage_y_cg": fuselage_y_cg,
                # "fuselage_z_cg": fuselage_z_cg,
                "wing_x_cg": wing_x_cg,
            }

        return results

    def calculate_uav_cg_chat(self) -> dict[str, dict[str, float]]:
        """Return fuselage and wing longitudinal CG for each mission configuration."""
        # ---------------------------------------------------------------------
        # 1. Mission‑specific items (mass [kg], x‑coordinate [m])
        # ---------------------------------------------------------------------
        configs = {
            "wildfire": dict(
                sensor=(self.wildfire_sensor_mass, self.wildfire_sensor_x),
                payload=(self.payload_mass, self.payload_x),
                buoy=(0.0, 0.0),
            ),
            "oil_spill": dict(
                sensor=(self.oil_spill_sensor_mass, self.oil_spill_sensor_x),
                payload=(self.payload_mass, self.payload_x),
                buoy=(self.buoy_mass, self.buoy_x),
            ),
            "no_payload_wildfire": dict(
                sensor=(self.wildfire_sensor_mass, self.wildfire_sensor_x),
                payload=(0.0, 0.0),
                buoy=(0.0, 0.0),
            ),
            "no_payload_oil_spill": dict(
                sensor=(self.oil_spill_sensor_mass, self.oil_spill_sensor_x),
                payload=(0.0, 0.0),
                buoy=(self.buoy_mass, self.buoy_x),
            ),
        }

        # ---------------------------------------------------------------------
        # 2. Fixed fuselage components (present in every configuration)
        # ---------------------------------------------------------------------
        fuselage_static = [
            (self.gymbal_connection_mass, self.gymbal_connection_x),
            (self.flight_controller_mass, self.flight_controller_x),
            (self.OBC_mass, self.OBC_x),
            (self.GPS_mass, self.GPS_x),
            (self.Mesh_network_module_mass, self.Mesh_network_module_x),
            (self.SATCOM_module_mass, self.SATCOM_module_x),
            (self.Winch_motor_mass, self.Winch_motor_x),
            (self.motor_mass_cruise + self.propeller_mass_cruise, self.motor_cruise_x),
            (self.CUAV_airlink_mass, self.CUAV_airlink_x),
            (self.fuselage_structural_mass, self.fuselage_structural_x_cg),
            (self.tailplane_structural_mass, self.tailplane_structural_x_cg),
        ]

        # ---------------------------------------------------------------------
        # 3. Wing group (identical for all variants)
        # ---------------------------------------------------------------------
        lift_motor_mass = self.motor_mass_VTOL + self.propeller_mass_VTOL
        wing_items = [
            (2 * lift_motor_mass, self.motor_front_VTOL_x),
            (2 * lift_motor_mass, self.motor_rear_VTOL_x),
            (self.battery_mass, self.battery_x),
            (self.PDB_mass, self.PDB_x),
            (self.wing_structural_mass, self.wing_structural_x_cg),
        ]

        # ---------------------------------------------------------------------
        # 4. Helper functions
        # ---------------------------------------------------------------------
        mass_sum = lambda items: sum(m for m, _ in items)
        moment_sum = lambda items: sum(m * x for m, x in items)

        # ---------------------------------------------------------------------
        # 5. Main loop
        # ---------------------------------------------------------------------
        results: dict[str, dict[str, float]] = {}
        for name, cfg in configs.items():
            fuselage_items = fuselage_static + [
                cfg["sensor"],
                cfg["payload"],
                cfg["buoy"],
            ]

            fus_mass = mass_sum(fuselage_items)
            fus_x_cg = moment_sum(fuselage_items) / fus_mass

            wing_mass = mass_sum(wing_items)
            wing_x_cg = moment_sum(wing_items) / wing_mass

            results[name] = {
                "fuselage_mass": fus_mass,
                "wing_mass": wing_mass,
                "fuselage_x_cg": fus_x_cg,
                "wing_x_cg": wing_x_cg,
            }

        return results

    # ~~~ Loading diagram ~~~
    def loading_diagram(self) -> tuple[np.ndarray, np.ndarray]:
        """Calculate the loading diagram for the UAV for different configurations."""
        x_lemac = np.linspace(0.5, self.l_fus - 0.5, 10)

        results = {}
        for configuration in ["wildfire", "oil_spill", "no_payload"]:
            if configuration == "wildfire":
                fuselage_x_cg = self.wildfire_fuselage_x_cg
                wing_x_cg = self.wildfire_wing_x_cg
                fuselage_mass = self.wildfire_fuselage_mass
                wing_mass = self.wildfire_wing_mass
            elif configuration == "no_payload":
                fuselage_x_cg = self.no_payload_fuselage_x_cg
                wing_x_cg = self.wildfire_wing_x_cg
                fuselage_mass = self.no_payload_fuselage_mass
                wing_mass = self.wildfire_wing_mass
            else:
                fuselage_x_cg = self.oil_spill_fuselage_x_cg
                wing_x_cg = self.oil_spill_wing_x_cg
                fuselage_mass = self.oil_spill_fuselage_mass
                wing_mass = self.oil_spill_wing_mass

            x_cg = (
                fuselage_x_cg * fuselage_mass + (wing_x_cg + x_lemac) * wing_mass
            ) / (fuselage_mass + wing_mass)

            x_cg_bar = (x_cg - x_lemac) / self.mac

            results[configuration] = {
                "x_lemac": x_lemac,
                "x_cg": x_cg,
                "x_cg_bar": x_cg_bar,
            }
        return results

    def loading_diagram_chat(
        self, n_pts: int = 1000
    ) -> dict[str, dict[str, np.ndarray]]:
        """
        Build a longitudinal-loading diagram for each payload configuration.

        Returns
        -------
        dict
            results[config] = {
                "x_lemac" : np.ndarray,   # span of LE-MAC positions tested [m]
                "x_cg"    : np.ndarray,   # absolute CG positions along fuselage [m]
                "x_cg_bar": np.ndarray,   # CG as fraction of MAC aft of LE-MAC [-]
            }
        Notes
        -----
        ▸ Uses calculate_uav_cg_chat() internally, so any change in component
        weights/locations is picked up automatically.
        ▸ The term (wing_x_cg + x_lemac) follows your original convention:
        wing-group CG is measured from the wing datum, whereas x_lemac is the
        leading-edge-of-MAC position along the fuselage.
        """
        # 1. Get current masses & CGs
        cg_results = self.calculate_uav_cg_chat()

        # 2. Create the LE-MAC sweep
        x_lemac = np.linspace(0.5, self.l_fus - 0.5, n_pts)

        # 3. Loop over configurations
        results: dict[str, dict[str, np.ndarray]] = {}
        for config, data in cg_results.items():
            fus_mass, fus_x = data["fuselage_mass"], data["fuselage_x_cg"]
            wing_mass, wing_x = data["wing_mass"], data["wing_x_cg"]

            # Aircraft CG for each LE-MAC position
            x_cg = (fus_x * fus_mass + (wing_x + x_lemac) * wing_mass) / (
                fus_mass + wing_mass
            )

            # CG expressed as fraction of MAC behind LE-MAC
            x_cg_bar = (x_cg - x_lemac) / self.mac

            results[config] = {"x_lemac": x_lemac, "x_cg": x_cg, "x_cg_bar": x_cg_bar}

        return results

    # ~~~ Scissor plot ~~~

    def scissor_plot(self) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
        """Return the control & stability curves and the non-dimensional CG track."""
        # Create an array with positions for lemac and the corresponding X_cg_bar values

        x_cg_bar = np.linspace(-0.5, 1.5, 100)

        # some preliminary calculations needed
        x_ac_bar = self.x_ac_bar_wing
        # ((1.8 * self.fuselage_diameter **2 * x_lemac )/ (self.CL_alpha_Ah * self.wing_span * self.mac )) #This would be the fuselage contribution - igor

        # Calculate the stability curve
        sh_s_stability = (
            1.0
            / (
                (self.CL_alpha_h / self.CL_alpha_Ah)
                * (1.0 - self.d_epsilon_d_alpha)
                * (self.lh / self.mac)
                * self.Vh_V  # this is already the sqaured value
            )
            * (x_cg_bar - x_ac_bar - 0.05)
        )
        # Calculate the control curve
        CL_h = -0.35 * self.AR_h ** (1 / 3)
        Cm_ac = (
            self.Cm_ac_wing
        )  # + -1.8*(1-(2.5*self.fuselage_diameter/self.l_fus))*(np.pi*self.fuselage_diameter**2*self.l_fus/(4*self.wing_span*self.mac))* 0.232/self.CL_alpha_Ah

        sh_s_control = (
            1.0
            / (
                (CL_h / self.CL_Aminush) * (self.lh / self.mac) * self.Vh_V
            )  # this is already the sqaured value
        ) * (x_cg_bar + (Cm_ac / self.CL_A_h - x_ac_bar))
        control_slope = 1.0 / (
            (CL_h / self.CL_A_h) * (self.lh / self.mac) * self.Vh_V
        )  # this is already the sqaured value

        return sh_s_control, sh_s_stability, x_cg_bar

    # ─────────────────────────────────────────────────────────────────────────────
    #  Horizontal-tail sizing (scissor plot)
    # ─────────────────────────────────────────────────────────────────────────────
    def scissor_plot_chat(
        self, n_pts: int = 200, static_margin: float = 0.05
    ) -> dict[str, tp.Any]:
        """
        Build data for a full scissor plot that is compatible with the new CG and
        loading-diagram helpers.

        Returns
        -------
        dict
            {
            "x_cg_bar"        : np.ndarray,          # nondimensional CG axis
            "sh_s_stability"  : np.ndarray,          # stability line  S_h/S
            "sh_s_control"    : np.ndarray,          # control line    S_h/S
            "cg_tracks"       : {cfg: np.ndarray},   # CG tracks from loading_diagram_chat
            }
        """

        # 1. Nondimensional CG axis (same span as previous hard-coded limits)
        x_cg_bar = np.linspace(-0.5, 1.5, n_pts)

        # 2.   ——— Stability requirement ———
        # S_h/S ≥ (x_cg_bar − x_ac_bar − SM) / [ (CLα_h / CLα_w) (1−dε/dα) (ℓ_h/ĉ) (Vh/V) ]
        stab_den = (
            (self.CL_alpha_h / self.CL_alpha_Ah)
            * (1.0 - self.d_epsilon_d_alpha)
            * (self.lh / self.mac)
            * self.Vh_V  # already the squared velocity ratio
        )
        sh_s_stability = (x_cg_bar - self.x_ac_bar_wing + static_margin) / stab_den
        sh_s_stability_no_margin = (x_cg_bar - self.x_ac_bar_wing) / stab_den

        # 3.   ——— Control requirement ———
        # Tail CL in a pull-up is approximated as −0.35 AR_h^(1/3)
        CL_h = -0.35 * self.AR_h ** (1.0 / 3.0)
        CL_Ah = self.CL_A_h  # aircraft lift coeff. (wing + body – tail)
        Cm_ac = self.Cm_ac_wing  # aerodynamic-centre moment coefficient

        ctrl_den = (CL_h / CL_Ah) * (self.lh / self.mac) * self.Vh_V
        sh_s_control = (x_cg_bar + (Cm_ac / CL_Ah - self.x_ac_bar_wing)) / ctrl_den

        # 4. Fetch the *actual* CG tracks so the user can plot them together
        cg_tracks: dict[str, np.ndarray] = {}
        ld_results = self.loading_diagram_chat(n_pts=n_pts)
        for cfg, data in ld_results.items():
            cg_tracks[cfg] = data["x_cg_bar"]  # already nondimensional

        # 5. Return everything nicely packaged
        return {
            "x_cg_bar": x_cg_bar,
            "sh_s_stability": sh_s_stability,
            "sh_s_stability_no_margin": sh_s_stability_no_margin,
            "sh_s_control": sh_s_control,
            "cg_tracks": cg_tracks,
        }

    # ---------------------------------------------------------------------#
    # Convenience getters                                                  #
    # ---------------------------------------------------------------------#

    def get_all(self) -> dict[str, Any]:
        """Return a *copy* of the output dictionary for external consumption."""
        return self._outputs.copy()

    # ---------------------------------------------------------------------#
    # Private helpers                                                      #
    # ---------------------------------------------------------------------#

    def _tau_from_ca_over_c(self, ratio) -> float:
        """Interpolate elevator effectiveness τ for the configured cₐ/c ratio."""
        data = np.loadtxt(self.EFFECTIVENESS_FILE, delimiter=",", skiprows=0)
        ca_c, tau = data.T
        return float(np.interp(ratio, ca_c, tau))


# ---------------------------------------------------------------------------#
# Basic sanity check                                                         #
# ---------------------------------------------------------------------------#
if __name__ == "__main__":  # pragma: no cover

    # from DetailedDesign.funny_inputs import structures_funny_inputs as fi
    from DetailedDesign.inputs import constants_inputs as constantsi
    from DetailedDesign.inputs import requirements_inputs as requirementsi
    from DetailedDesign.inputs import uav_inputs as auvi

    # from DetailedDesign.inputs import hardware_inputs as hi
    # from DetailedDesign.inputs import component_locations as pi
    from DetailedDesign.inputs import deployment_inputs as di
    from DetailedDesign.inputs import propulsion_inputs as propi
    from DetailedDesign.inputs import stab_n_con_inputs as sci

    inputs = {}
    inputs.update(constantsi)
    inputs.update(requirementsi)
    inputs.update(auvi)
    # inputs.update(hi)
    # inputs.update(pi)
    inputs.update(di)
    inputs.update(propi)
    inputs.update(sci)
    stabcon = StabCon(inputs)

    stabcon.size_ailerons()
    print("Ailerons sized successfully.")
    p_achieved, bo, Cl_delta_a, Cl_p = stabcon.size_ailerons()
    print(
        f"Achieved roll rate: {np.rad2deg(p_achieved):.3f} deg/s with bo = {bo:.3f} m\n"
        f"Cl_delta_a = {Cl_delta_a:.3f} and Cl_p = {Cl_p:.3f}"
    )

    # ─────────────────────────────────────────────────────────────────────────────
    # 1. Centre-of-gravity report
    # ─────────────────────────────────────────────────────────────────────────────
    cg_results = stabcon.calculate_uav_cg_chat()

    for cfg, res in cg_results.items():
        print(f"\n{cfg.upper()} configuration:")
        print(f"  Fuselage mass : {res['fuselage_mass']:.3f}  kg")
        print(f"  Fuselage CG x : {res['fuselage_x_cg']:.3f}  m")
        print(f"  Wing mass     : {res['wing_mass']:.3f}  kg")
        print(f"  Wing CG   x   : {res['wing_x_cg']:.3f}  m")

    # ─────────────────────────────────────────────────────────────────────────────
    # 2. Loading diagram (uses calculate_uav_cg_chat internally)
    # ─────────────────────────────────────────────────────────────────────────────
    loading_results = (
        stabcon.loading_diagram_chat()
    )  # optional: loading_diagram(n_pts=15)

    for cfg, data in loading_results.items():
        x_vals = data["x_cg_bar"]  # non-dimensional CG position
        y_vals = data["x_lemac"] / stabcon.l_fus  # LEMAC position / fuselage length
        plt.plot(x_vals, y_vals, label=f"{cfg} config")

    plt.xlabel("Non-dimensional CG position, $(x_{cg}-x_{LE})/\\bar c$")
    plt.ylabel("LEMAC / fuselage length, $x_{LE}/l_{fus}$")
    plt.title("Longitudinal Loading Diagram")
    plt.xlim(-0.5, 1.5)
    plt.grid(True)
    plt.legend()
    plt.show()

    sc_data = stabcon.scissor_plot_chat()

    # Plot the two sizing curves
    plt.plot(
        sc_data["x_cg_bar"],
        sc_data["sh_s_stability"],
        "k--",
        label="Stability + 5% Static Margin",
    )
    plt.plot(
        sc_data["x_cg_bar"],
        sc_data["sh_s_stability_no_margin"],
        "k:",
        label="Stability",
    )
    plt.plot(sc_data["x_cg_bar"], sc_data["sh_s_control"], "k-", label="Control")

    # Overlay the CG tracks for each payload case
    for cfg, track in sc_data["cg_tracks"].items():
        plt.plot(
            track, sc_data["x_cg_bar"], label=f"{cfg} CG track"
        )  # y-axis is same x_cg_bar

    plt.xlabel("Non-dimensional CG position, $(x_{cg}-x_{LE})/\\bar c$")
    plt.ylabel("$S_h/S$ or CG track")
    plt.title("Scissor Plot with CG Tracks")
    plt.xlim(-0.5, 1.5)
    plt.ylim(0, 1.5)
    plt.grid(True)
    plt.legend()
    plt.show()

    """

    # Generate the scissor plot
    plt.plot(stabcon.scissor_plot()[2], stabcon.scissor_plot()[0], label="Control")
    plt.plot(stabcon.scissor_plot()[2], stabcon.scissor_plot()[1], label="Stability")
    plt.xlabel("Non-dimensional CG position (x_cg_bar)")
    plt.ylabel("Sh/S")
    plt.title("Scissor Plot")
    plt.axhline(0, color="black", linestyle="--", linewidth=0.5)
    plt.axvline(0, color="black", linestyle="--", linewidth=0.5)
    plt.legend()
    plt.grid()
    plt.xlim(-0.5, 1.5)
    plt.ylim(0, 1)
    plt.show()
    print(
        "Scissor plot generated successfully. Now overlay the graphs to find the optimal tail size and determine LEMAC position"
    )

    user_input = float(input("Please enter the x_lemac/fuselage_length: "))
    user_input2 = float(input("Please enter the x_cg_bar: "))
    x_cg_location = user_input * stabcon.l_fus + user_input2 * stabcon.mac
    print(f"The x_cg location is: {x_cg_location:.3f} m")

    # print(stabcon.size_vertical_tailplane())
    # print("Vertical tailplane area: ", stabcon.size_vertical_tailplane()[0])
    # print("Vertical tailplane span: ", stabcon.size_vertical_tailplane()[1])
    # print("Vertical tailplane MAC: ", stabcon.size_vertical_tailplane()[2])
    # print("Vertical tailplane root chord: ", stabcon.size_vertical_tailplane()[3])
    # print("Vertical tailplane tip chord: ", stabcon.size_vertical_tailplane()[4])
    """
