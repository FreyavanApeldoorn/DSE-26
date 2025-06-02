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
        # Maximum allowable internal temperature (°C)
        self.T_int_max = inputs["T_int_max"]
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

    def get_hot_region_cooling_power(self) -> float:
        '''Steady-state cooling power (W) to maintain the initial internal temperature in hot ambient.'''
        R_tot = self._compute_resistances()
        # Maintain T_int_init at T_amb_hot
        return self.heat_int + (self.T_amb_hot - self.T_int_init) / R_tot

    def get_cooling_time_to_cruise_set(self) -> float:
        '''Time (s) to cool from T_int_init to cruise set-point under cruise cooling.'''
        Q_cruise = self.get_cruise_cooling_power()
        R_tot = self._compute_resistances()
        Q_int = self.heat_int
        T_ss = self.T_amb_cruise - R_tot * (Q_cruise - Q_int)
        if self.T_int_init <= self.T_int_cruise_set:
            return 0.0
        if Q_cruise <= Q_int or T_ss >= self.T_int_cruise_set:
            return math.inf
        tau = self.m_int * self.c_p_int * R_tot
        ratio = (self.T_int_cruise_set - T_ss) / (self.T_int_init - T_ss)
        return -tau * math.log(ratio)

    def get_all(self) -> dict[str, float]:
        '''Compute and return all thermal outputs.'''
        # Thermal mass (J/K)
        self.outputs["Thermal_mass"] = self.m_int * self.c_p_int
        # Cruise-phase cooling
        self.outputs["Cooling_power_cruise"] = self.get_cruise_cooling_power()
        # Hot-region steady cooling to maintain initial internal temp
        self.outputs["Cooling_power_hot"] = self.get_hot_region_cooling_power()
        # Time to cool back to cruise set-point
        self.outputs["Cooling_time_to_cruise_set"] = self.get_cooling_time_to_cruise_set()
        return self.outputs

if __name__ == '__main__': # pragma: no cover
    # Sanity check with example inputs
    example_inputs = {
        "T_amb_hot": 140.0,
        "T_amb_cruise": 45.0,
        "T_int_max": 60.0,
        "T_int_init": 30.0,
        "T_int_cruise_set": 30.0,
        "A_heat_shell": 0.5,
        "t_shell": 0.002,
        "k_Ti": 22.0,
        "include_insulation": True,
        "t_insulation": 0.01,
        "k_insulation": 0.02,
        "heat_coeff_ext": 50.0,
        "heat_int": 200.0,
        "m_int": 5.0,
        "c_p_int": 900.0,
        "t_exposure": 600.0
    }
    thermal = Thermal(example_inputs)
    outputs = thermal.get_all()
    print(outputs)

    # --- Simulation and plotting ---

    # Mission phases: cruise out (12 min), hot region, cruise back (12 min)
    dt = 1.0  # s interval
    phases = [("cruise", 12*60), ("hot", example_inputs["t_exposure"]), ("cruise", 12*60)]
    times, temps, power_req = [], [], []
    T = example_inputs["T_int_init"]
    R_tot = thermal._compute_resistances()
    Q_cruise = outputs["Cooling_power_cruise"]
    Q_hot = outputs["Cooling_power_hot"]

    for phase, duration in phases:
        for _ in range(int(duration/dt)):
            current_time = len(times) * dt
            times.append(current_time)
            # select ambient and commanded cooling
            if phase == "hot":
                T_amb = example_inputs["T_amb_hot"]
                Q_command = Q_hot
            else:
                T_amb = example_inputs["T_amb_cruise"]
                Q_command = Q_cruise
            # update internal temperature
            dTdt = (example_inputs["heat_int"] + (T_amb - T)/R_tot - Q_command) / (example_inputs["m_int"] * example_inputs["c_p_int"])
            T += dTdt * dt
            temps.append(T)
            # compute instantaneous required cooling (for plotting), floored at cruise level
            Q_inst = example_inputs["heat_int"] + (T_amb - T) / R_tot
            power_req.append(max(Q_inst, Q_cruise))

    # Plot internal temperature
    plt.figure()
    plt.plot(times, temps)
    plt.xlabel('Time (s)')
    plt.ylabel('Internal Temperature (°C)')
    plt.title('Internal Temperature Over Mission')
    plt.savefig('DetailedDesign\subsystems\Plots\internal_temperature.png')

    # Plot cooling power required
    plt.figure()
    plt.plot(times, power_req)
    plt.xlabel('Time (s)')
    plt.ylabel('Cooling Power Required (W)')
    plt.title('Cooling Power Over Mission')
    plt.savefig('DetailedDesign\subsystems\Plots\power_required_cooling.png')











    #============================OLD CODE=============================




    """
class Thermal:

    def __init__(self, inputs):
        self.inputs = inputs
        self.outputs = self.inputs.copy()

        self.T_amb = inputs["T_amb"]                #External ambient temperature the UAV is exposed to (°C)
        self.T_int_max = inputs["T_int_max"]        #Maximum allowable internal temperature for the electronics (°C)
        self.T_int_init = inputs["T_int_init"]      #Initial internal temperature UAV
        self.A_heat_shell = inputs["A_heat_shell"]      #Effective heat-transfer area of the shell or panel (m²)
        self.t_shell = inputs["t_shell"]            #Thickness of the titanium shell (m)
        self.k_Ti = inputs["k_Ti"]                 #Thermal conductivity of titanium (W/(m·K))
        self.heat_coeff_ext = inputs["heat_coeff_ext"]            #External convective heat-transfer coefficient (airblast) on the shell (W/(m²·K))
        self.heat_int = inputs["heat_int"]                 #Internal waste heat dissipation from electronics and systems (W)
        self.m_int = inputs["m_int"]                         #Mass of the internal components / thermal mass (kg)
        self.c_p_int = inputs["c_p_int"]                       #Effective specific heat capacity of the internal mass (J/(kg·K))
        self.t_exposure = inputs["t_exposure"]          #Duration spent in the hot environment (s)
        self.include_insulation = inputs["include_insulation"]      #Boolean flag: whether to include an insulation layer in the resistance network
        self.t_insulation = inputs["t_insulation"]                     #Thickness of the insulation layer (m)
        self.k_insulation = inputs["k_insulation"]                 #Thermal conductivity of the insulation material (W/(m·K))
        




    # ~~~ Intermediate Functions ~~~

    def _compute_resistances(self):
        """
        ##Compute thermal resistances: conduction through titanium shell, optional insulation, and external convection.
        ##Returns (R_Ti, R_ins, R_conv, R_tot) in K/W.
