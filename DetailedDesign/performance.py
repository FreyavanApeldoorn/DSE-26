import numpy as np

class Performance:

    def __init__(self, inputs: dict[str, float], hardware) -> None:
        self.inputs = inputs
        self.outputs = self.inputs.copy()
        self.hardware = hardware

        self.mission_type = inputs["mission_type"]

        self.total_mission_time = inputs["total_mission_time"]
        self.mission_perimeter = inputs["mission_perimeter"]
        self.time_uav_max = inputs["time_uav_max"]
        self.time_uav_min = inputs["time_uav_min"]

    # ~~~ Intermediate Functions ~~~

    def deployment_rates(self) -> float:
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
        
        if self.mission_type == "wildfire":
            self.uav_deployment_rate = self.mission_perimeter / self.time_uav_max
            self.mission_deployment_rate = self.mission_perimeter / self.total_mission_time

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