'''
This is the file for the thermal subsystem. It contains a single class.
'''

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

import numpy as np
import math
import matplotlib.pyplot as plt
from funny_inputs import funny_inputs


class Thermal:
    
    def __init__(self, inputs: dict[str, float]) -> None:
        self.inputs = inputs
        self.outputs = self.inputs.copy()

        # deploy-region ambient temperature (°C)
        self.T_amb_deploy = inputs["T_amb_deploy"]
        # Cruise-region ambient temperature (°C)
        self.T_amb_cruise = inputs["T_amb_cruise"]
        # Initial internal temperature before deploy region (°C)
        self.T_int_init = inputs["T_int_init"]
        # Cruise internal set-point after deploy region (°C)
        self.T_int_cruise_set = inputs["T_int_cruise_set"]

        # Shell geometry and materials
        self.A_heat_shell = inputs["A_heat_shell"]    # Effective heat-transfer area (m²)
        self.t_shell = inputs["t_shell"]              # Titanium shell thickness (m)
        self.k_Ti = inputs["k_Ti"]                    # Titanium conductivity (W/(m·K))

        # Insulation (optional)
        self.include_insulation = inputs.get("include_insulation", False)
        self.t_insulation = inputs.get("t_insulation", 0.0)    # Insulation thickness (m)
        self.k_insulation = inputs.get("k_insulation", 1.0)    # Insulation conductivity (W/(m·K))

        # Heat loads and coefficients
        self.heat_int = inputs["heat_int"]                # Internal dissipation (W)
        self.heat_coeff_ext = inputs["heat_coeff_ext"]    # External convective coeff. (W/(m²·K))

        # Internal thermal mass
        self.m_int = inputs["m_int"]      # Mass of components (kg)
        self.c_p_int = inputs["c_p_int"]  # Specific heat capacity (J/(kg·K))

        # Exposure time in deploy region (s)
        self.t_exposure = inputs["time_deploy"] + inputs["time_ascent"] + inputs["time_descent"]  # assuming exposure includes ascent and descent phases
        # Cruise leg duration (s) for both outbound and return
        self.t_cruise_max = inputs["time_uav_max"] - self.t_exposure  
        self.t_cruise_min = inputs["time_uav_min"] - self.t_exposure
        # Maximum thermal power available (positive = heating, negative = cooling) (W)
        self.Q_therm = - inputs["power_thermal_required"]     # Maximum heating/cooling capacity (W)


    # ~~~ Intermediate Functions ~~~

    def _compute_resistances(self) -> float:
        '''Compute total thermal resistance (K/W).'''
        R_Ti = self.t_shell / (self.k_Ti * self.A_heat_shell)
        R_ins = (self.t_insulation / (self.k_insulation * self.A_heat_shell)) if self.include_insulation else 0.0
        R_conv = 1.0 / (self.heat_coeff_ext * self.A_heat_shell)
        return R_Ti + R_ins + R_conv

    # ~~~ Output functions ~~~

    def get_cruise_thermal_power(self) -> float:
        '''
        Thermal power (W) to hold cruise set-point at cruise ambient.
        Positive = heating, Negative = cooling.
        '''
        R_tot = self._compute_resistances()
        # In steady-state, 0 = heat_int + (T_amb - T_set)/R_tot + Q_hold
        # So Q_hold = - [heat_int + (T_amb - T_set)/R_tot]
        return - (self.heat_int + (self.T_amb_cruise - self.T_int_cruise_set) / R_tot)

    def simulate_deploy_phase(self, Q_therm: float) -> float:
        '''
        Simulate the 1-s iterative deploy phase and return the exit internal temperature.
        Q_therm > 0 means heating, Q_therm < 0 means cooling.
        '''
        R_tot = self._compute_resistances()
        # Compute the hold power (negative = cooling) at T_int_init in deploy ambient:
        Q_hold_initial = - (self.heat_int + (self.T_amb_deploy - self.T_int_init) / R_tot)
        # If maximum available thermal power is <= Q_hold_initial (i.e. strong enough cooling),
        # clamp at Q_hold_initial so the bay stays at T_int_init
        if Q_therm <= Q_hold_initial:
            self.outputs["deploy_hold_power"] = Q_hold_initial
            return self.T_int_init

        # Otherwise run full-power iteration and clamp each second if over‐heating or over‐cooling
        T_current = self.T_int_init
        for _ in range(int(self.t_exposure)):
            # recompute the instantaneous hold power at this T_current
            Q_hold = - (self.heat_int + (self.T_amb_deploy - T_current) / R_tot)
            # If Q_therm <= Q_hold, then cooling capacity is enough to hold temperature
            if Q_therm <= Q_hold:
                self.outputs.setdefault("deploy_hold_power_times", []).append(Q_hold)
                return T_current
            # Otherwise integrate one second with the available Q_therm
            dTdt = (self.heat_int + (self.T_amb_deploy - T_current) / R_tot + Q_therm) / (
                self.m_int * self.c_p_int
            )
            T_current += dTdt
        return T_current

    def simulate_cruise_phase(self, T_start: float, Q_therm: float, duration: float) -> float:
        '''
        Simulate cruise-phase (1-s steps) from T_start over given duration, return end temperature.
        Q_therm > 0 means heating, Q_therm < 0 means cooling.
        '''
        R_tot = self._compute_resistances()
        T_current = T_start
        for _ in range(int(duration)):
            dTdt = (self.heat_int + (self.T_amb_cruise - T_current) / R_tot + Q_therm) / (
                self.m_int * self.c_p_int
            )
            T_current += dTdt
        return T_current

    def get_deploy_region_exit_temperature(self) -> float:
        '''Compute exit temperature from deploy zone under fixed max thermal power.'''
        return self.simulate_deploy_phase(self.Q_therm)

    def get_time_to_cruise_set(self) -> float:
        '''
        Iteratively compute time (s) to reach cruise set-point from deploy-exit under max thermal power.
        Returns infinity if never reachable.
        '''
        T_exit = self.get_deploy_region_exit_temperature()
        R_tot = self._compute_resistances()
        T_current = T_exit
        time_elapsed = 0.0
        # Determine sign target: if bay above set, we need negative Q_therm to cool; if below, positive to heat.
        while True:
            if abs(T_current - self.T_int_cruise_set) < 1e-6:
                return time_elapsed
            # Compute instantaneous hold power at this T_current in cruise ambient
            Q_hold = - (self.heat_int + (self.T_amb_cruise - T_current) / R_tot)
            # If T_current > set and Q_therm >= Q_hold (i.e. heating or insufficient cooling), cannot reach from above
            if T_current > self.T_int_cruise_set and self.Q_therm >= Q_hold:
                return math.inf
            # If T_current < set and Q_therm <= Q_hold (i.e. cooling or insufficient heating), cannot reach from below
            if T_current < self.T_int_cruise_set and self.Q_therm <= Q_hold:
                return math.inf
            # Otherwise integrate one second
            dTdt = (self.heat_int + (self.T_amb_cruise - T_current) / R_tot + self.Q_therm) / (
                self.m_int * self.c_p_int
            )
            T_current += dTdt
            time_elapsed += 1.0

            # If we cross the set-point exactly, stop
            if (dTdt < 0 and T_current <= self.T_int_cruise_set) or (dTdt > 0 and T_current >= self.T_int_cruise_set):
                return time_elapsed

    def get_required_thermal_for_zero_gain(self, tol: float = 0.1) -> float:
        '''
        Find minimum thermal power (W) such that, over the mission:
          • Outbound cruise holds at T_int_init
          • deploy zone and return cruise both run at this constant power
        the final internal temperature equals the initial temperature.
        Positive output = heating rating; negative = cooling rating.
        '''
        def mission_end_temp(Q_trial: float) -> float:
            # 1) Outbound cruise: hold initial temp at cruise using just enough power
            Q_cruise_hold = self.get_cruise_thermal_power()
            T_mid = self.simulate_cruise_phase(self.T_int_init, Q_cruise_hold, self.t_cruise_min)
            # 2) deploy zone: run at Q_trial
            T_mid = self.simulate_deploy_phase(Q_trial)
            # 3) Return cruise: run at Q_trial
            T_end = self.simulate_cruise_phase(T_mid, Q_trial, self.t_cruise_min)
            return T_end

        # We search Q_trial between Q_low=0 (no active heating/cooling) and Q_high negative (strong cooling)
        R_tot = self._compute_resistances()
        Q_low = 0.0
        T_low = mission_end_temp(Q_low) - self.T_int_init  # positive means bay ends above initial
        # Large negative bound for strong cooling
        Q_high = - (abs(self.heat_int + (self.T_amb_deploy - self.T_int_init) / R_tot) + 1000.0)
        T_high = mission_end_temp(Q_high) - self.T_int_init  # negative means bay ends below initial

        # If no-power case already ends at or below initial, zero active power needed
        if T_low <= 0:
            return 0.0
        # If even strongest cooling cannot bring below initial, impossible
        if T_high > 0:
            return math.inf

        # Bisection between Q_low (>=0) and Q_high (<0)
        while abs(Q_high - Q_low) > tol:
            Q_mid = 0.5 * (Q_low + Q_high)
            T_mid = mission_end_temp(Q_mid) - self.T_int_init
            if T_mid > 0:
                Q_low = Q_mid
            else:
                Q_high = Q_mid
        return 0.5 * (Q_low + Q_high)

    def get_all(self) -> dict[str, float]:
        '''Compute and return all thermal outputs (including required thermal rating for zero net gain).'''
        self.outputs["Thermal_mass"] = self.m_int * self.c_p_int
        self.outputs["Thermal_power_cruise"] = self.get_cruise_thermal_power()
        self.outputs["Thermal_power_deploy"] = self.Q_therm
        self.outputs["T_exit_deploy"] = self.get_deploy_region_exit_temperature()
        self.outputs["Time_to_cruise_set"] = self.get_time_to_cruise_set()
        self.outputs["Required_thermal_zero_gain"] = self.get_required_thermal_for_zero_gain()
        
        # self.outputs["thickness_insulation"] = None



        self.outputs["power_thermal_required"] = - self.get_required_thermal_for_zero_gain()  # Maximum thermal power rating (W)
        self.outputs["max_required_energy_thermal"] = None  # max required energy for thermal at max range (Wh)

        return self.outputs


