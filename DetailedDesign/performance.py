import numpy as np
import math
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from mission import Mission

from deployment import Deployment

class Performance:

    def __init__(self, inputs: dict[str, float], hardware) -> None:
        self.inputs = inputs
        self.outputs = self.inputs.copy()
        self.hardware = hardware
        self.deployment = Deployment(self.inputs, 'perimeter', self.mission_perimeter)
        self.mission = Mission(inputs)

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


        self.total_mission_time_oil = ... # Func(range, n_UAVs, n_workers, self.nr_runs_oil)
        self.total_mission_time_fire = ... #

        #single calculation

        # Deployment rate is from the time the first UAV takes off to the time the last one lands
        self.mission_deployment_rate_oil = self.oil_mass / self.total_mission_time_oil
        self.mission_deployment_rate_fire = self.mission_perimeter / self.total_mission_time_fire

        
        if plot:
            #Deployment rate based on range 
            range_range = np.arange(1, 21)
            oil_mass_range = np.arange(1, 1000)
            perimeter_range = np.arange(1, 1000)

            R_oil, Y_oil = np.meshgrid(range_range, oil_mass_range)
            R_fire, Y_fire = np.meshgrid(range_range, perimeter_range)

            # Example dep_time formula (can be adjusted)
            dep_time_oil = ...
            dep_time_fire = ...

            dep_rate_oil = Y_oil / dep_time_oil
            dep_rate_fire = Y_fire / dep_time_fire


            plt.figure(figsize=(8, 6))
            contour = plt.contourf(R_oil, Y_oil, dep_rate_oil, levels=50, cmap='plasma')
            plt.colorbar(contour, label='Deployment Rate [kg/s]')
            plt.xlabel('Range [km]')
            plt.ylabel('Oil Mass [kg]')
            plt.tight_layout()
            plt.savefig('DetailedDesign\plots\oil_range_mass_diagram')
            plt.show()

            plt.figure(figsize=(8, 6))
            contour = plt.contourf(R_fire, Y_fire, dep_rate_fire, levels=50, cmap='plasma')
            plt.colorbar(contour, label='Deployment Rate [m/s]')
            plt.xlabel('Range [km]')
            plt.ylabel('Oil Mass [kg]')
            plt.tight_layout()
            plt.savefig('DetailedDesign\plots\oil_range_mass_diagram')
            plt.show()

            #Deployment range based on nr_nests and nr_workers
            nests_range = range(1, 11)
            workers_range = range(0, 21)

            nest_worker_table = pd.DataFrame(index=workers_range, columns=nests_range, dtype=float)

            for strat in ['oil', 'wildfire']:
                for workers in workers_range:
                    for nests in nests_range:

                        if workers % 2 == 0:
                            dep_time = ... #Add
                            if strat == 'oil':
                                nest_worker_table.loc[workers, nests] = self.oil_mass / dep_time
                            else:
                                if nests <= workers <= 2 * nests:
                                    nest_worker_table.loc[workers, nests] = self.mission_perimeter / dep_time
                        else:
                            nest_worker_table.loc[workers, nests] = np.nan

                plt.figure(figsize=(10, 6))
                sns.heatmap(nest_worker_table, annot=True, fmt=".2f", cmap="RdYlGn", cbar_kws={'label': 'Deployment Rate'})
                plt.title(f"Deployment Rate by Number of Workers and Nests for {strat}")
                plt.xlabel("Number of Nests")
                plt.ylabel("Number of Workers")
                plt.tight_layout()
                plt.savefig(f"DetailedDesign\plots\{strat}_worker_nest_heatmap.png")
                plt.show()   


        # elif self.mission_type == "oil_spill":
        #     self.uav_deployment_rate = self.mission_mass

        else:
            raise ValueError(f"Unsupported mission type: {self.mission_type}")

    def response_time(self) -> float:
        pass

    def turnaround_time(self) -> float:
        pass

    def energy_consumption(self) -> float:
        pass

    def total_mass(self) -> float:
        pass

    


    # ~~~ Output functions ~~~ 

    def get_all(self) -> dict[str, float]:

        self.deployment_rates()

        self.outputs["uav_deployment_rate"] = self.uav_deployment_rate
        self.outputs["mission_deployment_rate"] = self.mission_deployment_rate

        return self.outputs
    
if __name__ == '__main__':
    # Perform sanity checks here
    ...