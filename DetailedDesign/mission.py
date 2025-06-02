import numpy as np

'''
This is the file for the mission. It contains a single class.
'''

class Mission:

    def __init__(self, inputs: dict[str, float], verbose: bool = True) -> None:
        
        self.inputs = inputs
        self.outputs = self.inputs.copy() # Copy inputs to outputs
        self.verbose = verbose

        #Nest
        self.number_of_UAV = inputs["number_of_UAV"] # mission input
        self.number_of_containers = inputs["number_of_containers"] #expected from nest
        #self.number_of_nests = inputs["number_of_nests"] # expected from nest
        self.number_of_slaves = inputs["number_of_workers"] # 

        #Input Times
        self.time_wing_attachment = inputs["time_wing_attachment"] #
        self.time_aerogel_loading = inputs["time_aerogel_loading"] #
        self.time_startup_UAV = inputs["time_startup_UAV"] # 
        self.time_between_containers = inputs["time_between_containers"] # 
        self.time_UAV_wrapup_check = inputs["time_UAV_wrapup_check"] # 
        self.time_UAV_turnaround_check = inputs["time_UAV_turnaround_check"] # 
        self.time_put_back_UAV = inputs["time_put_back_UAV"] # 
        self.time_startup_nest = inputs["time_startup_nest"] # 
        self.time_final_wrapup = inputs["time_final_wrapup"] # 
        self.time_between_UAV = inputs["time_between_UAV"] # 
        self.time_battery_swapping = inputs["time_battery_swapping"] # Time between swapping batteries [s]: From UAV design

        self.margin = inputs["margin"]


        #UAV Inputs
        self.h_cruise = inputs["h_cruise"] # Mission altitude [m]: mission definition
        self.V_climb_v = inputs["V_climb_v"] # Climb speed [m/s]: mission definition
        self.V_descent = inputs["V_descent"] # Descent speed [m/s]: mission definition
        self.V_cruise = inputs["V_cruise"] # Cruise speed [m/s]: mission definition

        self.time_transition = inputs["time_transition"]
        self.time_deploy = inputs["time_deploy"] # Time for deploying the UAV [s]: From UAV design
        self.time_scan = inputs["time_scan"] # Time for scanning [s]: From UAV design 


        #Mission Specifics
        self.mission_type = inputs['mission_type']
        self.mission_perimeter = inputs["mission_perimeter"] #We define, mission perimeter [m] 
        self.R_max = inputs["R_max"] # Maximum range [m]: mission definition


        #Aerogel Specifics
        self.num_aerogels = inputs["num_aerogels"]
        
    

    # ~~~ Intermediate Functions ~~~

    def calc_time_preparation(self) -> float:
        """
        Calculate the total preparation time required for UAV launch.
        This method computes the time needed to prepare all UAVs and containers for launch,
        taking into account the number of UAVs, number of containers, number of available workers,
        and various time components such as wing attachment, aerogel loading, UAV startup, and nest startup.
        The calculation considers different scenarios based on the number of workers relative to the number of UAVs.
        Returns
        -------
        float
            The total preparation time in seconds.
        Raises
        ------
        ValueError
            If the number of slaves (workers) is less than 1.
        Notes
        -----
        - If the number of slaves is greater than or equal to the number of UAVs, preparation time is minimized.
        - If the number of slaves is less than the number of UAVs, a linear relation is assumed for walking time between containers.
        - The method caches the calculated launch and preparation times as instance attributes.
        """
        
        #Bottom point graph - the maximum time based on a single worker
        UAV_launch_time = self.time_wing_attachment + self.time_aerogel_loading +  self.time_startup_UAV + self.time_between_UAV # Time for 1 UAV to prepare
        self.UAV_launch_time = UAV_launch_time  # cache launch time

        #Top point graph - the minimum time 
        time_launch_1worker = (UAV_launch_time * self.number_of_UAV + self.time_between_containers * self.number_of_containers) #Assume containers relatively closer together, linear relation walking time, upper bound
        time_slope = (UAV_launch_time - time_launch_1worker)/(self.number_of_UAV - 1)
        if self.number_of_slaves >= self.number_of_UAV:
            time_preparation = UAV_launch_time + self.time_startup_nest
        elif self.number_of_slaves < 1:
            raise ValueError("Number of slaves is less than 1, and that's a big problem!")
        else: 
            time_preparation = time_launch_1worker + time_slope * (self.number_of_slaves - 1) + self.time_startup_nest #Assume containers relatively closer together, linear relation walking time, upper bound
        
        self.time_preparation = time_preparation


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

        time_turnaround_min = self.time_UAV_turnaround_check + self.time_battery_swapping + self.time_aerogel_loading # Time for 1 UAV to turnaround nothing special
        self.time_turnaround = time_turnaround_min # Assuming 


    def uav_mission_time(self) -> float: 
        """
        Calculates and stores the total UAV mission time by summing the durations of all mission phases.
        The method computes the time required for ascent, transition, cruise, scan, descent, deployment, and turnaround phases.
        It updates the corresponding instance attributes with the calculated times and stores the total mission time in `self.time_uav`.
        Returns
        -------
        float
            The total UAV mission time in seconds.
        Notes
        -----
        - Assumes that all required instance attributes (e.g., `h_cruise`, `V_climb_v`, `V_descent`, `R_max`, `V_cruise`, etc.)
        are already set.
        - The method prints the total mission time if `self.verbose` is True.
        """
        
        self.time_ascent = self.h_cruise / self.V_climb_v
        self.time_descent = self.h_cruise / self.V_descent
        self.time_cruise = self.R_max / self.V_cruise
        self.time_transition = self.time_transition
        self.time_scan = self.time_scan
        self.time_deploy = self.time_deploy

        self.calc_time_turn_around()   # calculate time for turnaround

        mission_times = np.array([self.time_ascent, self.time_transition, self.time_cruise, self.time_transition, 
                         self.time_scan, self.time_descent, self.time_deploy, self.time_ascent, 
                         self.time_transition, self.time_cruise, self.time_transition, self.time_descent, self.time_turnaround])
        self.time_uav = np.sum(mission_times)

        hover_times = np.array([self.time_ascent, self.time_transition, self.time_transition, self.time_scan, self.time_descent, 
                                self.time_deploy, self.time_ascent, self.time_transition, self.time_transition, self.time_descent])
        self.hover_time = np.sum(np.array(hover_times))

        cruise_times = np.array([self.time_cruise, self.time_cruise])
        self.cruise_time = np.sum(np.array(cruise_times))

        if self.verbose:
            print(f"UAV Mission Time: {self.time_uav} seconds")


    # def deployment_rate_uav(self) -> float: 
        
    #     effective_width = self.aerogel_width - (2*self.deployment_accuracy)
    #     if effective_width <= 0:
    #         raise ValueError("Effective aerogel width must be positive. Check deployment_accuracy.")
        
    #     n_layers = np.ceil(self.fire_break_width / effective_width)
    #     self.n_layers = n_layers

    #     self.uav_mission_time()

    #     perimeter_per_trip = self.aerogel_length / self.n_layers
    #     self.uav_deployment_rate = perimeter_per_trip / self.time_uav


    def calc_time_operation(self) -> float:
        """
        Calculates the total operation time required for the UAV mission.
        This method computes the number of cycles needed to complete the mission based on the number of aerogels and UAVs available. It then calculates the total operation time by multiplying the number of cycles by the time required for a single UAV mission. Optionally, it prints detailed information if verbose mode is enabled.
        Returns
        -------
        float
            The total operation time required for the mission in seconds.
        Notes
        -----
        - Assumes that `self.uav_mission_time()` sets `self.time_uav`.
        - The number of cycles is calculated as the ceiling of the ratio between the number of aerogels and the number of UAVs.
        - The result is stored in `self.time_operation`.
        """

        self.uav_mission_time()

        num_cycles = np.ceil(self.num_aerogels / self.number_of_UAV)
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
        """
        Calculates the total mission time by summing preparation, operation, and wrap-up phases.
        This method first computes the time required for each mission phase by calling their respective methods.
        It then checks if the UAV mission time is sufficient to cover the preparation time (accounting for nest startup time).
        If not, it raises a ValueError to indicate overlapping UAV operations.
        Finally, it sums the times for all phases to determine the total mission time and stores it as an attribute.
        Raises
        ------
        ValueError
            If the UAV mission time is less than the preparation time minus the nest startup time, indicating overlapping UAV operations.
        Notes
        -----
        - The method assumes that `calc_time_preparation`, `calc_time_operation`, and `calc_time_wrapup` are defined and update the corresponding attributes.
        - The margin check for `UAV_launch_time` is present but not yet implemented.
        """

        self.calc_time_preparation()
        self.calc_time_operation()
        self.calc_time_wrapup()

        if self.time_uav < self.time_preparation - self.time_startup_nest:
            raise ValueError("UAV mission time is less than preparation time, so UAVs will overlap. Check inputs.")
        else:
            total_mission_time = self.time_preparation + self.time_operation + self.time_wrapup
            self.total_mission_time = total_mission_time

        if self.UAV_launch_time > self.time_turnaround + self.margin:
            pass # ADD MARGIN STUFF


    def true_mission_deployment_rate(self) -> float:
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
        
        self.calc_total_mission_time()
        self.uav_deployment_rate = self.mission_perimeter / self.time_uav
        self.deployment_rate = self.mission_perimeter / self.total_mission_time

    # ~~~ Output functions ~~~ 
 
    def get_all(self) -> dict[str, float]:

        self.calc_total_mission_time()
        self.true_mission_deployment_rate()

        self.outputs["time_hover"] = self.hover_time
        self.outputs["time_cruise"] = self.cruise_time
        self.outputs["time_uav"] = self.time_uav

        self.outputs["time_preparation"] = self.time_preparation
        self.outputs["time_operation"] = self.time_operation
        self.outputs["time_wrapup"] = self.time_wrapup
        self.outputs["total_mission_time"] = self.total_mission_time
        self.outputs["true_deployment_rate"] = self.deployment_rate

        return self.outputs
    

