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
        #Mission Specifics
        self.mission_perimeter = inputs["mission_perimeter"] #We define, mission perimeter [m] 
    # ~~~ Intermediate Functions ~~~

    def time_preparation(self) -> float: #Verified
        #Bottom point graph
        UAV_preparation_time = self.time_wing_attachment + self.time_aerogel_loading +  self.time_startup_UAV + self.time_between_UAV # Time for 1 UAV to prepare
        #Top point graph
        time_preparation_1worker = (UAV_preparation_time * self.number_of_UAV + self.time_between_containers * self.number_of_containers) #Assume containers relatively closer together, linear relation walking time, upper bound
        time_slope = (UAV_preparation_time - time_preparation_1worker)/(self.number_of_UAV - 1)
        if self.number_of_slaves >= self.number_of_UAV:
            time_preparation = UAV_preparation_time + self.time_startup_nest
        elif self.number_of_slaves < 1:
            raise ValueError("Number of slaves must be at least 1, that is a big problem!")
        else: 
            time_preparation = time_preparation_1worker + time_slope * (self.number_of_slaves - 1) + self.time_startup_nest #Assume containers relatively closer together, linear relation walking time, upper bound
        return time_preparation 

    def time_operation(self) -> float:
        time_turnaround = self.time_UAV_turnaround_check + self.time_battery_swapping + self.time_aerogel_loading # Time for 1 UAV to turnaround nothing special
        time_operation_ideal_conditions = self.mission_perimeter/ ()
        pass


    def time_wrapup(self) -> float: #Verified
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
        return time_wrapup
    
    def total_mission_time(self) -> float:

        return
        #return self.time_preparation + time_operation + time_wrapup

    # ~~~ Output functions ~~~ 
 
    def get_all(self) -> dict[str, float]:

        self.outputs["time_preparation"] = self.time_preparation()
        self.outputs["time_operation"] = self.time_operation
        self.outputs["time_wrapup"] = self.time_wrapup()
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
    