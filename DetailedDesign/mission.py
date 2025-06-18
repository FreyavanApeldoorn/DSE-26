import numpy as np
import math 


from DetailedDesign.deployment import Deployment


'''
This is the file for the mission. It contains a single class.
'''

class Mission:

    def __init__(self, inputs: dict[str, float], verbose: bool = False) -> None:
        
        self.inputs = inputs
        self.outputs = self.inputs.copy() # Copy inputs to outputs
        self.verbose = verbose

        #Nest
        self.number_of_UAV = inputs["number_of_UAVs"] # mission input
        self.number_of_containers = inputs["number_of_containers"] #expected from nest
        self.cap_gen = inputs["capacity_gen"]
        self.cap_nogen = inputs["capacity_nogen"]

        self.number_of_slaves = inputs["number_of_workers"] # 
        self.number_of_workers = inputs["number_of_workers"] # Number of workers available for the mission

        #Input Times
        # self.time_wing_attachment = inputs["time_wing_attachment"] #
        # self.time_aerogel_loading = inputs["time_aerogel_loading"] #
        # self.time_startup_UAV = inputs["time_startup_UAV"] # 
        # self.time_between_containers = inputs["time_between_containers"] # 
        # self.time_UAV_wrapup_check = inputs["time_UAV_wrapup_check"] # 
        # self.time_UAV_turnaround_check = inputs["time_UAV_turnaround_check"] # 
        # self.time_put_back_UAV = inputs["time_put_back_UAV"] # 
        # self.time_startup_nest = inputs["time_startup_nest"] # 
        # self.time_final_wrapup = inputs["time_final_wrapup"] # 
        # self.time_between_UAV = inputs["time_between_UAV"] # 
        # self.time_battery_swapping = inputs["time_battery_swapping"] # Time between swapping batteries [s]: From UAV design

        # Launch times
        #self.time_unload_container = 5*60
        self.time_open_container = 30
        self.time_startup_nest = 3*60
        self.time_unload_uav = 60
        self.time_assemble_uav = 30
        self.time_position_uav = 30
        self.time_startup_uav = 30

        self.time_walk_between_containers = 60 # Time to walk between containers [s]: From UAV design

        # Turnaround times
        self.time_turnaround_check = 15
        self.time_reload_aerogel = 30
        self.time_replace_battery = 30

        # Wrapup times
        #self.time_


        self.margin = inputs["margin"]


        #UAV Inputs
        self.h_cruise = inputs["h_cruise"] # Mission altitude [m]: mission definition
        self.V_climb_v = inputs["ROC_VTOL"] # Climb speed [m/s]: mission definition
        self.V_descent = inputs["ROD_VTOL"] # Descent speed [m/s]: mission definition
        self.V_cruise = inputs["V_cruise"] # Cruise speed [m/s]: mission definition
        self.wind_speed = inputs["wind_speed"] # Wind speed [m/s]: mission definition

        self.time_transition = inputs["time_transition"]
        self.time_deploy = inputs["time_deploy"] # Time for deploying the UAV [s]: From UAV design
        self.time_scan = inputs["time_scan"] # Time for scanning [s]: From UAV design 


        #Mission Specifics
        self.mission_type = inputs['mission_type']
        self.mission_perimeter = inputs["mission_perimeter"] #We define, mission perimeter [m] 
        self.oil_mass = inputs["oil_mass"]
        self.aerogel_absorption_factor = 50 #g/g https://www.sciencedirect.com/science/article/pii/S2213343722002299, https://www.sciencedirect.com/science/article/pii/S1385894715002326#:~:text=50%20°C.-,Abstract,their%20high%20oil%20absorption%20capacities.
        self.R_max = inputs["R_max"] # Maximum range [m]: mission definition
        self.R_min = inputs["R_min"]


        self.deployment = Deployment(self.outputs, 'perimeter', self.mission_perimeter)

        #Aerogel Specifics
        #self.num_aerogels = inputs["nr_aerogels"]
        
    

    # ~~~ Intermediate Functions ~~~

    def calc_time_turn_around(self) -> float:
        """
        Calculates the turnaround time for a UAV.
        The turnaround time is computed as the sum of the UAV turnaround check time,
        battery swapping time, and aerogel loading time. The result is stored in
        `self.time_turnaround`.
        Returns
        -------
        float
            The total turnaround time in minutes.
        """

        time_turnaround_min = self.time_turnaround_check + self.time_reload_aerogel + self.time_replace_battery # Time for 1 UAV to turnaround nothing special
        
        pairs = self.number_of_workers // 2  # how many pairs of workers we have

        self.time_min_launch = time_turnaround_min / pairs  # time between launches, assuming pairs of workers handle one UAV each


    def calc_time_preparation(self) -> float:
        # first, ensure our turnaround time is up to date
        self.calc_time_turn_around()

        if self.number_of_workers < 2:
            raise ValueError("Number of workers must be at least 2 for preparation time calculation.")

        # constants
        time_nest_setup = (
            self.time_open_container
            + self.time_startup_nest
        )

        time_uav_setup = (
            self.time_unload_uav
            + self.time_assemble_uav
            + self.time_position_uav
            + self.time_startup_uav
        )

        if self.verbose:
            print(f"Number of Workers: {self.number_of_workers}")

        pairs = self.number_of_workers // 2
        
        uavs_launched = 0
        total_time = 0.0


        #print(f"\n\n\nDEBUG\n\n\n {type(self.cap_gen)} : {type(self.cap_nogen)} : {type(self.number_of_containers)}\n\n\n")
        # list of nest capacities: first nest is the generator nest with 6 UAVs
        nest_capacities = [self.cap_gen] + [self.cap_nogen] * (self.number_of_containers - 1)
        # (you’d set number_of_containers_minus_one appropriately elsewhere)


        if self.verbose:
            print(f"Nest Capacities: {nest_capacities}")
            print(f"Number of Pairs: {pairs}")
            print(f"Number of UAVs: {self.number_of_UAV}")
            print(f"Time Nest Setup: {time_nest_setup} seconds")
            print(f"Time UAV Setup: {time_uav_setup} seconds")

        for cap in nest_capacities:
            if uavs_launched >= self.number_of_UAV:
                break

            # time to set up this nest
            #total_time += self.time_open_container

            # how many UAVs we will actually take from this nest
            remaining = self.number_of_UAV - uavs_launched
            uavs_this_nest = min(cap, remaining)

            # full batches we can launch in parallel
            full_batches = uavs_this_nest // pairs
            # and the leftover (partial) batch size
            partial = uavs_this_nest % pairs

            # for each full batch:
            for _ in range(full_batches):
                # setup time (all pairs work in parallel on one UAV each, so
                # total time is just one setup time per batch)
                total_time += time_uav_setup
                # need spacing delays between UAVs in the batch
                total_time += (pairs - 1) * self.time_min_launch
                uavs_launched += pairs

            # if there’s a leftover partial batch, we only add one more setup time
            if partial > 0:
                total_time += time_uav_setup
                uavs_launched += partial

            # if we still need more, walk to next container
            if uavs_launched < self.number_of_UAV:
                total_time += self.time_walk_between_containers

        self.time_launch = total_time
        self.time_preparation = total_time + time_nest_setup

        if self.verbose:
            print(f"Preparation Time: {self.time_preparation/60} minutes")
            print(f"UAV Launch Time: {(self.time_launch)/60} minutes")



    def uav_mission_time(self) -> float: 
        
        self.time_ascent = self.h_cruise / self.V_climb_v
        self.time_descent = self.h_cruise / self.V_descent
        self.time_cruise = self.R_max / (self.V_cruise - self.wind_speed) # Slowest-case scenario, wind against the UAV
        self.time_cruise_min = self.R_min / (self.V_cruise + self.wind_speed) # Fastest-case scenario, wind with the UAV

        if self.verbose:
            print(f"Time Ascent: {self.time_ascent} seconds")
            print(f"Time Descent: {self.time_descent} seconds")
            print(f"Time Cruise: {self.time_cruise} seconds")
            print(f"Time Cruise Min: {self.time_cruise_min} seconds")

        self.calc_time_turn_around()   # calculate time for turnaround

        mission_times = np.array([self.time_ascent, self.time_transition, self.time_cruise, self.time_transition, 
                         self.time_scan, self.time_descent, self.time_deploy, self.time_ascent, 
                         self.time_transition, self.time_cruise, self.time_transition, self.time_descent, self.time_min_launch])
        self.time_uav = np.sum(mission_times)
        self.time_uav_min = self.time_uav - self.time_cruise + self.time_cruise_min

        cruise_times = np.array([self.time_cruise, self.time_cruise])
        self.cruise_time = np.sum(np.array(cruise_times))

        ascent_times = np.array([self.time_ascent, self.time_ascent])
        self.time_ascent = np.sum(np.array(ascent_times))

        descent_times = np.array([self.time_descent, self.time_descent])
        self.time_descent = np.sum(np.array(descent_times))

        if self.verbose:
            print(f"UAV Mission Time: {self.time_uav} seconds")



    def calc_UAV_runs(self):

        print("RAN calc_UAV_runs()")

        if self.mission_type == "wildfire":

            # For wildfire
            self.nr_runs_fire = Deployment(self.inputs, 'perimeter', self.mission_perimeter).perimeter_creation()
            self.num_trips = self.nr_runs_fire

        elif self.mission_type == "oil_spill":
            # For oil
            aerogel_mass, _, _ =  self.deployment.aerogel_size()
            self.nr_runs_oil = math.ceil((self.oil_mass / self.aerogel_absorption_factor) / aerogel_mass)
            self.num_trips = self.nr_runs_oil

        else:
            raise ValueError(f"Unsupported mission type: {self.mission_type}")
        
        if self.verbose:
            print(f"Number of trips for mission: {self.num_trips}")

        print(f"Number of trips {self.num_trips}")


    def calc_time_operation(self) -> float:

        print("RAN calc_time_operation()")

        self.uav_mission_time()
        self.calc_UAV_runs()

        #self.num_trips = self.num_aerogels
        num_cycles = self.num_trips / self.number_of_UAV
        self.num_cycles = num_cycles
        self.time_operation = num_cycles * self.time_uav

        if self.verbose:
            print(f"Number of cycles: {num_cycles}")
            print(f"Time Operation: {self.time_operation/60} minutes")



    def calc_time_wrapup(self) -> float: #Verified
        """
        Calculates the total wrap-up time for UAV operations based on the number of UAVs, containers, and available workers.
        The method computes the time required to wrap up UAV operations, considering the time for wing attachment, putting back UAVs, wrap-up checks, and time between UAVs and containers. The calculation adapts based on the number of available workers (slaves) and UAVs.
        Returns
        -------
        float
            The total wrap-up time in the same time units as the input parameters.
        Raises
        ------
        ValueError
            If the number of slaves is less than 1.
        Notes
        -----
        The result is also stored in the instance variable `self.time_wrapup`.
        """

        #Bottom point graph
        UAV_wrapup_time = self.time_wing_attachment + self.time_put_back_UAV + self.time_UAV_wrapup_check + self.time_between_UAV # Time for 1 UAV to wrapup
        #Top point graph
        time_wrapup_1worker = (UAV_wrapup_time * self.number_of_UAV + self.time_between_containers * self.number_of_containers)
        time_slope = (UAV_wrapup_time - time_wrapup_1worker)/(self.number_of_UAV - 1)
        if self.number_of_slaves >= self.number_of_UAV:
            time_wrapup = UAV_wrapup_time + self.time_final_wrapup
        elif self.number_of_slaves < 1:
            raise ValueError("Number of slaves is less than 1, and that's a big problem!")
        else:
            time_wrapup = time_wrapup_1worker + time_slope * (self.number_of_slaves - 1) + self.time_final_wrapup
        
        self.time_wrapup = time_wrapup 
        

    def calc_total_mission_time(self) -> float:
  

        self.calc_time_preparation()
        self.calc_time_operation()
        #self.calc_time_wrapup()


        total_mission_time = self.time_preparation + self.time_operation #+ self.time_wrapup
        self.total_mission_time = total_mission_time

        if self.verbose:
            print('total_mission_time', total_mission_time)



    def performance_calcs(self, r_max: float, nr_UAvs: int, nr_containers: int, nr_workers: int) -> None:
        
        update = False

        if update:
            self.R_max = r_max 
            self.number_of_UAV = nr_UAvs
            self.number_of_containers = nr_containers
            self.number_of_workers = nr_workers


        self.calc_total_mission_time()  # recalculate total mission time with new parameters
        

        #reset all the values in self
        return self.total_mission_time, self.time_operation


    # ~~~ Output functions ~~~ 
 
    def get_all(self) -> dict[str, float]:

        self.calc_total_mission_time()

        self.outputs["trips_for_mission"] = self.num_trips
        

        self.outputs["time_uav_max"] = self.time_uav
        self.outputs["time_uav_min"] = self.time_uav_min
        self.outputs["time_cruise_max"] = self.cruise_time
        self.outputs["time_cruise_min"] = self.time_cruise_min
        self.outputs['time_ascent'] = self.time_ascent
        self.outputs['time_descent'] = self.time_descent
        self.outputs["time_turnaround"] = self.time_min_launch




        self.outputs["time_preparation"] = self.time_preparation
        self.outputs["time_operation"] = self.time_operation
        self.outputs["time_wrapup"] = self.time_preparation #self.time_wrapup
        self.outputs["total_mission_time"] = self.total_mission_time

        return self.outputs
    


