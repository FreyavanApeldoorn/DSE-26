import numpy as np

'''
This is the file for the nest. It contains a single class.
'''

class Nest:

    def __init__(self, inputs: dict[str, float], verbose: bool = False) -> None:

        self.verbose = verbose
        self.inputs = inputs
        self.outputs = self.inputs.copy()
        
        # Mission parameters
        self.n_drones = inputs["Number_of_UAVs"]

        # UAV Dimensions 
        self.uav_span = inputs["b_wing"]
        self.uav_wing_area = inputs["S_wing"]
        self.FW_height = inputs["FW_height"]  # height of the fuselage
        self.FW_width = inputs["FW_width"]  # width of the fuselage
        self.uav_chord = self.uav_wing_area / self.uav_span if self.uav_span != 0 else 0 

        self.uav_mass = inputs["M_to"]

        # Aerogel dimensions
        self.aerogel_width = inputs["aerogel_width"]  # width of the aerogel
        self.aerogel_diameter = inputs["aerogel_diameter"]  # diameter of the aerogel

        # Generator parameters
        self.generator_efficiency = inputs["generator_efficiency"]
        self.diesel_energy_density = inputs["diesel_energy_density"]

        # Nest contraints
        #self.nest_energy = inputs["nest_energy"]
        self.nest_length = inputs["nest_length"]
        self.nest_width = inputs["nest_width"]
        self.nest_height = inputs["nest_height"]
        #self.nest_mass = inputs["nest_mass"]

        self.available_volume_per_nest = self.nest_length * self.nest_width * self.nest_height


    def uav_dimensions(self):

        uav_span = self.uav_span
        uav_width_FW = self.FW_width
        uav_heigh_FW = self.FW_height
        v_UAV_FW = uav_span * uav_width_FW * uav_heigh_FW  # m^3

        fuselage_length_margin = 0
        delta_fuselage_length = 0.5
        fuselage_width_margin = 0.5
        uav_fuselage_length = self.aerogel_width * (1 + fuselage_length_margin) + delta_fuselage_length  # m
        uav_fuselage_width = self.aerogel_diameter * (1 + fuselage_width_margin)  # m
        v_UAV_fuselage = uav_fuselage_length * uav_fuselage_width * uav_fuselage_width


        self.uav_volume = v_UAV_FW + v_UAV_fuselage  # m^3


    def generator_sizing(self):
        
        
        #total_energy = self.nest_energy   # required energy in Wh
        total_energy = 1000


        # Generator volume:
        VF_generator = 0.1   # faction of nest volume for generator    
        l_generator = 0.9   # width of generator in m
        height_generator = 1.3

        volume_generator = VF_generator * self.available_volume_per_nest
        self.volume_generator = volume_generator
        l_op = self.nest_length - l_generator   # total length minus generator width
        self.l_op = l_op 

        #mass of generator
        #m_


        # Estimate fuel tank volume based on required energy
        # Assumptions:
        # - Diesel fuel energy density: 35.8 MJ/liter (or 9.94 kWh/liter)
        # - 1 kWh = 3.6 MJ
        # - Generator efficiency is a fraction (e.g., 0.3 for 30%)
        # - Add 10% margin to tank size

        diesel_energy_density_kwh_per_l = 9.94  # kWh/liter
        diesel_energy_density_wh_per_l = diesel_energy_density_kwh_per_l * 1000  # convert to Wh/liter
        margin = 1.1  # 10% margin

        # Calculate required fuel energy input (account for generator efficiency)
        required_fuel_energy_wh = total_energy / self.generator_efficiency

        # Calculate required fuel volume in liters
        fuel_tank_volume_l = (required_fuel_energy_wh / diesel_energy_density_wh_per_l) * margin
        self.fuel_tank_volume = fuel_tank_volume_l

        # mass of 


        # Check if fuel tank can be fitted within width_generator
        if self.fuel_tank_volume > (l_generator * self.nest_width * self.nest_height) - volume_generator:
            print(f"Fuel tank volume: {self.fuel_tank_volume:.2f} liters")
            print(f"Available space in generator compartment: {(l_generator * self.nest_width * self.nest_height) - volume_generator:.2f} liters")
            raise ValueError("Fuel tank volume exceeds available space in the generator compartment.")
        

        self.volume_generator = 5.05


        if self.verbose:
            print(f"Required fuel tank volume: {fuel_tank_volume_l:.2f} liters")


    def misc_sizing(self):

        v_locker = 0.5*0.5
        VF_electronics = 0.05
        VF_equipment = 0.05
        MF_electronics = 0.05
        MF_equipment = 0.05

        self.v_electronics = VF_electronics * self.available_volume_per_nest 
        self.v_equipment = VF_equipment * self.available_volume_per_nest

        self.v_locker = v_locker


        area_human = self.nest_height * 0.6  # m^2
        v_operating_space = area_human * self.l_op
        self.v_operating_space_gen = v_operating_space
        self.v_operating_space_nogen = area_human * self.nest_length

        if self.verbose:
            print(f"Volume of electronics: {self.v_electronics:.2f} m^3")
            print(f"Volume of equipment: {self.v_equipment:.2f} m^3")
            print(f"Volume of locker: {self.v_locker:.2f} m^3")
            print(f"Volume of operating space with generator: {self.v_operating_space_gen:.2f} m^3")
            print(f"Volume of operating space without generator: {self.v_operating_space_nogen:.2f} m^3")



    def uavs_battery_sizing(self):


        # UAVs volume:
        VF_UAV_margin = 0.1   # fraction of UAV volume for margin
        uav_volume = (self.uav_volume) * (1 + VF_UAV_margin) # UAV volume in m^3


        # UAV batteries volume:
        VF_UAV_battery = 0.3   # fraction of UAV volume for battery
        battery_size = VF_UAV_battery * uav_volume # battery size in m^3

        self.v_uav_bat = uav_volume + battery_size

        if self.verbose:
            print(f"Volume of UAVs: {uav_volume:.2f} m^3")
            print(f"Volume of batteries: {battery_size:.2f} m^3")
            print(f"Total volume of UAVs and batteries: {self.v_uav_bat:.2f} m^3")


    def volume_sizing(self):

        """
        
        Parameters that must be defined:
        - VF_generator: fraction of nest volume for generator
        - VF_UAV_battery: fraction of UAV volume for battery
        - VF_UAV_margin: fraction of UAV volume for margin (between drones)



        """
        # Calculate the total volume available for one nest
        available_volume_per_nest = self.nest_length * self.nest_width * self.nest_height

        self.uav_dimensions()  
        self.generator_sizing()        
        self.misc_sizing()
        self.uavs_battery_sizing()

        v_op_gen = available_volume_per_nest - self.volume_generator - self.v_locker - self.v_operating_space_gen
        v_op_nogen = available_volume_per_nest - self.v_locker - self.v_operating_space_nogen
        



        # if self.verbose:
        #     print(f"v_op_gen: {v_op_gen:.2f} m^3")
        #     print(f"v_op_nogen: {v_op_nogen:.2f} m^3")


        v_tot_uav_bat = self.v_uav_bat * self.n_drones

        if v_op_gen > v_tot_uav_bat:
            n_containers = 1
            n_cap_nest_gen = int(v_op_gen // self.v_uav_bat)
            empty_slots = n_cap_nest_gen - self.n_drones

        else:
            n_cap_nest_gen = int(v_op_gen // self.v_uav_bat)  # Number of whole drones (with battery) that fit in v_op
            n_remaining = int(self.n_drones - n_cap_nest_gen)

            # print(f"number of remaining drones: {n_remaining}")

            # n_cap_nest_nogen = int(v_op_nogen // self.v_uav_bat)  # Number of drones in overflow container
            # n_nest_nogen = n_remaining // n_cap_nest_nogen  # Number of overflow containers needed

            # empty_slots = (n_cap_nest_nogen * n_nest_nogen) - n_remaining

            # if self.verbose
            #     print(f"Number of drones that fit in generator nest: {n_cap_nest_gen}")
            #     print(f"Number of drones remaining: {n_remaining}")
            #     print(f"Number of drones that fit in non-generator nest: {n_cap_nest_nogen}")
            #     print(f"Number of overflow nests needed: {n_nest_nogen}")
            #     print(f"Empty slots in last overflow nest: {empty_slots}")

            # n_containers = 1 + n_nest_nogen
            n_cap_nest_nogen = int(v_op_nogen // self.v_uav_bat)  # Number of drones in overflow container
            n_nest_nogen = int(np.ceil(n_remaining / n_cap_nest_nogen))  # Number of overflow containers needed

            # Number of drones in the last overflow nest
            drones_in_last_nest = n_remaining % n_cap_nest_nogen
            if drones_in_last_nest == 0:
                empty_slots = 0
            else:
                empty_slots = n_cap_nest_nogen - drones_in_last_nest

            if self.verbose:
                print(f"Number of drones that fit in generator nest: {n_cap_nest_gen}")
                print(f"Number of drones remaining: {n_remaining}")
                print(f"Number of drones that fit in non-generator nest: {n_cap_nest_nogen}")
                print(f"Number of overflow nests needed: {n_nest_nogen}")
                print(f"Empty slots in last overflow nest: {empty_slots}")

            n_containers = 1 + n_nest_nogen


        self.n_nests = n_containers
        self.n_extra = empty_slots

        if self.verbose:
            print(f"Number of nests needed: {self.n_nests}")
            print(f"Number of extra slots in the last nest: {self.n_extra}")
            print(f"Volume available per nest: {available_volume_per_nest:.2f} m^3")
            print(f"Volume of generator: {self.volume_generator:.2f} m^3")
            print(f"Volume of electronics and equipment (locker): {self.v_locker:.2f} m^3")
            print(f"Volume of operating space with generator: {self.v_operating_space_gen:.2f} m^3")
            print(f"Volume of operating space without generator: {self.v_operating_space_nogen:.2f} m^3")
            print(f"Volume of UAVs and batteries: {v_tot_uav_bat:.2f} m^3")


    def mass_sizing(self):

        pass


    def energy_sizing(self):
        pass

    def deployment_time():
        pass


    # ~~~ Output functions ~~~ 

    def get_all(self) -> dict[str, float]:

        self.volume_sizing()

        self.outputs["Number_of_nests"] = ...
        self.outputs["Number_of_UAVs"]


        self.outputs["Nest_volume"] = ...
        self.outputs["Nest_mass"] = ...

        self.outputs["Volume_fueltank"] = ...

        return self.outputs
    
if __name__ == '__main__':
    # Example usage
    inputs = {
        "b_wing": 3.0, 
        "S_wing": 1.8,
        "FW_height": 0.3,
        "FW_width": 2.25,

        "uav_length": 2.5,
        "uav_width": 2.5,
        "uav_height": 0.5,
        "M_to": 1.0,
        "Number_of_UAVs": 20,
        "generator_efficiency": 0.3,
        "diesel_energy_density": 9.94,
        "nest_energy": 1000,  # in Wh
        "nest_length": 5.9,
        "nest_width": 2.35,
        "nest_height": 2.39,
        "nest_mass": 100.0,
        "aerogel_width": 1.5,
        "aerogel_diameter": 0.2

    }
    nest = Nest(inputs, verbose=True)
    outputs = nest.get_all()
    