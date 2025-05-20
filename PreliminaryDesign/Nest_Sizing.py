"""File containing nest sizing functions."""
"""Inputs will be UAV dimensions, space needed for electronics
Space needed for generator, batteries, and other components and margins between drones."""

import numpy as np
from scipy.optimize import minimize
import matplotlib.pyplot as plt



class AeroShield_Nest:
    """Class for nest sizing."""
    def __init__(self, UAVs_stored: int, UAV_amount_x: int, UAV_amount_y: int, UAV_amount_x_shelve:int, double_sided: bool, UAV_aligned:bool):
        """
        ^ Y
        |          Storage
        |
        ---------------------------> X
        UAVs_Stored: total drones stored in the nest
        UAV_amount_x: number of drones in x direction
        UAV_amount_y: number of drones in y direction
        UAV_amount_x_shelve: number of drones per shelve in x direction
        double_sided: True if drawer on both sides of the nest, False if drawer on one side
        UAV_aligned:True if UAVs span aligned with x-axis, False if UAVs span aligned with y-axis
        X-axis is the direction of the nest length, y nest width 
        """

        #Total amount of drones that can be stored in the nest
        self.UAVs_stored = UAVs_stored
        #Number of drones that can be stored in a row
        self.UAV_amount_x = UAV_amount_x
        self.UAV_amount_y = UAV_amount_y
        #Whether drawer on both sides of the nest
        self.double_sided = double_sided
        #Alignment of UAVs
        self.UAV_aligned = UAV_aligned
        #Number of shelves
        self.shelves_per_row = int(np.ceil((UAV_amount_x/ UAV_amount_x_shelve))) # Add one to get number of divider walls, including the end walls
        #Drones per shelve
        self.UAVs_shelved = UAV_amount_x_shelve * UAV_amount_y
        #Total number of stacked rows
        if double_sided:
            self.rows = int(np.ceil(UAVs_stored / (UAV_amount_x * UAV_amount_y * 2)))
        else:
            self.rows = int(np.ceil(UAVs_stored / (UAV_amount_x * UAV_amount_y)))
        
    def calculate_storage_size_UAV(self, UAV_span: float, UAV_height: float, UAV_fuselage_length: float, UAV_margin: float, shelve_margin: float) -> tuple:
        """Calculate the size of the UAV based on the UAV dimensions.
        inputs:
        UAV_fuselage_length --> [m]
        UAV_span --> [m]
        UAV_height --> [m]
        UAV_margin --> [m], drone margin along all sides  
        Shelve_margin --> [m], based on the amount of space needed for the shelve divider walls and motor system
        margins could be further investigated, for example different margins in different directions
        
        outputs:
        nest_length --> [m], length of the storage
        nest_width --> [m], width of the storage
        nest_height --> [m], height of the storage
        nest_volume --> [m^3], volume of the storage
        """

        #If UAVs are aligned with x-axis
        if self.UAV_aligned:
            #Amount of drones in a row * length + margin combined with tracks for each shelve ensuring seperate retractability
            nest_length = (UAV_span + UAV_margin) * self.UAV_amount_x +  self.shelves_per_row * 2 * shelve_margin #X-axis [m]
            #If double sided, add margin for the other side of the drawerdouble_sided:
            """Do we want some margin in between the drawer? not included rn"""
            if self.double_sided:
                nest_width = (UAV_fuselage_length + UAV_margin) * self.UAV_amount_y * 2  #y-axis [m]
            else:
                nest_width = (UAV_fuselage_length + UAV_margin) * self.UAV_amount_y #y-axis [m]
        else:
            #If UAVs are aligned with y-axis
            nest_length = (UAV_fuselage_length + UAV_margin) * self.UAV_amount_x +  self.shelves_per_row * 2 * shelve_margin #X-axis [m]
            """Do we want some margin in between the drawer? not included rn"""
            if self.double_sided:
                nest_width = (UAV_span + UAV_margin) * self.UAV_amount_y * 2 # y-axis [m]
            else:
                nest_width = (UAV_span + UAV_margin) * self.UAV_amount_y # y-axis [m]

        nest_height = (UAV_height + UAV_margin) * self.rows #z-axis [m]

        nest_volume = nest_length * nest_width * nest_height #[m^3]
        return (nest_volume, nest_length, nest_width, nest_height)
    