if __name__ == '__main__':
    # Perform sanity checks here
    test_inputs_mission = {
        "number_of_UAV": 20,
        "number_of_nests": 2,
        "number_of_containers": 2,
        "number_of_slaves": 2,
        "time_wing_attachment": 10.0,
        "time_aerogel_loading": 20.0,
        "time_startup_UAV": 20.0,
        "time_between_containers": 30.0,
        "time_UAV_wrapup_check": 30.0,
        "time_UAV_turnaround_check": 30.0,
        "time_put_back_UAV": 10.0,
        "time_final_wrapup": 300.0,
        "time_between_UAV": 10.0,
        "time_startup_nest": 120.0,
        "time_battery_swapping": 10.0,
        "h_cruise": 120.0,  # Mission altitude [m]
        "V_climb_v": 6.0,  # Climb speed [m/s]
        "V_descent": 3.0,  # Descent speed [m/s]
        "V_cruise": 100/3.6,  # Cruise speed [m/s]
        "time_transition": 30.0,  # Time for transition [s]
        "time_deploy": 5.0*60,  # Time for deploying the UAV [s]
        "time_scan": 60,  # Time for scanning [s]
        "mission_perimeter": 10000.0,  # Mission perimeter [m]
        "R_max": 20000.0,  # Maximum range [m]
        "num_aerogels": 1000,  # Number of aerogels to deploy
        "margin": 5.0  # Margin for overlap check [s]   
    }

    mission = Mission(test_inputs_mission)
    outputs = mission.get_all()

    for key, value in outputs.items():
        print(f"{key}: {value}")

    print()
    print(f"Deployment Rate: {mission.deployment_rate*3600} m/hour")
    