if __name__ == '__main__':
    # Sanity check with example inputs:

    thermal = Thermal(funny_inputs)
    outputs = thermal.get_all()
    # Print each output on its own line
    for key, value in outputs.items():
        print(f"{key}: {value}")

    # --- Simulation and plotting ---
    dt = 1.0  # s interval
    phases = [
        ("cruise", funny_inputs["t_cruise"]),
        ("deploy", funny_inputs["t_exposure"]),
        ("cruise", funny_inputs["t_cruise"])
    ]
    times, temps, power_req = [], [], []
    T = funny_inputs["T_int_init"]
    R_tot = thermal._compute_resistances()
    Q_cruise_hold = outputs["Thermal_power_cruise"]

    for phase, duration in phases:
        if phase == "cruise":
            for _ in range(int(duration / dt)):
                current_time = len(times) * dt
                times.append(current_time)
                if current_time < funny_inputs["t_cruise"]:
                    T_amb = funny_inputs["T_amb_cruise"]
                    Q_command = Q_cruise_hold
                else:
                    T_amb = funny_inputs["T_amb_cruise"]
                    if T > funny_inputs["T_int_init"]:
                        Q_command = funny_inputs["Q_therm"]
                    else:
                        Q_command = Q_cruise_hold
                dTdt = (funny_inputs["heat_int"] + (T_amb - T) / R_tot + Q_command) / (
                    funny_inputs["m_int"] * funny_inputs["c_p_int"]
                )
                T += dTdt * dt
                temps.append(T)
                power_req.append(Q_command)

        elif phase == "deploy":
            for _ in range(int(duration / dt)):
                current_time = len(times) * dt
                times.append(current_time)
                T_amb = funny_inputs["T_amb_deploy"]
                Q_hold = - (funny_inputs["heat_int"] + (T_amb - T) / R_tot)
                if funny_inputs["Q_therm"] <= Q_hold:
                    Q_command = Q_hold
                    temps.append(T)
                    power_req.append(Q_command)
                    continue
                Q_command = funny_inputs["Q_therm"]
                dTdt = (funny_inputs["heat_int"] + (T_amb - T) / R_tot + Q_command) / (
                    funny_inputs["m_int"] * funny_inputs["c_p_int"]
                )
                T += dTdt * dt
                temps.append(T)
                power_req.append(Q_command)

    # Plot internal temperature
    plt.figure()
    plt.plot(times, temps)
    plt.xlabel('Time (s)')
    plt.ylabel('Internal Temperature (°C)')
    plt.title('Internal Temperature Over Mission')
    plt.savefig('DetailedDesign/subsystems/Plots/internal_temperature.png')

    # Plot commanded thermal power over mission
    plt.figure()
    plt.plot(times, power_req)
    plt.xlabel('Time (s)')
    plt.ylabel('Commanded Thermal Power (W)')
    plt.title('Thermal Power Demand Over Mission')
    plt.savefig('DetailedDesign/subsystems/Plots/thermal_power_demand.png')