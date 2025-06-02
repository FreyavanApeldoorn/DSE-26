'''
This is the file for the thermal subsystem. It contains a single class.
'''

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

import numpy as np
import math
import matplotlib.pyplot as plt

class Thermal:
    
    def __init__(self, inputs: dict[str, float]) -> None:
        self.inputs = inputs
        self.outputs = self.inputs.copy()

        # Hot-region ambient temperature (°C)
        self.T_amb_hot = inputs["T_amb_hot"]
        # Cruise-region ambient temperature (°C)
        self.T_amb_cruise = inputs["T_amb_cruise"]
        # Initial internal temperature before hot region (°C)
        self.T_int_init = inputs["T_int_init"]
        # Cruise internal set-point after hot region (°C)
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

        # Exposure time in hot region (s)
        self.t_exposure = inputs["t_exposure"]
        # Cruise leg duration (s) for both outbound and return
        self.t_cruise = inputs.get("t_cruise", 12*60)  
        # Maximum cooler power available (W)
        self.Q_cooler = inputs.get("Q_cooler", 0.0)       # Maximum cooler capacity (W)

    # ~~~ Intermediate Functions ~~~

    def _compute_resistances(self) -> float:
        '''Compute total thermal resistance (K/W).'''
        R_Ti = self.t_shell / (self.k_Ti * self.A_heat_shell)
        R_ins = (self.t_insulation / (self.k_insulation * self.A_heat_shell)) if self.include_insulation else 0.0
        R_conv = 1.0 / (self.heat_coeff_ext * self.A_heat_shell)
        return R_Ti + R_ins + R_conv

    # ~~~ Output functions ~~~

    def get_cruise_cooling_power(self) -> float:
        '''Cooling power (W) to hold cruise set-point at cruise ambient.'''
        R_tot = self._compute_resistances()
        return self.heat_int + (self.T_amb_cruise - self.T_int_cruise_set) / R_tot

    def simulate_hot_phase(self, Q_cool: float) -> float:
        '''Simulate the 1-s iterative hot phase and return the exit internal temperature.'''
        R_tot = self._compute_resistances()
        # Compute the steady hold power at T_int_init in hot ambient
        Q_hold_initial = self.heat_int + (self.T_amb_hot - self.T_int_init) / R_tot
        # If max cooler is larger than hold, clamp to hold power (no temperature rise)
        if Q_cool >= Q_hold_initial:
            self.outputs["Hot_hold_power"] = Q_hold_initial
            return self.T_int_init

        # Otherwise run full-power iteration, but clamp each second if overcool
        T_current = self.T_int_init
        for _ in range(int(self.t_exposure)):
            # recompute the hold power at this T_current
            Q_hold = self.heat_int + (self.T_amb_hot - T_current) / R_tot
            if Q_cool >= Q_hold:
                # clamp to Q_hold to keep T_current constant
                self.outputs.setdefault("Hot_hold_power_times", []).append(Q_hold)
                return T_current
            # integrate one second with full Q_cool
            dTdt = (self.heat_int + (self.T_amb_hot - T_current) / R_tot - Q_cool) / (self.m_int * self.c_p_int)
            T_current += dTdt
        return T_current

    def simulate_cruise_phase(self, T_start: float, Q_cool: float, duration: float) -> float:
        '''Simulate cruise-phase (1-s steps) from T_start over given duration, return end T.'''
        R_tot = self._compute_resistances()
        T_current = T_start
        for _ in range(int(duration)):
            dTdt = (self.heat_int + (self.T_amb_cruise - T_current) / R_tot - Q_cool) / (self.m_int * self.c_p_int)
            T_current += dTdt
        return T_current

    def get_hot_region_exit_temperature(self) -> float:
        '''Compute exit temperature from hot-zone under fixed max cooler power.'''
        return self.simulate_hot_phase(self.Q_cooler)

    def get_cooling_time_to_cruise_set(self) -> float:
        '''Iteratively compute time (s) to cool from hot exit temp down to cruise set-point under Q_cooler.'''
        T_exit = self.get_hot_region_exit_temperature()
        R_tot = self._compute_resistances()
        T_current = T_exit
        time_elapsed = 0.0
        while T_current > self.T_int_cruise_set:
            dTdt = (self.heat_int + (self.T_amb_cruise - T_current) / R_tot - self.Q_cooler) / (self.m_int * self.c_p_int)
            if dTdt >= 0:
                return math.inf
            T_current += dTdt
            time_elapsed += 1.0
        return time_elapsed

    def get_required_cooler_for_zero_gain(self, tol: float = 0.1) -> float:
        '''
        Find minimum cooler power (W) such that, with a mission profile:
          - Cruise out uses cruise-set cooling (just enough to hold T_int_init)
          - Hot region and cruise return both run at this cooler power
        the final internal temperature equals the initial temperature.
        '''
        def mission_end_temp(Q_trial: float) -> float:
            # 1) Cruise-out: hold initial temp at cruise ambient using just enough power
            Q_cruise_hold = self.get_cruise_cooling_power()
            T_mid = self.simulate_cruise_phase(self.T_int_init, Q_cruise_hold, self.t_cruise)
            # 2) Hot region: run at Q_trial
            T_mid = self.simulate_hot_phase(Q_trial)
            # 3) Cruise back: continue at Q_trial
            T_end = self.simulate_cruise_phase(T_mid, Q_trial, self.t_cruise)
            return T_end

        # Bounds: Q_low=0, Q_high large enough so T_end < T_int_init
        Q_low, Q_high = 0.0, self.heat_int + (self.T_amb_hot - self.T_int_init) / self._compute_resistances() + 1000.0
        T_low = mission_end_temp(Q_low)
        T_high = mission_end_temp(Q_high)
        if T_low <= self.T_int_init:
            return 0.0
        if T_high > self.T_int_init:
            return math.inf
        while Q_high - Q_low > tol:
            Q_mid = 0.5 * (Q_low + Q_high)
            T_mid = mission_end_temp(Q_mid)
            if T_mid > self.T_int_init:
                Q_low = Q_mid
            else:
                Q_high = Q_mid
        return 0.5 * (Q_low + Q_high)

    def get_all(self) -> dict[str, float]:
        '''Compute and return all thermal outputs (including required cooler power for zero net gain).'''
        self.outputs["Thermal_mass"] = self.m_int * self.c_p_int
        self.outputs["Cooling_power_cruise"] = self.get_cruise_cooling_power()
        self.outputs["Cooling_power_hot"] = self.Q_cooler
        self.outputs["T_exit_hot"] = self.get_hot_region_exit_temperature()
        self.outputs["Cooling_time_to_cruise_set"] = self.get_cooling_time_to_cruise_set()
        self.outputs["Required_cooler_zero_gain"] = self.get_required_cooler_for_zero_gain()
        return self.outputs