class OldNest:

    """Class for nest sizing."""

    """
    - Drones, including margin + Batteries
    - Generator + Fuel tank
    - Electronics (e.g., communication, sensors, cooling systems)
    - Operating space (A_human * Length + something
    - Equipment (e.g., tools, spare parts, fire-extinguishing)
     
    """


    def __init__(self, inputs: dict[str, float | int], verbose: bool = False):
        



        self.verbose = verbose
        self.inputs = inputs

        self.uav_length = inputs["uav_length"]
        self.uav_width = inputs["uav_width"]
        self.uav_height = inputs["uav_height"]
        self.uav_mass = inputs["uav_mass"]

        self.n_nests = inputs["n_nests"]
        self.n_drones = inputs["n_drones"]

        # Generator parameters
        self.generator_efficiency = inputs["generator_efficiency"]
        self.diesel_energy_density = inputs["diesel_energy_density"]

        self.nest_energy = inputs["nest_energy"]

        # nest contraints
        self.nest_length = inputs["nest_length"]
        self.nest_width = inputs["nest_width"]
        self.nest_height = inputs["nest_height"]
        self.nest_mass = inputs["nest_mass"]



    def energy_sizing(self):
        
        """
        This function calculates the required volume of the fuel tank based on the nest energy requirements.
        
        """

        total_energy = self.nest_energy   # required energy in Wh

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

        if self.verbose:
            print(f"Required fuel tank volume: {fuel_tank_volume_l:.2f} liters")


    def power_sizing(self): 
        pass
        



    def volume_sizing(self):

        """
        
        Parameters that must be defined:
        - VF_generator: fraction of nest volume for generator
        - VF_UAV_battery: fraction of UAV volume for battery
        - VF_UAV_margin: fraction of UAV volume for margin (between drones)



        """
        # Calculate the total volume available for one nest
        available_volume_per_nest = self.nest_length * self.nest_width * self.nest_height


        # Generator volume:
        VF_generator = 0.1   # faction of nest volume for generator    
        volume_generator = VF_generator * available_volume_per_nest

        # UAVs volume:
        VF_UAV_margin = 0.1   # fraction of UAV volume for margin
        uav_volume = (self.uav_height * self.uav_width * self.uav_length) * (1 + VF_UAV_margin) # UAV volume in m^3
        volume_uav = self.n_drones * uav_volume  # total UAV volume in m^3

        # UAV batteries volume:
        VF_UAV_battery = 0.3   # fraction of UAV volume for battery
        battery_size = VF_UAV_battery * uav_volume # battery size in m^3
        UAV_battery_volume = self.n_drones * battery_size # total battery volume in m^3

        required_volume_uavs = volume_uav + UAV_battery_volume






    def mass_sizing(self):

        pass


    def deployment_time():
        pass



    def size_nest(self):
        
        self.energy_sizing()

        self.inputs["uavs_per_nest"] =   # amount of uavs in a nest
        self.inputs["n_nests"] =    # number of nests for mission
        self.inputs["nest_volume"] =
        self.inputs["v_nest"] =   # nest volume
        self.inputs["v_gen"] =   # generator volume
        self.inputs["nest_mass"] = 
        self.inputs["nest_energy"] = 
        self.inputs["nest_fuel_tank"] = 
        self.inputs["t_land_and_recharge"] = 

    
    def plot_nest_sizing(self):
        
        """
        Plots something like number of nests vs time to complete mission, with different perimeter lines
        """
        
        pass







    class Nest:

    """Class for nest sizing."""

    """
    - Drones, including margin + Batteries
    - Generator + Fuel tank
    - Electronics (e.g., communication, sensors, cooling systems)
    - Operating space (A_human * Length + something
    - Equipment (e.g., tools, spare parts, fire-extinguishing)
     
    """


    def __init__(self, inputs: dict[str, float | int], verbose: bool = False):
        



        self.verbose = verbose
        self.inputs = inputs

        self.uav_length = inputs["uav_length"]
        self.uav_width = inputs["uav_width"]
        self.uav_height = inputs["uav_height"]
        self.uav_mass = inputs["uav_mass"]

        self.n_nests = inputs["n_nests"]
        self.n_drones = inputs["n_drones"]

        # Generator parameters
        self.generator_efficiency = inputs["generator_efficiency"]
        self.diesel_energy_density = inputs["diesel_energy_density"]

        self.nest_energy = inputs["nest_energy"]

        # nest contraints
        self.nest_length = inputs["nest_length"]
        self.nest_width = inputs["nest_width"]
        self.nest_height = inputs["nest_height"]
        self.nest_mass = inputs["nest_mass"]

        self.available_volume_per_nest = self.nest_length * self.nest_width * self.nest_height


    def uavs_battery_sizing(self):


        # UAVs volume:
        VF_UAV_margin = 0.1   # fraction of UAV volume for margin
        uav_volume = (self.uav_height * self.uav_width * self.uav_length) * (1 + VF_UAV_margin) # UAV volume in m^3
        volume_uav = self.n_drones * uav_volume  # total UAV volume in m^3


        # UAV batteries volume:
        VF_UAV_battery = 0.3   # fraction of UAV volume for battery
        battery_size = VF_UAV_battery * uav_volume # battery size in m^3
        UAV_battery_volume = self.n_drones * battery_size # total battery volume in m^3




    def generator_sizing(self):
        
        total_energy = self.nest_energy   # required energy in Wh

        # Generator volume:
        VF_generator = 0.1   # faction of nest volume for generator    
        volume_generator = VF_generator * self.available_volume_per_nest

        l_leftover = self.nest_length - 0.9


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

        if self.verbose:
            print(f"Required fuel tank volume: {fuel_tank_volume_l:.2f} liters")




    def volume_sizing(self):

        """
        
        Parameters that must be defined:
        - VF_generator: fraction of nest volume for generator
        - VF_UAV_battery: fraction of UAV volume for battery
        - VF_UAV_margin: fraction of UAV volume for margin (between drones)



        """
        # Calculate the total volume available for one nest
        available_volume_per_nest = self.nest_length * self.nest_width * self.nest_height


        required_volume_uavs = volume_uav + UAV_battery_volume



        return l_gen, v_gen


    def mass_sizing(self):

        pass


    def energy_sizing(self):


    def deployment_time():
        pass



    def size_nest(self):
        
        self.energy_sizing()

        self.inputs["uavs_per_nest"] =   # amount of uavs in a nest
        self.inputs["n_nests"] =    # number of nests for mission
        self.inputs["nest_volume"] =
        #self.inputs["v_nest"] =   # nest volume
        self.inputs["v_gen"] =   # generator volume
        self.inputs["nest_mass"] = 
        self.inputs["nest_energy"] = 
        self.inputs["nest_fuel_tank"] = 
        self.inputs["t_land_and_recharge"] = 

    
    def plot_nest_sizing(self):
        
        """
        Plots something like number of nests vs time to complete mission, with different perimeter lines
        """
        
        pass