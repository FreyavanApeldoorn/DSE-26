'''
This is the file for the propulsion and power subsystem. It contains a single class.
'''

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

import numpy as np


class Power:

    def __init__(self, inputs: dict[str, float], hardware=None) -> None:
        self.inputs = inputs
        self.outputs = self.inputs.copy()
        self.hardware = hardware

        self.M_to = inputs["M_to"]
        self.DOD_fraction = self.inputs["DOD_fraction"] 
        self.specific_energy = inputs["battery_specific_energy"] 
        self.eta_battery = self.inputs["eta_battery"]  # battery efficiency

        self.time_cruise = inputs["time_cruise_max"]
        self.time_ascent = inputs["time_ascent"]
        self.time_descent = inputs["time_descent"]
        self.time_deploy = inputs["time_deploy"]
        self.time_transition = inputs["time_transition"]
        self.time_scan = inputs["time_scan"]
        self.time_idle = inputs["time_turnaround"]

        
        self.power_ascent = inputs["power_required_VTOL"]
        self.power_descent = inputs["power_required_hover"]  # assuming hover power is used for descent
        self.power_deploy = inputs["power_deploy"]
        self.power_transition = inputs["power_transition"]
        self.power_scan = inputs["power_scan"]
        self.power_idle = inputs["power_idle"]
        self.power_cruise_hardware = inputs["power_cruise_hardware"]  # Power required for cruise operations from hardware

        self.power_required_VTOL = inputs["power_required_VTOL"]  # Power required for VTOL operations
        self.power_required_cruise = inputs["power_required_cruise"]  # Power required for cruise operations
        self.power_required_hover = inputs["power_required_hover"]  # Power required for hover operations

        #Calculate the total power 
        self.power_scan_total = self.power_scan + self.power_required_VTOL
        self.power_deploy_total = self.power_deploy + self.power_required_VTOL
        self.power_cruise_total = self.power_cruise_hardware + self.power_required_cruise

    # ~~~ Intermediate Functions ~~~
    def power_consumptions_motors(self) -> float:

        return

    def calculate_required_capacity(self) -> float:
        
        
        times = np.array([
            self.time_cruise,
            self.time_ascent,
            self.time_descent,
            self.time_deploy,
            self.time_transition,
            self.time_scan,
            self.time_idle
        ])
        powers = np.array([
            self.power_cruise_total,
            self.power_ascent,
            self.power_descent,
            self.power_deploy_total,
            self.power_transition,
            self.power_scan_total,
            self.power_idle

        ])

        self.trip_capacity = np.sum(times * powers)
        self.trip_capacity_wh = self.trip_capacity / 3600


    def old_calculate_battery_mass(self) -> float:
        '''
        This calculates the required battery mass given mission energy and constraints
        '''
        self.calculate_required_capacity()   # calculated the required capacity in Wh
        E_required_Wh = self.required_capacity_wh

        E_battery = E_required_Wh / 3600 / (self.eta_battery * self.DOD_fraction) # convert J to Wh and consider efficiency and depth of discharge
        #Use formula from research paper to determine battery mass
        a = 4.04
        b = 139
        c = 0.0155
    
        discriminant = b**2 - 4 * a * (c - E_battery)

        if discriminant < 0:
            raise ValueError("No real solution for the given energy input.")

        M_battery = (-b + (discriminant)**(1/2)) / (2 * a)
        M_battery = E_battery / 240  # assume different specific energy density of 240 Wh/kg

        max_battery_frac = 0.35
        max_battery_mass = max_battery_frac * self.M_to # Maximum battery mass is 40% of MTOW
        battery_mass = min(M_battery, max_battery_mass) 

        return battery_mass
    
    def calculate_battery_mass(self) -> float:
        
        MF_battery = self.trip_capacity_wh / (self.specific_energy * self.eta_battery * self.DOD_fraction * self.M_to)
        self.battery_mass = MF_battery * self.M_to




    def calculate_max_power(self) -> float:
        pass



    # ~~~ Output functions ~~~ 


    def get_all(self) -> dict[str, float]:

        # These are all the required outputs for this class. Plz consult the rest if removing any of them!

        self.calculate_required_capacity()
        self.calculate_battery_mass()

        self.outputs["mass_battery"] = self.battery_mass # if self.hardware["battery_mass"] is None else self.hardware["battery_mass"]
        self.outputs["required_capacity_wh"] = self.trip_capacity_wh
        self.outputs["battery_capacity"] = self.trip_capacity_wh   # updated true capacity (might increase after choosing a battery)

        return self.outputs

    
if __name__ == '__main__': # pragma: no cover
    # Perform sanity checks here
    
    inputs = {
        "time_cruise": 1440.0,  # seconds
        "time_ascent": 40.0,  # seconds
        "time_descent": 80.0,  # seconds
        "time_deploy": 130.0,  # seconds
        "time_transition": 30,  # seconds
        "time_scan": 60,  # seconds
        "time_turnaround": 60.0,  # seconds
        "power_cruise": 1849.5497559983473,  # Watts
        "power_ascent": 3475.137999774786,  # Watts
        "power_descent": 23186.135304507123,  # Watts
        "power_deploy": 3475.137999774786+96.0,  # Watts
        "power_transition": 3475.137999774786+1849.5497559983473,  # Watts
        "power_scan": 23186.135304507123,  # Watts
        "power_idle": 100,  # Watts
        "DOD_fraction": 0.8,  # Depth of discharge fraction
        "eta_battery": 0.9,  # Battery efficiency
        "M_to": 30,  # Maximum Takeoff Mass [kg]
    }
    power = Power(inputs)
    outputs = power.get_all()
    print("Battery mass:", outputs["Battery_mass"], "kg")
    print("Battery volume:", outputs["Battery_volume"], "m^3")
    print("Battery capacity:", outputs["Battery_capacity"], "Wh")