if __name__ == '__main__': 
    # Sanity check with example inputs
    example_inputs = {
        "T_amb_hot": 140.0,
        "T_amb_cruise": 45.0,
        "T_int_max": 60.0,
        "T_int_init": 30.0,
        "T_int_cruise_set": 30.0,
        "A_heat_shell": 0.5,
        "t_shell": 0.002,
        "k_Ti": 6.7,
        "include_insulation": True,
        "t_insulation": 0.01,
        "k_insulation": 0.017,
        "heat_coeff_ext": 45.0,
        "heat_int": 200.0,
        "m_int": 5.0,
        "c_p_int": 500.0,
        "t_exposure": 600.0,
        "t_cruise": 12*60,
        "Q_cooler": 300.0
    }
    thermal = Thermal(example_inputs)
    outputs = thermal.get_all()
    # Print each output on its own line
    for key, value in outputs.items():
        print(f"{key}: {value}")

    # --- Simulation and plotting ---
    dt = 1.0  # s interval
    phases = [("cruise", example_inputs["t_cruise"]), ("hot", example_inputs["t_exposure"]), ("cruise", example_inputs["t_cruise"])]
    times, temps, power_req = [], [], []
    T = example_inputs["T_int_init"]
    R_tot = thermal._compute_resistances()
    Q_cruise_hold = outputs["Cooling_power_cruise"]

    for phase, duration in phases:
        if phase == "cruise":
            # Determine if outbound or inbound based on time index
            for _ in range(int(duration / dt)):
                current_time = len(times) * dt
                times.append(current_time)

                if current_time < example_inputs["t_cruise"]:
                    # Outbound cruise: hold at initial temp
                    T_amb = example_inputs["T_amb_cruise"]
                    Q_command = Q_cruise_hold
                else:
                    # Inbound cruise: run max cooler until back to initial temp, then hold
                    T_amb = example_inputs["T_amb_cruise"]
                    if T > example_inputs["T_int_init"]:
                        Q_command = example_inputs["Q_cooler"]
                    else:
                        Q_command = Q_cruise_hold

                dTdt = (example_inputs["heat_int"] + (T_amb - T) / R_tot - Q_command) / (example_inputs["m_int"] * example_inputs["c_p_int"])
                T += dTdt * dt
                temps.append(T)
                power_req.append(Q_command)

        elif phase == "hot":
            for _ in range(int(duration / dt)):
                current_time = len(times) * dt
                times.append(current_time)
                T_amb = example_inputs["T_amb_hot"]
                # clamp logic in hot phase
                Q_hold = example_inputs["heat_int"] + (T_amb - T) / R_tot
                if example_inputs["Q_cooler"] >= Q_hold:
                    Q_command = Q_hold
                    temps.append(T)
                    power_req.append(Q_command)
                    continue
                # Otherwise use full cooler power
                Q_command = example_inputs["Q_cooler"]
                dTdt = (example_inputs["heat_int"] + (T_amb - T) / R_tot - Q_command) / (example_inputs["m_int"] * example_inputs["c_p_int"])
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

    # Plot commanded cooling power over mission
    plt.figure()
    plt.plot(times, power_req)
    plt.xlabel('Time (s)')
    plt.ylabel('Commanded Cooling Power (W)')
    plt.title('Cooling Power Demand Over Mission')
    plt.savefig('DetailedDesign/subsystems/Plots/power_demand_cooler.png')  