'''
This is the file for the propulsion and power subsystem. It contains a single class.
'''



class Power:

    def __init__(self, inputs: dict[str, float]) -> None:
        self.inputs = inputs
        self.outputs = self.inputs.copy()

    # ~~~ Intermediate Functions ~~~

    def calculate_battery_mass(self) -> float:
        '''
        This calculates the required battery mass given mission energy and constraints
        '''
        E_required_Wh = self.inputs["E_required_Wh"]
        DOD_fraction = self.inputs["DOD_fraction"]
        eta_battery = self.inputs["eta_battery"]
        M_to = self.inputs["M_to"]

        E_battery = E_required_Wh / 3600 / (eta_battery * DOD_fraction) # convert J to Wh and consider efficiency and depth of discharge
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
        max_battery_mass = max_battery_frac * M_to # Maximum battery mass is 40% of MTOW
        battery_mass = min(M_battery, max_battery_mass) 

        return battery_mass

    # ~~~ Output functions ~~~ 

    def get_all(self) -> dict[str, float]:

        # These are all the required outputs for this class. Plz consult the rest if removing any of them!

        outputs["Battery_mass"] = ...
        outputs["Battery_volume"] = ...
        outputs["Battery_capacity"] = ...

        return self.outputs
    
if __name__ == '__main__':
    # Perform sanity checks here
    pow = Power(funny_inputs)