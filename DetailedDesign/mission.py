import numpy as np

'''
This is the file for the mission. It contains a single class.
'''

class Mission:

    def __init__(self, inputs: dict[str, float]) -> None:
        
        self.inputs = inputs
        self.outputs = self.inputs.copy() # Copy inputs to outputs

        #Nest
        self.number_of_UAV = inputs["number_of_UAV"] #expected from nest per nest
        self.number_of_containers = inputs["number_of_containers"] #expected from nest
        self.number_of_nests = inputs["number_of_nests"] #expected from nest
        self.number_of_slaves = inputs["number_of_slaves"] #We define, per nest

        #Input Times
        self.time_wing_attachment = inputs["time_wing_attachment"] #We define, upper bound [s]
        self.time_aerogel_loading = inputs["time_aerogel_loading"] #We define, upper bound [s]
        self.time_startup_UAV = inputs["time_startup_UAV"] #We define, upper bound [s]
        self.time_between_containers = inputs["time_between_containers"] #We define, upper bound, time to walk between containers, no walking between nest [s]
        self.time_UAV_wrapup_check = inputs["time_UAV_wrapup_check"] #We define, upper bound, time to check UAVs [s]
        self.time_UAV_turnaround_check = inputs["time_UAV_turnaround_check"] #We define, upper bound, time to check UAVs [s]
        self.time_put_back_UAV = inputs["time_put_back_UAV"] #We define, upper bound, time to put back UAVs [s]
        self.time_startup_nest = inputs["time_startup_nest"] #We define, upper bound, time to startup nest [s]
        self.time_final_wrapup = inputs["time_final_wrapup"] #We define, upper bound, time to wrap up Nest [s]
        self.time_between_UAV = inputs["time_between_UAV"] #We define, upper bound, time to walk between UAVs [s]
        self.time_battery_swapping = inputs["time_battery_swapping"] #We define, upper bound, time to swap batteries [s]

        #UAV Inputs
        self.h_cruise = inputs["h_cruise"] # Mission altitude [m]: mission definition
        self.V_climb_v = inputs["V_climb_v"] # Climb speed [m/s]: mission definition
        self.V_descent = inputs["V_descent"] # Descent speed [m/s]: mission definition
        self.V_cruise = inputs["V_cruise"] # Cruise speed [m/s]: mission definition

        self.time_transition = inputs["time_transition"]
        self.time_deploy = inputs["time_deploy"] # Time for deploying the UAV [s]: From UAV design
        self.time_scan = inputs["time_scan"] # Time for scanning [s]: From UAV design 

        #Mission Specifics
        self.mission_perimeter = inputs["mission_perimeter"] #We define, mission perimeter [m] 
        self.R_max = inputs["R_max"] # Maximum range [m]: mission definition
        self.fire_break_width = inputs["fire_break_width"]


        #Aerogel Specifics
        self.aerogel_length = inputs["aerogel_length"]
        self.aerogel_width = inputs["aerogel_width"] 
        self.deployment_accuracy = inputs["deployment_accuracy"] 



        self.num_aerogels = inputs["num_aerogels"]

        

    # ~~~ Intermediate Functions ~~~

    def calc_time_preparation(self) -> float:
        #Bottom point graph
        UAV_launch_time = self.time_wing_attachment + self.time_aerogel_loading +  self.time_startup_UAV + self.time_between_UAV # Time for 1 UAV to prepare
        self.UAV_launch_time = UAV_launch_time  # cache launch time

        #Top point graph
        time_launch_1worker = (UAV_launch_time * self.number_of_UAV + self.time_between_containers * self.number_of_containers) #Assume containers relatively closer together, linear relation walking time, upper bound
        time_slope = (UAV_launch_time - time_launch_1worker)/(self.number_of_UAV - 1)
        if self.number_of_slaves >= self.number_of_UAV:
            time_preparation = UAV_launch_time + self.time_startup_nest
        elif self.number_of_slaves < 1:
            raise ValueError("Number of slaves must be at least 1, that is a big problem!")
        else: 
            time_preparation = time_launch_1worker + time_slope * (self.number_of_slaves - 1) + self.time_startup_nest #Assume containers relatively closer together, linear relation walking time, upper bound
        
        self.time_preparation = time_preparation


    def calc_time_turn_around(self) -> float:
        time_turnaround_min = self.time_UAV_turnaround_check + self.time_battery_swapping + self.time_aerogel_loading # Time for 1 UAV to turnaround nothing special
        self.time_turnaround = time_turnaround_min # Assuming 


    def uav_mission_time(self) -> float: 
        
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
        
        time_operation_design = self.mission_perimeter/ (self.number_of_UAV * (self.uav_deployment_rate))
        self.time_operation_design = time_operation_design 


    def calc_time_wrapup(self) -> float: #Verified
        #Bottom point graph
        UAV_wrapup_time = self.time_wing_attachment + self.time_put_back_UAV + self.time_UAV_wrapup_check + self.time_between_UAV # Time for 1 UAV to wrapup
        #Top point graph
        time_wrapup_1worker = (UAV_wrapup_time * self.number_of_UAV + self.time_between_containers * self.number_of_containers)
        time_slope = (UAV_wrapup_time - time_wrapup_1worker)/(self.number_of_UAV - 1)
        if self.number_of_slaves >= self.number_of_UAV:
            time_wrapup = UAV_wrapup_time + self.time_final_wrapup
        elif self.number_of_slaves < 1:
            raise ValueError("Number of slaves must be at least 1, that is a big problem!")
        else:
            time_wrapup = time_wrapup_1worker + time_slope * (self.number_of_slaves - 1) + self.time_final_wrapup
        
        self.time_wrapup = time_wrapup 
        

    def calc_total_mission_time(self) -> float:

        self.time_preparation()
        self.time_operation()
        self.time_wrapup()

        if self.time_uav < self.time_preparation - self.time_startup_nest:
            raise ValueError("UAV mission time is less than preparation time, so UAVs will overlap. Check inputs.")
        else:
            total_mission_time = self.time_preparation + self.time_operation + self.time_wrapup
            self.total_mission_time = total_mission_time

        if self.UAV_launch_time > self.time_turnaround + self.margin:
            pass # ADD MARGIN STUFF


    def mission_deployment_rate(self) -> float:
        
        self.mission_perimeter / 

    # ~~~ Output functions ~~~ 
 
    def get_all(self) -> dict[str, float]:

        self.total_mission_time()

        self.outputs["time_hover"] = ...
        self.outputs["time_cruise"] = ...
        # self.outputs["time_"]

        self.outputs["time_preparation"] = self.time_preparation
        self.outputs["time_operation"] = self.time_operation
        self.outputs["time_wrapup"] = self.time_wrapup
        self.outputs["total_mission_time"] = self.total_mission_time

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
        
    }

    mission = Mission(test_inputs_mission)

    #Verification of the inputs
    time_prep = mission.time_preparation()
    time_wrapup = mission.time_wrapup()
    print(f"Time preparation: {time_prep} seconds")
    print(f"Time wrapup: {time_wrapup} seconds")
    