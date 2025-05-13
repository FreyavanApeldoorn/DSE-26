"""File containing nest sizing functions."""
"""Inputs will be UAV dimensions, space needed for electronics
Space needed for generator, batteries, and other components and margins between drones."""

import numpy as np
from scipy.optimize import minimize
import matplotlib.pyplot as plt



class Drawers_UAV_Size:
    """Class for nest sizing."""
    def __init__(self, drones_stored: int, drones_per_row: int, double_sided: bool, UAV_aligned:bool):
        """UAV_aligned:True if UAVs span aligned with x-axis, False if UAVs span aligned with y-axis
        X-axis is the direction of the nest length, y nest width 
        ^ Y
        |          Drawer
        |
        ---------------------------> X
        Height, Width, Length are the dimensions of the UAV"""

        #Total amount of drones that can be stored in the nest
        self.drones_stored = drones_stored
        #Number of drones that can be stored in a row
        self.drones_per_row = drones_per_row
        #Whether drawer on both sides of the nest
        self.double_sided = double_sided
        #ALignment of UAVs
        self.UAV_aligned = UAV_aligned
        #Total number of stacked rows
        if double_sided:
            self.rows = np.ceil(drones_stored / (drones_per_row*2))
        else:
            self.rows = np.ceil(drones_stored / drones_per_row)
        