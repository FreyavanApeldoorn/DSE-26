import numpy as np
import math
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from deployment import Deployment

class Performance:

    def __init__(self, inputs: dict[str, float], hardware) -> None:
        self.inputs = inputs
        self.outputs = self.inputs.copy()
        self.hardware = hardware
        self.deployment = Deployment(self.inputs, 'perimeter', self.mission_perimeter)

        self.n_workers = ...
        self.n_nests = ...
        self.range = ...

        self.aerogel_absorption_factor = 50 #g/g https://www.sciencedirect.com/science/article/pii/S2213343722002299, https://www.sciencedirect.com/science/article/pii/S1385894715002326#:~:text=50%20°C.-,Abstract,their%20high%20oil%20absorption%20capacities.

        self.mission_perimeter = inputs["mission_perimeter"]
        self.oil_mass = inputs['oil_mass']

    # ~~~ Intermediate Functions ~~~

    def calc_UAV_runs(self):
        # For wildfire
        self.nr_runs_fire = self.deployment.perimeter_creation()

        # For oil
        aerogel_mass, _, _ =  self.deployment.aerogel_size()
        self.nr_runs_oil = math.ceil((self.oil_mass / self.aerogel_absorption_factor) / aerogel_mass)


    def deployment_rates(self, plot=True) -> float:
        """
        Calculates and updates the UAV and overall deployment rates for the mission.
        This method computes the UAV deployment rate and the overall deployment rate
        based on the mission perimeter, UAV time, and total mission time. It updates
        the corresponding instance attributes with the calculated values.
        Returns
        -------
        float
            The overall deployment rate for the mission.
        Notes
        -----
        This method assumes that `calc_total_mission_time` properly updates
        `self.time_uav` and `self.total_mission_time` before the rates are calculated.
        """

        self.calc_UAV_runs()


        self.total_mission_time_oil = ... # Func(range, n_nests, n_workers, self.nr_runs_oil)
        self.total_mission_time_fire = ... #

        #single calculation
        self.mission_deployment_rate_oil = self.oil_mass / self.total_mission_time_oil
        self.mission_deployment_rate_fire = self.mission_perimeter / self.total_mission_time_fire

        
        if plot:
            #Deployment rate based on range 

            #Deployment range based on nr_nests and nr_workers
            nests_range = range(1, 11)
            workers_range = range(0, 21)

            nest_worker_table = pd.DataFrame(index=workers_range, columns=nests_range, dtype=float)

            for workers in workers_range:
                for nests in nests_range:
                    if nests <= workers <= 2 * nests and workers % 2 == 0:
                        nest_worker_table.loc[workers, nests] = ... #add this here
                    else:
                        nest_worker_table.loc[workers, nests] = np.nan

            plt.figure(figsize=(10, 6))
            sns.heatmap(nest_worker_table, annot=True, fmt=".2f", cmap="RdYlGn", cbar_kws={'label': 'Deployment Rate'})
            plt.title("Deployment Rate by Number of Workers and Nests")
            plt.xlabel("Number of Nests")
            plt.ylabel("Number of Workers")
            plt.tight_layout()
            plt.show()      
    


    # ~~~ Output functions ~~~ 

    def get_all(self) -> dict[str, float]:

        self.deployment_rates()

        self.outputs["uav_deployment_rate"] = self.uav_deployment_rate
        self.outputs["mission_deployment_rate"] = self.mission_deployment_rate

        return self.outputs
    
if __name__ == '__main__':
    # Perform sanity checks here
    ...