"""

        # Titanium conduction resistance

        R_Ti = self.t_shell / (self.k_Ti * self.A_heat_shell)

        # Insulation conduction resistance (if used)
        if self.include_insulation:
            R_ins = self.t_insulation / (self.k_insulation * self.A_heat_shell)
        else:
            R_ins = 0.0

        # External convection resistance
        R_conv = 1.0 / (self.heat_coeff_ext * self.A_heat_shell)

        # Total resistance
        R_tot = R_Ti + R_ins + R_conv

        return R_Ti, R_ins, R_conv, R_tot

    def _compute_steady_state_cooling(self) -> float:
        """
        ##Compute steady-state cooling power required (W) to hold internal at setpoint indefinitely.
"""
        R_Ti, R_ins, R_conv, R_tot = self._compute_resistances()

        return self.heat_int + (self.T_amb - self.T_int_max) / R_tot

    def _compute_transient_cooling(self) -> float:
        """
        ##Compute transient cooling power (W) for limited exposure time.
"""
        R_Ti, R_ins, R_conv, R_tot = self._compute_resistances()

        delta_T_allowed = self.T_int_max - self.T_int_init
        # Average internal temperature during transient
        T_int_avg = self.T_int_max + 0.5 * delta_T_allowed
        # Energy balance over exposure time
        return (self.m_int * self.c_p_int * delta_T_allowed) / self.t_exposure + self.heat_int + (self.T_amb - T_int_avg) / R_tot

    # ~~~ Output functions ~~~ 
    """
    ##def get_all(self) -> dict[str, float]:
        
        # These are all the required outputs for this class. Plz consult the rest if removing any of them!

    ##    outputs["Thermal_mass"] = ...
    ##    outputs["Thermal_power_required"] = ...

    ##    return self.outputs
"""


    def get_all(self) -> dict[str, float]:
        # These are all the required outputs for this class. Plz consult the rest if removing any of them!
        # Compute thermal mass (J/K)
        self.outputs["Thermal_mass"] = self.m_int * self.c_p_int

        # Compute total thermal resistance
        _, _, _, R_tot = self._compute_resistances()
        delta_T_allowed = self.T_int_max - self.T_int_init
        # Choose cooling calculation: transient if time and delta provided, else steady-state
        if self.t_exposure > 0 and delta_T_allowed > 0:
            Q_req = self._compute_transient_cooling()
        else:
            Q_req = self._compute_steady_state_cooling()

        self.outputs["Thermal_power_required"] = Q_req
        return self.outputs

if __name__ == '__main__':
    # Sanity checks:

    sample_inputs = {
        "T_amb": 140.0,            # °C
        "T_int_max": 60.0,         # °C
        "T_int_init": 30,          # °C 
        "A_heat_shell": 0.5,                  # m^2
        "t_shell": 0.002,             # m
        "k_Ti": 22.0,              # W/(m·K)
        "heat_coeff_ext": 50.0,             # W/(m^2·K)
        "heat_int": 200.0,            # W
        "m_int": 5.0,              # kg
        "c_p_int": 900.0,              # J/(kg·K)
        "t_exposure": 600.0,      # s
        "include_insulation": False,
        "t_insulation": 0.01,           # m
        "k_insulation": 0.02           # W/(m·K)
    }
    thermal = Thermal(sample_inputs)
    outputs = thermal.get_all()
    print("Thermal_mass (J/K):", outputs["Thermal_mass"])
    print("Thermal_power_required (W):", outputs["Thermal_power_required"])
"""

