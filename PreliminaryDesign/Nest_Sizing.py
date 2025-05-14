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