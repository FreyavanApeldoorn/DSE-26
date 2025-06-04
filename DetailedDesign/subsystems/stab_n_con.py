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
from DetailedDesign.inputs import hardware_inputs as hi
from DetailedDesign.inputs import component_locations as pi
from DetailedDesign.inputs import deployment_inputs as di
from DetailedDesign.inputs import propulsion_inputs as propi


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

        self.oil_sensor_mass = inputs['oil_sensor_mass']
        self.oil_sensor_x = inputs['oil_sensor_x']
        self.oil_sensor_y = inputs['oil_sensor_y']
        self.oil_sensor_z = inputs['oil_sensor_z']
        self.wildfire_sensor_mass = inputs['wildfire_sensor_mass']
        self.wildfire_sensor_x = inputs['wildfire_sensor_x']
        self.wildfire_sensor_y = inputs['wildfire_sensor_y']
        self.wildfire_sensor_z = inputs['wildfire_sensor_z']
        self.gymbal_connection_mass = inputs['gymbal_connection_mass']
        self.gymbal_connection_x = inputs['gymbal_connection_x']
        self.gymbal_connection_y = inputs['gymbal_connection_y']
        self.gymbal_connection_z = inputs['gymbal_connection_z']    
        self.flight_controller_mass = inputs['flight_controller_mass']
        self.flight_controller_x = inputs['flight_controller_x']
        self.flight_controller_y = inputs['flight_controller_y']
        self.flight_controller_z = inputs['flight_controller_z']
        self.OBC_mass = inputs['OBC_mass']
        self.OBC_x = inputs['OBC_x']
        self.OBC_y = inputs['OBC_y']
        self.OBC_z = inputs['OBC_z']
        self.GPS_mass = inputs['GPS_mass']
        self.GPS_x = inputs['GPS_x']
        self.GPS_y = inputs['GPS_y']
        self.GPS_z = inputs['GPS_z']
        self.Mesh_network_module_mass = inputs['Mesh_network_module_mass']
        self.Mesh_network_module_x = inputs['Mesh_network_module_x'] 
        self.Mesh_network_module_y = inputs['Mesh_network_module_y']
        self.Mesh_network_module_z = inputs['Mesh_network_module_z']
        self.SATCOM_module_mass = inputs['SATCOM_module_mass']
        self.SATCOM_module_x = inputs['SATCOM_module_x']
        self.SATCOM_module_y = inputs['SATCOM_module_y']
        self.SATCOM_module_z = inputs['SATCOM_module_z']
        self.Winch_motor_mass = inputs['Winch_motor_mass']
        self.Winch_motor_x = inputs['Winch_motor_x']  
        self.Winch_motor_y = inputs['Winch_motor_y']
        self.Winch_motor_z = inputs['Winch_motor_z']
        self.payload_mass = inputs['payload_mass']
        self.payload_x = inputs['payload_x']
        self.payload_y = inputs['payload_y']
        self.payload_z = inputs['payload_z']
        self.motor_mass_cruise = inputs['motor_mass_cruise']
        self.motor_cruise_x = inputs['motor_cruise_x']
        self.motor_cruise_y = inputs['motor_cruise_y']  
        self.motor_cruise_z = inputs['motor_cruise_z']
        self.propeller_mass_cruise = inputs['propeller_mass_cruise']
        #self.propeller_cruise_x = inputs['propeller_cruise_x']
        #self.propeller_cruise_y = inputs['propeller_cruise_y']
        #self.propeller_cruise_z = inputs['propeller_cruise_z']
        self.motor_mass_VTOL = inputs['motor_mass_VTOL']
        self.motor_front_VTOL_x = inputs['motor_front_VTOL_x']  
        #self.motor_front_VTOL_y = inputs['motor_front_VTOL_y']
        #self.motor_front_VTOL_z = inputs['motor_front_VTOL_z']
        self.motor_rear_VTOL_x = inputs['motor_rear_VTOL_x']
        #self.motor_rear_VTOL_y = inputs['motor_rear_VTOL_y']
        #self.motor_rear_VTOL_z = inputs['motor_rear_VTOL_z']
        self.propeller_mass_VTOL = inputs['propeller_mass_VTOL']
        #self.propeller_VTOL_x = inputs['propeller_VTOL_x']
        #self.propeller_VTOL_y = inputs['propeller_VTOL_y']
        #self.propeller_VTOL_z = inputs['propeller_VTOL_z']
        self.battery_mass = inputs['battery_mass']
        self.battery_x = inputs['battery_x']
        self.battery_y = inputs['battery_y']
        self.battery_z = inputs['battery_z']
        self.PDB_mass = inputs['PDB_mass']
        self.PDB_x = inputs['PDB_x']
        self.PDB_y = inputs['PDB_y']
        self.PDB_z = inputs['PDB_z']
        self.buoy_mass = inputs['buoy_mass']
        self.buoy_x = inputs['buoy_x']
        self.buoy_y = inputs['buoy_y']
        self.buoy_z = inputs['buoy_z']          
        


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
                sensor_mass * sensor_x +
                self.gymbal_connection_mass * self.gymbal_connection_x +
                self.flight_controller_mass * self.flight_controller_x +
                self.OBC_mass * self.OBC_x +
                self.GPS_mass * self.GPS_x +
                self.Mesh_network_module_mass * self.Mesh_network_module_x +
                self.SATCOM_module_mass * self.SATCOM_module_x +
                self.Winch_motor_mass * self.Winch_motor_x +
                (self.motor_mass_cruise + self.propeller_mass_cruise) * self.motor_cruise_x +
                self.payload_mass * self.payload_x +
                buoy_mass * buoy_x 
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
                sensor_mass +
                self.gymbal_connection_mass +
                self.flight_controller_mass +
                self.OBC_mass +
                self.GPS_mass +
                self.Mesh_network_module_mass +
                self.SATCOM_module_mass +
                self.Winch_motor_mass +
                self.payload_mass +
                buoy_mass + 
                self.motor_mass_cruise +
                self.propeller_mass_cruise 
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
                2 * (self.motor_mass_VTOL + self.propeller_mass_VTOL) * self.motor_front_VTOL_x +
                2 * (self.motor_mass_VTOL + self.propeller_mass_VTOL) * self.motor_rear_VTOL_x +
                self.battery_mass * self.battery_x +
                self.PDB_mass * self.PDB_x 
                # add wing structure here
            )

            wing_mass = (
                4 * self.motor_mass_VTOL +
                self.battery_mass + 
                self.PDB_mass
                # add wing structure here
            )

            wing_x_cg = numerator_x_wing / wing_mass

            # Save result for this configuration
            results[configuration] = {
                "fuselage_mass": fuselage_mass,
                "wing_mass": wing_mass,
                "fuselage_x_cg": fuselage_x_cg,
                #"fuselage_y_cg": fuselage_y_cg,
                #"fuselage_z_cg": fuselage_z_cg,
                "wing_x_cg": wing_x_cg,
            }

        return results


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
    inputs = {}
    inputs.update(hi)          # Your hardware dict
    inputs.update(pi)
    inputs.update(di)   
    inputs.update(propi)    # Your component locations dict
    stabcon = StabCon(inputs)
    
    # CG calculation
    cg_results = stabcon.calculate_UAV_cg()
    for config, result in cg_results.items():
        print(f"\n{config.upper()} configuration:")
        print(f"  Fuselage mass: {result['fuselage_mass']:.3f} kg")
        print(f"  Fuselage CG (x): {result['fuselage_x_cg']:.3f} m")
        print(f"  Wing mass: {result['wing_mass']:.3f} kg")
        print(f"  Wing CG (x): {result['wing_x_cg']:.3f} m")