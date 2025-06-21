import numpy as np
import math
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from mission import Mission

from deployment import Deployment

class Performance:

    def __init__(self, inputs: dict[str, float]) -> None:
        self.inputs = inputs
        self.outputs = self.inputs.copy()
        # self.hardware = hardware

        self.mission_perimeter = inputs["mission_perimeter"]
        self.oil_mass = inputs['oil_mass']

        self.deployment = Deployment(self.inputs, 'perimeter', self.mission_perimeter)
        self.mission = Mission(inputs)

        # Standard case
        self.n_workers = 6 #2 per nest
        self.n_nests = 3 #fits 20 UAVs
        self.n_uavs = 20 #from requirement
        self.range = inputs['R_max']

        self.generator_nest_cap = 6
        self.reg_nest_cap = 10

        self.aerogel_absorption_factor = 50 #g/g https://www.sciencedirect.com/science/article/pii/S2213343722002299, https://www.sciencedirect.com/science/article/pii/S1385894715002326#:~:text=50%20°C.-,Abstract,their%20high%20oil%20absorption%20capacities.

    # ~~~ Intermediate Functions ~~~

    def calc_UAV_runs(self):
        # For wildfire
        self.nr_runs_fire = self.deployment.perimeter_creation()

        # For oil
        aerogel_mass, _, _ =  self.deployment.aerogel_size()
        self.nr_runs_oil = math.ceil((self.oil_mass / self.aerogel_absorption_factor) / aerogel_mass)

    def test(self):
        self.mission.get_all()
        print(self.mission.total_mission_time / 60 / 60)


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

        #single calculation

        # Deployment rate is from the time the first UAV takes off to the time the last one lands
        # self.mission_deployment_rate_oil = self.oil_mass / self.total_mission_time_oil
        # self.mission_deployment_rate_fire = self.mission_perimeter / self.total_mission_time_fire

        
        if plot:

            range_range = range(10000, 25000, 1000)
            oil_range = range(1000, 9001, 1000)
            perimeter_range = range(100, 601, 100)
            
            time_range = []
            grid = []
            for r in range_range:
                for m in oil_range:
                    mis = Mission(self.inputs)
                    mis.oil_mass = m
                    mis.mission_type = 'oil_spill'
                    mis.R_max = r
                    mis.calc_total_mission_time()
                    res = mis.total_mission_time / (60)
                    time_range.append(res)
                    grid.append((r, m))
                    if r == 20000 and m == 7000:
                        print(res)


            range_vals = sorted(set([pt[0] for pt in grid]))
            oil_vals = sorted(set([pt[1] for pt in grid]))

            Z = np.array(time_range).reshape(len(range_vals), len(oil_vals)).T
            X, Y = np.meshgrid(range_vals, oil_vals)  # X: range, Y: AR

            plt.figure(figsize=(8, 6))
            cp = plt.contourf(X, Y, Z, cmap='plasma')
            plt.colorbar(cp, label='total response time [min]')
            plt.xlabel('Range [m]')
            plt.ylabel('oil mass [kg]')
            plt.savefig('DetailedDesign\plots\oil_range.png')
            plt.show()

            time_range = []
            grid = []
            for r in range_range:
                for p in perimeter_range:
                    mis = Mission(self.inputs)
                    mis.mission_perimeter = p
                    mis.mission_type = 'wildfire'
                    mis.R_max = r
                    mis.calc_total_mission_time()
                    res = mis.total_mission_time / (60)
                    print(res)
                    time_range.append(res)
                    if r == 20000 and p == 500:
                        print(res)
                    grid.append((r, p))


            range_vals = sorted(set([pt[0] for pt in grid]))
            perimeter_vals = sorted(set([pt[1] for pt in grid]))

            Z = np.array(time_range).reshape(len(range_vals), len(perimeter_vals)).T
            X, Y = np.meshgrid(range_vals, perimeter_vals)  # X: range, Y: AR

            plt.figure(figsize=(8, 6))
            cp = plt.contourf(X, Y, Z, cmap='plasma')
            plt.colorbar(cp, label='total response time [min]')
            plt.xlabel('Range [m]')
            plt.ylabel('Mission perimeter [m]')
            plt.savefig('DetailedDesign\plots\perimeter_range.png')
            plt.show()
            

            
            #Deployment range based on nr_nests and nr_workers
            uavs_range = range(10, 51)
            workers_range = range(2, 13)

            uav_worker_table = pd.DataFrame(index=workers_range, columns=uavs_range, dtype=float)


            
            for strat in ['oil_spill', 'wildfire']:
                uav_worker_table = pd.DataFrame(index=workers_range, columns=uavs_range, dtype=float)
                for workers in workers_range:
                    for uavs in uavs_range:
                        nests = 1 + max(0, math.ceil((uavs - self.generator_nest_cap) / self.reg_nest_cap))
                        mis = Mission(self.inputs)
                        mis.mission_type = strat
                        mis.number_of_UAV = uavs
                        mis.number_of_workers = workers
                        mis.number_of_containers = nests
                        mis.calc_total_mission_time()

                        dep_time = mis.total_mission_time / (60*60)
                        if strat == 'oil_spill':
                            unit = '[kg/h]'
                            uav_worker_table.loc[workers, uavs] = round(self.oil_mass / dep_time)
                            if uavs == 20 and workers == 6:
                                print('oil', round(self.oil_mass / dep_time))
                        else:
                            unit = '[m/h]'
                            if uavs == 20 and workers == 6:
                                print('fire', round(self.mission_perimeter / dep_time))
                            if nests <= workers <= 2 * nests:
                                uav_worker_table.loc[workers, uavs] = round(self.mission_perimeter / dep_time)
                            else:
                                uav_worker_table.loc[workers, uavs] = np.nan

                plt.figure(figsize=(8, 6))
                sns.heatmap(uav_worker_table, annot=False, fmt=".2f", cmap="RdYlGn", cbar_kws={'label': f'Deployment Rate {unit}'}, annot_kws={"size": 6})
                ax = plt.gca()
                for spine in ax.spines.values():
                    spine.set_visible(True)
                    spine.set_edgecolor('black')
                    spine.set_linewidth(1.5)
                plt.xlabel("Number of UAVs")
                plt.ylabel("Number of Workers")
                plt.tight_layout()
                plt.savefig(f"DetailedDesign\plots\{strat}_worker_nest_heatmap.png")
                plt.show()   
                
                



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

    from funny_inputs import deployment_funny_inputs

    test_inputs_performance = {
        "number_of_UAVs": 20,
        "number_of_containers": 3,
        "capacity_gen": 5,
        "capacity_nogen": 10,
        "number_of_workers": 6,
        "margin": 60,
        "h_cruise": 100.0,
        "ROC_VTOL": 3.0,
        "ROD_VTOL": 2.0,
        "V_cruise": 20.0,
        "wind_speed": 5.0,
        "time_transition": 10.0,
        "time_deploy": 20.0,
        "time_scan": 60.0,
        "mission_type": "oil_spill",
        "mission_perimeter": 500.0,
        "oil_mass": 7000.0,
        "R_max": 20000.0,
        "R_min": 1000.0,
        #"nr_aerogels"S: 12,
        # The following are needed for wrapup (used in calc_time_wrapup)
        "time_wing_attachment": 30.0,
        "time_put_back_UAV": 30.0,
        "time_UAV_wrapup_check": 15.0,
        "time_between_UAV": 10.0,
        "time_between_containers": 60.0,
        "time_final_wrapup": 60.0,
    }

    test_inputs_performance.update(deployment_funny_inputs)

    perf = Performance(test_inputs_performance)

    perf.deployment_rates()