# ==========================================================

if __name__ == '__main__':
    # Perform sanity checks here

    from funny_inputs import deployment_funny_inputs

    test_inputs_mission = {
        "number_of_UAVs": 20,
        "number_of_containers": 3,
        "capacity_gen": 6,
        "capacity_nogen": 10,
        "number_of_workers": 4,
        "margin": 60,
        "h_cruise": 120.0,
        "ROC_VTOL": 3.0,
        "ROD_VTOL": 2.0,
        "V_cruise": 100/3.6,
        "wind_speed": 30.0/3.6,
        "time_transition": 30.0,
        "time_deploy": 5*60,
        "time_scan": 60.0,
        "mission_type": "wildfire",
        "mission_perimeter": 1000.0,
        "oil_mass": 7000.0,
        "R_max": 20000.0,
        "R_min": 1000.0,
        #"nr_aerogels": 12,
        # The following are needed for wrapup (used in calc_time_wrapup)
        "time_wing_attachment": 30.0,
        "time_put_back_UAV": 30.0,
        "time_UAV_wrapup_check": 15.0,
        "time_between_UAV": 10.0,
        "time_between_containers": 60.0,
        "time_final_wrapup": 60.0
    }
    deployment_funny_inputs.update(test_inputs_mission)  # Update with deployment inputs

    mission = Mission(test_inputs_mission)

    mission.mission_type = 'wildfire'
    mission.mission_perimeter = 201
    mission.calc_total_mission_time()
    print(mission.num_trips)
    print(round(mission.total_mission_time) / 60 / 60)

    mission.mission_type = 'oil_spill'
    mission.calc_total_mission_time()
    print(round(mission.total_mission_time)) 


    