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

from DetailedDesign.funny_inputs import constants_funny_inputs as constantsi
from DetailedDesign.funny_inputs import stab_n_con_funny_inputs as fi

# from DetailedDesign.funny_inputs import structures_funny_inputs as fi
from DetailedDesign.inputs import hardware_inputs as hi
from DetailedDesign.inputs import component_locations as pi
from DetailedDesign.inputs import deployment_inputs as di
from DetailedDesign.inputs import propulsion_inputs as propi
from DetailedDesign.inputs import stab_n_con_inputs as sci


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
        self.wing_root_chord = inputs["wing_root_chord"]
        self.wing_tip_chord = inputs["wing_tip_chord"]
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
        # self.Propeller_diameter_VTOL = inputs["Propeller_diameter_VTOL"]
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
        # Make a *copy* of the inputs dict so we do not mutate the caller’s data.
        self._outputs: dict[str, Any] = inputs.copy()

        self.oil_sensor_mass = inputs["oil_sensor_mass"]
        self.oil_sensor_x = inputs["oil_sensor_x"]
        self.oil_sensor_y = inputs["oil_sensor_y"]
        self.oil_sensor_z = inputs["oil_sensor_z"]
        self.wildfire_sensor_mass = inputs["wildfire_sensor_mass"]
        self.wildfire_sensor_x = inputs["wildfire_sensor_x"]
        self.wildfire_sensor_y = inputs["wildfire_sensor_y"]
        self.wildfire_sensor_z = inputs["wildfire_sensor_z"]
        self.gymbal_connection_mass = inputs["gymbal_connection_mass"]
        self.gymbal_connection_x = inputs["gymbal_connection_x"]
        self.gymbal_connection_y = inputs["gymbal_connection_y"]
        self.gymbal_connection_z = inputs["gymbal_connection_z"]
        self.flight_controller_mass = inputs["flight_controller_mass"]
        self.flight_controller_x = inputs["flight_controller_x"]
        self.flight_controller_y = inputs["flight_controller_y"]
        self.flight_controller_z = inputs["flight_controller_z"]
        self.OBC_mass = inputs["OBC_mass"]
        self.OBC_x = inputs["OBC_x"]
        self.OBC_y = inputs["OBC_y"]
        self.OBC_z = inputs["OBC_z"]
        self.GPS_mass = inputs["GPS_mass"]
        self.GPS_x = inputs["GPS_x"]
        self.GPS_y = inputs["GPS_y"]
        self.GPS_z = inputs["GPS_z"]
        self.Mesh_network_module_mass = inputs["Mesh_network_module_mass"]
        self.Mesh_network_module_x = inputs["Mesh_network_module_x"]
        self.Mesh_network_module_y = inputs["Mesh_network_module_y"]
        self.Mesh_network_module_z = inputs["Mesh_network_module_z"]
        self.SATCOM_module_mass = inputs["SATCOM_module_mass"]
        self.SATCOM_module_x = inputs["SATCOM_module_x"]
        self.SATCOM_module_y = inputs["SATCOM_module_y"]
        self.SATCOM_module_z = inputs["SATCOM_module_z"]
        self.Winch_motor_mass = inputs["Winch_motor_mass"]
        self.Winch_motor_x = inputs["Winch_motor_x"]
        self.Winch_motor_y = inputs["Winch_motor_y"]
        self.Winch_motor_z = inputs["Winch_motor_z"]
        self.payload_mass = inputs["payload_mass"]
        self.payload_x = inputs["payload_x"]
        self.payload_y = inputs["payload_y"]
        self.payload_z = inputs["payload_z"]
        self.motor_mass_cruise = inputs["motor_mass_cruise"]
        self.motor_cruise_x = inputs["motor_cruise_x"]
        self.motor_cruise_y = inputs["motor_cruise_y"]
        self.motor_cruise_z = inputs["motor_cruise_z"]
        self.propeller_mass_cruise = inputs["propeller_mass_cruise"]
        # self.propeller_cruise_x = inputs['propeller_cruise_x']
        # self.propeller_cruise_y = inputs['propeller_cruise_y']
        # self.propeller_cruise_z = inputs['propeller_cruise_z']
        self.motor_mass_VTOL = inputs["motor_mass_VTOL"]
        self.motor_front_VTOL_x = inputs["motor_front_VTOL_x"]
        # self.motor_front_VTOL_y = inputs['motor_front_VTOL_y']
        # self.motor_front_VTOL_z = inputs['motor_front_VTOL_z']
        self.motor_rear_VTOL_x = inputs["motor_rear_VTOL_x"]
        # self.motor_rear_VTOL_y = inputs['motor_rear_VTOL_y']
        # self.motor_rear_VTOL_z = inputs['motor_rear_VTOL_z']
        self.propeller_mass_VTOL = inputs["propeller_mass_VTOL"]
        # self.propeller_VTOL_x = inputs['propeller_VTOL_x']
        # self.propeller_VTOL_y = inputs['propeller_VTOL_y']
        # self.propeller_VTOL_z = inputs['propeller_VTOL_z']
        self.battery_mass = inputs["battery_mass"]
        self.battery_x = inputs["battery_x"]
        self.battery_y = inputs["battery_y"]
        self.battery_z = inputs["battery_z"]
        self.PDB_mass = inputs["PDB_mass"]
        self.PDB_x = inputs["PDB_x"]
        self.PDB_y = inputs["PDB_y"]
        self.PDB_z = inputs["PDB_z"]
        self.buoy_mass = inputs["buoy_mass"]
        self.buoy_x = inputs["buoy_x"]
        self.buoy_y = inputs["buoy_y"]
        self.buoy_z = inputs["buoy_z"]
        self.wildfire_fuselage_x_cg = inputs["wildfire_fuselage_x_cg"]
        self.oil_spill_fuselage_x_cg = inputs["oil_spill_fuselage_x_cg"]
        self.wildfire_wing_x_cg = inputs["wildfire_wing_x_cg"]
        self.oil_spill_wing_x_cg = inputs["oil_spill_wing_x_cg"]
        self.wildfire_fuselage_mass = inputs["wildfire_fuselage_mass"]
        self.oil_spill_fuselage_mass = inputs["oil_spill_fuselage_mass"]
        self.wildfire_wing_mass = inputs["wildfire_wing_mass"]
        self.oil_spill_wing_mass = inputs["oil_spill_wing_mass"]
        self.mac = inputs["mac"]
        self.l_fus = inputs["l_fus"]

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
        spanwise_stations = np.linspace(0.0, half_span, 100)
        chord = (
            self.wing_root_chord
            - ((self.wing_root_chord - self.wing_tip_chord) / half_span)
            * spanwise_stations
        )
        print("spanwise_stations =", spanwise_stations)
        print("chord =", chord)
        print("roll_rate_req =", self.roll_rate_req)

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

    # ~~~ Rudder sizing ~~~

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
        for configuration in ["wildfire", "oil_spill"]:
            if configuration == "wildfire":
                sensor_mass = self.wildfire_sensor_mass
                sensor_x = self.wildfire_sensor_x
                sensor_y = self.wildfire_sensor_y
                sensor_z = self.wildfire_sensor_z
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
                + self.payload_mass * self.payload_x
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
                + self.payload_mass
                + buoy_mass
                + self.motor_mass_cruise
                + self.propeller_mass_cruise
                # add structure, tail, landing gear
            )
            print("numerator_x_fuselage =", numerator_x_fuselage)
            print("fuselage_mass =", fuselage_mass)

            fuselage_x_cg = numerator_x_fuselage / fuselage_mass
            print("fuselage_x_cg =", fuselage_x_cg)
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

    # ~~~ Loading diagram ~~~
    def loading_diagram(self) -> tuple[np.ndarray, np.ndarray]:
        x_lemac = np.linspace(0.0, self.l_fus - self.mac, 10)

        results = {}
        for configuration in ["wildfire", "oil_spill"]:
            if configuration == "wildfire":
                fuselage_x_cg = self.wildfire_fuselage_x_cg
                wing_x_cg = self.wildfire_wing_x_cg
                fuselage_mass = self.wildfire_fuselage_mass
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

    # ~~~ Scissor plot ~~~

    def scissor_plot(self) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
        """Return the control & stability curves and the non-dimensional CG track."""
        # Create an array with positions for lemac.
        x_lemac = np.linspace(0.0, self.l_fus - self.mac, 5)

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

    inputs = {}
    inputs.update(constantsi)
    inputs.update(fi)
    inputs.update(hi)
    inputs.update(pi)
    inputs.update(di)
    inputs.update(propi)
    inputs.update(sci)
    stabcon = StabCon(inputs)

    stabcon.size_ailerons()
    print("Ailerons sized successfully.")
    p_achieved, bo = stabcon.size_ailerons()
    print(
        f"Achieved roll rate: {np.rad2deg(p_achieved):.3f} deg/s with bo = {bo:.3f} m"
    )

    """

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

    # CG calculation
    cg_results = stabcon.calculate_UAV_cg()
    for config, result in cg_results.items():
        setattr(stabcon, f"{config}_fuselage_x_cg", result["fuselage_x_cg"])
        setattr(stabcon, f"{config}_wing_x_cg", result["wing_x_cg"])
        setattr(stabcon, f"{config}_fuselage_mass", result["fuselage_mass"])
        setattr(stabcon, f"{config}_wing_mass", result["wing_mass"])

        print(f"\n{config.upper()} configuration:")
        print(f"  Fuselage mass: {result['fuselage_mass']:.3f} kg")
        print(f"  Fuselage CG (x): {result['fuselage_x_cg']:.3f} m")
        print(f"  Wing mass: {result['wing_mass']:.3f} kg")
        print(f"  Wing CG (x): {result['wing_x_cg']:.3f} m")

    loading_results = stabcon.loading_diagram()

    for configuration in ["wildfire", "oil_spill"]:
        if configuration == "wildfire":
            print("wildfire_fuselage_x_cg:", stabcon.wildfire_fuselage_x_cg)
            print("wildfire_wing_x_cg:", stabcon.wildfire_wing_x_cg)
            print("wildfire_fuselage_mass:", stabcon.wildfire_fuselage_mass)
            print("wildfire_wing_mass:", stabcon.wildfire_wing_mass)
        else:
            print("oil_spill_fuselage_x_cg:", stabcon.oil_spill_fuselage_x_cg)
            print("oil_spill_wing_x_cg:", stabcon.oil_spill_wing_x_cg)
            print("oil_spill_fuselage_mass:", stabcon.oil_spill_fuselage_mass)
            print("oil_spill_wing_mass:", stabcon.oil_spill_wing_mass)

    for config in loading_results:
        print(
            f"{config} x_cg_bar: min={np.min(loading_results[config]['x_cg_bar'])}, max={np.max(loading_results[config]['x_cg_bar'])}"
        )
        print(
            f"{config} x_lemac / l_fus: min={np.min(loading_results[config]['x_lemac'] / stabcon.l_fus)}, max={np.max(loading_results[config]['x_lemac'] / stabcon.l_fus)}"
        )

    for config in loading_results:
        x_vals = loading_results[config][
            "x_cg_bar"
        ]  # x-axis: non-dimensional CG position
        y_vals = (
            loading_results[config]["x_lemac"] / stabcon.l_fus
        )  # y-axis: LEMAC / fuselage length
        plt.plot(x_vals, y_vals, label=f"{config} config")

    plt.ylabel("LEMAC / l_fus")
    plt.xlabel("Non-dimensional CG position")
    plt.title("Loading Diagram for Both Configurations")
    plt.legend()
    plt.grid(True)
    plt.xlim(0, 1)
    plt.show()
    """
