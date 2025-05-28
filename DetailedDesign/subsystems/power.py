import numpy as np

'''
This is the file for the propulsion and power subsystem. It contains a single class.
'''



class Power:

    def __init__(self, inputs: dict[str, float]) -> None:
        self.inputs = inputs
        self.outputs = self.inputs.copy()

        self.M_to = inputs["M_to"]
        self.DOD_fraction = self.inputs["DOD_fraction"]
        self.eta_battery = self.inputs["eta_battery"]

        self.time_hover = inputs["time_hover"]
        self.time_cruise = inputs["time_cruise"]
        self.time_ascent = inputs["time_ascent"]
        self.time_descent = inputs["time_descent"]
        self.time_deploy = inputs["time_deploy"]
        self.time_transition = inputs["time_transition"]
        self.time_scan = inputs["time_scan"]
        self.time_idle = inputs["time_idle"]

        self.power_hover = inputs["power_hover"]
        self.power_cruise = inputs["power_cruise"]
        self.power_ascent = inputs["power_ascent"]
        self.power_descent = inputs["power_descent"]
        self.power_deploy = inputs["power_deploy"]
        self.power_transition = inputs["power_transition"]
        self.power_scan = inputs["power_scan"]
        self.power_idle = inputs["power_idle"]


    # ~~~ Intermediate Functions ~~~

    def calculate_required_capacity(self) -> float:
        
        times = np.array([
            self.time_hover,
            self.time_cruise,
            self.time_ascent,
            self.time_descent,
            self.time_deploy,
            self.time_transition,
            self.time_scan,
            self.time_idle
        ])
        powers = np.array([
            self.power_hover,
            self.power_cruise,
            self.power_ascent,
            self.power_descent,
            self.power_deploy,
            self.power_transition,
            self.power_scan,
            self.power_idle
        ])
        self.required_capacity = np.sum(times * powers)
        self.required_capacity_wh = self.required_capacity / 3600


    def calculate_battery_mass(self) -> float:
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

    # ~~~ Output functions ~~~ 

    def get_all(self) -> dict[str, float]:

        # These are all the required outputs for this class. Plz consult the rest if removing any of them!

        self.outputs["Battery_mass"] = self.calculate_battery_mass()
        self.outputs["Battery_volume"] = ...
        self.outputs["Battery_capacity"] = ...   # updated true capacity (might increase after choosing a battery)

        return self.outputs
    
if __name__ == '__main__':
    # Perform sanity checks here
    
    inputs = {

        "time_hover": 60*10,  # seconds
        "time_cruise": 20*60,  # seconds
        "time_ascent": 120,  # seconds
        "time_descent": 120,  # seconds
        "time_deploy": 180,  # seconds
        "time_transition": 60,  # seconds
        "time_scan": 240,  # seconds
        "time_idle": 180,  # seconds
        "power_hover": 100,  # Watts
        "power_cruise": 80,  # Watts
        "power_ascent": 120,  # Watts
        "power_descent": 90,  # Watts
        "power_deploy": 150,  # Watts
        "power_transition": 110,  # Watts
        "power_scan": 130,  # Watts
        "power_idle": 50,  # Watts
        "DOD_fraction": 0.8,  # Depth of discharge fraction
        "eta_battery": 0.9,  # Battery efficiency
        "M_to": 30,  # Maximum Takeoff Mass [kg]
        "battery_energy_density": 240,  # Wh/kg, specific energy density of the battery

    }
    power = Power(inputs)
    outputs = power.get_all()
    print("Battery mass:", outputs["Battery_mass"], "kg")
    print("Battery volume:", outputs["Battery_volume"], "m^3")
    print("Battery capacity:", outputs["Battery_capacity"], "Wh")