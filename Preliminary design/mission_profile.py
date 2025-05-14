
import numpy as np
import matplotlib.pyplot as plt


"""
inputs:

"""





# def rate_of_climb(P_a, P_r, W):

#     ROC = (P_a - P_r) / W

#     return ROC


# def rate_of_descent(P_a, P_r, W):



# #==============================




# #==============================


def power_load(P_load=1000):
    """
    P_load: power to load the UAV
    """

    return P_load


def power_ascent(P_a_VTOL):

    """
    P_a_VTOL: power available (assuming full power) (Vanessa)
    """

    return P_a_VTOL


def power_transition(P_a_transition):
    return P_a_transition



def power_cruise(P_a_FW):

    """
    P_a_FW: power to cruise (Frank)
    """

    return P_a_FW


def power_descent(P_r, P_a_VTOL):

    P_descent = P_r - (P_a_VTOL - P_r)   # giving the same ROC as in ascent

    return P_descent


def power_deploy(P_deploy=1000):

    """
    P_deploy: power to deploy the UAV
    """

    return P_deploy



# P_load, P_a_VTOL, P_a_FW, P_a_transition, P_r (hover), P_deploy





class MissionProfile:

    """
    Class to define the mission profile of a UAV

    Parameters
    ----------
    mission_parameters: dict
        Dictionary containing the mission parameters
    time_estimates: dict
        Dictionary containing the time estimates for each phase of the mission
    power_requirements: dict
        Dictionary containing the power requirements for each phase of the mission

    Attributes
    ----------
    h_cruise: float
        Cruise altitude in meters
    R_max: float
        Maximum range in meters
    V_climb_v: float
        Climb speed in m/s
    V_cruise: float
        Cruise speed in m/s
    V_descent: float
        Descent speed in m/s
    t_load: float
        Time to load the UAV in seconds
    t_transition: float
        Time to transition from VTOL to FW in seconds
    t_scan: float
        Time to scan the area in seconds
    t_deploy: float
        Time to deploy the UAV in seconds
    t_recharge: float
        Time to recharge the UAV in seconds
    P_load: float
        Power to load the UAV in watts
    P_a_VTOL: float
        Power available for VTOL in watts
    P_r_FW: float
        Power required for FW in watts
    P_a_transition: float
        Power available for transition in watts
    P_r: float
        Power required for hover in watts
    P_deploy: float
        Power to deploy the UAV in watts

    Methods
    -------

    """

    def __init__(self, mission_parameters: dict, time_estimates: dict, power_requirements: dict) -> None:         
        self.h_cruise = mission_parameters["h_cruise"]
        self.R_max = mission_parameters["R_max"]
        self.V_climb_v = mission_parameters["V_climb_v"]
        self.V_cruise = mission_parameters["V_cruise"]
        self.V_descent = mission_parameters["V_descent"]

        self.t_load = time_estimates["t_load"]
        self.t_transition = time_estimates["t_transition"]
        self.t_scan = time_estimates["t_scan"]
        self.t_deploy = time_estimates["t_deploy"]
        self.t_recharge = time_estimates["t_recharge"]

        self.P_load = power_requirements["P_load"]
        self.P_a_VTOL = power_requirements["P_a_VTOL"]
        self.P_r_FW = power_requirements["P_r_FW"]
        self.P_a_transition = power_requirements["P_a_transition"]
        self.P_r = power_requirements["P_r"]
        self.P_deploy = power_requirements["P_deploy"]
        


    def time_load(self):
        """
        t_load: time to load the UAV
        """

        return self.t_load


    def time_ascent(self):

        """
        t_ascent: time to ascend to cruise altitude
        """

        t_ascent = self.h_cruise / self.V_climb_v
        
        return t_ascent


    def time_transition(self):
        
        """
        t_transition: time to transition from VTOL to FW
        """

        return self.t_transition


    def time_cruise(self):

        """
        Assuming same cruise speed in both directions
        """

        t_cruise = self.R_max / self.V_cruise
        
        return t_cruise


    def time_descent(self):
        
        """
        t_descent: time to descend to ground
        """

        t_descent = self.h_cruise / self.V_descent
        
        return t_descent



    def time_scan(self):

        """
        t_scan: time to scan the area
        """

        return self.t_scan


    def time_deploy(self):

        """
        t_deploy: time to deploy the UAV
        """

        return self.t_deploy


    def time_recharge(self):

        """
        t_recharge: time to recharge the UAV
        """

        return self.t_recharge

    

    def mission_profile(self):

        t_load = self.time_load()
        t_ascent = self.time_ascent()
        t_transition = self.time_transition()
        t_cruise = self.time_cruise()
        t_descent = self.time_descent()
        t_scan = self.time_scan()
        t_deploy = self.time_deploy()
        t_recharge = self.time_recharge()

        times = [t_load, t_ascent, t_transition, t_cruise, t_transition, t_descent, t_scan, t_deploy, t_ascent, t_transition, t_cruise, t_transition, t_descent, t_recharge]
        times = np.array(times)
        total_time = np.sum(times)

        powers = [self.P_load, self.P_a_VTOL, self.P_a_transition, self.P_r_FW, self.P_a_transition, self.P_r, self.P_r, self.P_deploy, self.P_a_VTOL, self.P_a_transition, self.P_r_FW, self.P_a_transition, self.P_r, self.P_load]
        powers = np.array(powers)
        total_power = np.sum(powers)

        energies = times * powers
        total_energy = np.sum(energies)

        return total_time, total_energy, times, energies, powers
    

    def 

    

    def plot_energy_consumption(self):
        """
        Plot the mission profile
        """

        times = self.mission_profile()[2]
        energies = self.mission_profile()[3]

        plt.figure(figsize=(10, 6))
        plt.bar(range(len(times)), energies/3600, tick_label=['Load', 'Ascent', 'Transition', 'Cruise', 'Transition', 'Descent', 'Scan', 'Deploy', 'Ascent', 'Transition', 'Cruise', 'Transition', 'Descent', 'Recharge'])
        plt.ylabel('Energy (Wh)')
        plt.title('Mission Profile')
        plt.xticks(rotation=45)
        plt.grid(axis='y')
        plt.tight_layout()
        plt.show()

    def plot_power_consumption(self):
        """
        Plot the power consumption over time
        """

        times = self.mission_profile()[2]
        powers = self.mission_profile()[4]

        time_points = np.cumsum(times)  # Cumulative time points
        time_points = np.insert(time_points, 0, 0)  # Add starting point at time 0

        plt.figure(figsize=(10, 6))
        plt.step(time_points / 60, np.append(powers, powers[-1]), where='post', label='Power Consumption')
        plt.xlabel('Time (minutes)')
        plt.ylabel('Power (W)')
        plt.title('Power Consumption Over Mission Duration')
        plt.grid()
        plt.legend()
        plt.tight_layout()
        plt.show()

    

#===============================
#===============================
# Example usage


mission_definition = []   # Define the mission profile here
mission_parameters = {"h_cruise": 120, "R_max": 30000, "V_climb_v": 3, "V_cruise": 70/3.6, "V_descent": 3}   
time_estimates = {"t_load": 1*60, "t_transition": 30, "t_scan": 60, "t_deploy": 5*60, "t_recharge": 5*60}
power_requirements = {"P_load": 300, "P_a_VTOL": 4500, "P_r_FW": 1500, "P_a_transition": 6000, "P_r": 3500, "P_deploy": 4000}


mission = MissionProfile(mission_parameters, time_estimates, power_requirements)


total_time, total_energy, times, energies, powers = mission.mission_profile()

print("Total mission time: ", total_time/60, "minutes")
print("Total energy required: ", total_energy/3600, "Wh")

mission.plot_energy_consumption()
mission.plot_power_consumption()
