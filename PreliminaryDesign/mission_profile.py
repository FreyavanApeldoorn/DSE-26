
import numpy as np
import matplotlib.pyplot as plt

class UAVProfile:

    """
    Class to define the mission profile of a UAV

    Parameters
    ----------
    inputs: dict
        Dictionary containing the mission parameters
    inputs: dict
        Dictionary containing the time estimates for each phase of the mission
    inputs: dict
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
    P_r_VTOL: float
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

    def __init__(self, inputs: dict) -> None:    
        self.inputs = inputs     
        self.h_cruise = inputs["h_cruise"]
        self.R_max = inputs["R_max"]
        self.V_climb_v = inputs["V_climb_v"]
        self.V_cruise = inputs["V_cruise"]
        self.V_descent = inputs["V_descent"]

        self.t_load = inputs["t_load"]
        self.t_transition = inputs["t_transition"]
        self.t_scan = inputs["t_scan"]
        self.t_deploy = inputs["t_deploy"]
        self.t_recharge = inputs["t_recharge"]

        self.P_load = inputs["P_load"]
        self.P_r_VTOL = inputs["P_r_VTOL"]
        self.P_r_FW = inputs["P_r_FW"]
        self.P_a_transition = inputs["P_a_transition"]
        self.P_r = inputs["P_r"]
        self.P_deploy = inputs["P_deploy"]
        


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

    

    def size_uav_profile(self):

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
        self.times_array = times
        total_time = np.sum(times)

        powers = [self.P_load, self.P_r_VTOL, self.P_a_transition, self.P_r_FW, self.P_a_transition, self.P_r, self.P_r, self.P_deploy, self.P_r_VTOL, self.P_a_transition, self.P_r_FW, self.P_a_transition, self.P_r, self.P_load]
        powers = np.array(powers)
        self.powers_array = powers
        total_power = np.sum(powers)

        energies = times * powers
        self.energies_array = energies
        total_energy = np.sum(energies)

        self.inputs['total_mission_time'] = total_time
        self.inputs['total_mission_energy'] = total_energy
        #self.inputs['mission_times_array'] = times
        #self.inputs['mission_energies_array'] = energies
        #self.inputs['mission_powers_array'] = powers

        return self.inputs
    
    

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

    




class SwarmProfile:
    """
    A class to model and size a swarm of drones for wildfire and oil spill containment missions,
    focusing on aerogel deployment for creating fire breaks.
    Attributes:
        verbose (bool): If True, enables verbose output for debugging.
        inputs (dict): Dictionary containing all input parameters for the mission.
        fire_break_width (float): Required width of the fire break to be created.
        R_max (float): Maximum allowed radius or range constraint for the mission.
        n_drones (int): Number of drones in the swarm.
        n_nests (int): Number of nests or deployment bases.
        aerogel_length (float): Length of aerogel deployed by each drone per mission.
        aerogel_width (float): Width of the aerogel strip.
        aerogel_thickness (float): Thickness of the aerogel strip.
        uav_mission_time (float): Total mission time for one drone.
        uav_mission_energy (float): Total mission energy consumed by one drone.
        deployment_accuracy (float): Deployment accuracy margin to account for placement errors.
        n_layers (float): Number of aerogel layers required to cover the fire break width.
    Methods:
        required_layers():
            Calculates the number of aerogel layers required to cover the fire break width,
            accounting for deployment accuracy. Raises ValueError if effective width is non-positive.
        mission_performance():
            Computes the swarm's deployment rate (meters/second) and total energy consumption
            for the mission, considering all drones and required layers.
        update_parameters():
            Updates the input dictionary with calculated swarm deployment rate and energy,
            and returns the updated dictionary.
    """

    def __init__(self, inputs, verbose=False):
        """
        Initializes the mission profile with the provided input parameters.
        Parameters
        ----------
        inputs : dict
            Dictionary containing all required input parameters:
                - required_perimeter (float): The total perimeter (in meters) that needs to be covered for wildfire or oil spill containment.
                - fire_break_width (float): The width (in meters) of the fire break to be created.
                - R_max (float): The maximum allowed radius or constraint for the mission.
                - n_drones (int): Number of drones to be deployed in the mission.
                - n_nests (int): Number of nests (deployment bases) to be used.
                - aerogel_length (float): Length (in meters) of the aerogel material used.
                - aerogel_width (float): Width (in meters) of the aerogel material used.
                - aerogel_thickness (float): Thickness (in meters) of the aerogel material used.
                - total_mission_time (float): Total mission time (in seconds or minutes, as specified).
                - total_mission_energy (float): Total energy consumption for the mission.
                - deployment_accuracy (float): Accuracy (as a percentage or value) of the deployment process.
        verbose : bool, optional
            If True, prints detailed information about the initialization process. Default is False.
        """

        

        self.verbose = verbose

        self.inputs = inputs

        # Parameters to do with wildfire & oil spill requirements
        # self.required_perimeter is no longer required as input

        self.required_perimeter = inputs["required_perimeter"]
        self.fire_break_width = inputs["fire_break_width"]

        if self.verbose:
            print(f"Fire break width: {self.fire_break_width} m")
            print(f"Required perimeter: {self.required_perimeter} m")

        # Constraints
        self.R_max = inputs["R_max"]

        # Things we vary within the mission
        self.n_drones = inputs["n_drones"]
        self.n_nests = inputs["n_nests"]

        self.aerogel_length = inputs["aerogel_length"]
        self.aerogel_width = inputs["aerogel_width"]
        self.aerogel_thickness = inputs["aerogel_thickness"]

        # Previous calculation results
        self.uav_mission_time = inputs["total_mission_time"]
        self.uav_mission_energy = inputs["total_mission_energy"]

        # Deployment parameters:
        self.deployment_accuracy = inputs["deployment_accuracy"]


    def required_layers(self):
        """
        Calculates and returns the number of aerogel layers required to cover the fire break perimeter,
        accounting for deployment accuracy.
        The method computes the effective width of each aerogel layer by subtracting the deployment
        accuracy from the nominal aerogel width. It then determines how many such layers are needed to
        span the total fire break width. If the effective width is not positive, a ValueError is raised.
        Returns:
            float: The number of layers required to cover the fire break perimeter.
        Raises:
            ValueError: If the effective aerogel width is not positive.
        Side Effects:
            Sets self.n_layers to the calculated number of layers.
            If self.verbose is True, prints the number of layers required.
        """

        

        # Increase width to account for deployment accuracy
        effective_width = self.aerogel_width - (2*self.deployment_accuracy)
        if effective_width <= 0:
            raise ValueError("Effective aerogel width must be positive. Check deployment_accuracy.")
        
        n_layers = np.ceil(self.fire_break_width / effective_width)
        self.n_layers = n_layers

        if self.verbose:
            print(f"Number of layers for perimeter coverage: {n_layers}")

        return n_layers


    def mission_performance(self):
        """
        Calculates and returns the swarm deployment rate and total energy consumption for the mission.
        This method computes:
            - The total deployed aerogel length for the mission, considering the number of drones and required layers.
            - The deployment rate, defined as the total deployed aerogel length divided by the mission time.
            - The total energy consumption for all drones and layers during the mission.
        Updates:
            self.inputs["swarm_deployment_rate"]: The deployment rate (meters/second).
            self.inputs["swarm_energy"]: The total energy consumed (units as per uav_mission_energy).
        Returns:
            tuple:
                deployment_rate (float): The rate at which aerogel is deployed by the swarm (meters/second).
                total_energy (float): The total energy consumed by the swarm during the mission.
        """

        self.n_layers = self.required_layers()

        # The total deployed aerogel length per mission
        perimeter_per_trip = self.aerogel_length / self.n_layers
        required_trips = np.ceil(self.required_perimeter / perimeter_per_trip)
        required_cycles = required_trips / self.n_drones
        self.required_trips, self.required_cycles = required_trips, required_cycles

        if self.verbose:
            print(f"Perimeter per trip: {perimeter_per_trip} m")
            print(f"Number of trips required: {required_trips}")
            print(f"Number of cycles required: {required_cycles}")

        # Deployment rate: meters of aerogel deployed per second (all drones, all layers)
        deployment_rate = perimeter_per_trip / self.uav_mission_time
        self.deployment_rate = deployment_rate

        # Calculate energy consumption (all drones, all layers)
        total_energy = self.uav_mission_energy * self.required_trips
        self.total_energy = total_energy
        self.total_energy_per_nest = total_energy / self.n_nests

        total_time = self.uav_mission_time * self.required_cycles
        self.swarm_time = total_time

        if self.verbose:
            print(f"Deployment rate: {deployment_rate} m/s")
            print(f"Total energy consumption: {total_energy} J")
            print(f"Total mission time: {total_time/60} minutes")



    def size_swarm_profile(self):
        """
        Updates the input parameters with the latest swarm deployment rate and total energy.
        This method calls `mission_performance()` to retrieve the current deployment rate and total energy
        required for the mission. It then updates the `inputs` dictionary with these values under the keys
        'swarm_deployment_rate' and 'swarm_energy', respectively.
        Returns:
            dict: The updated inputs dictionary containing the new deployment rate and energy values.
        """

        self.mission_performance()
        self.inputs["swarm_deployment_rate"] = self.deployment_rate   # meters/second
        self.inputs["swarm_energy"] = self.total_energy
        self.inputs["nest_energy"] = self.total_energy_per_nest
        self.inputs["swarm_time"] = self.swarm_time
        self.inputs["required_trips"] = self.required_trips
        self.inputs["required_cycles"] = self.required_cycles


        return self.inputs



# example usage
if __name__ == '__main__':
    mission_definition = []   # Define the mission profile here
    swarm_inputs = {"h_cruise": 120, "R_max": 30000, "V_climb_v": 3, "V_cruise": 120/3.6, "V_descent": 3, "required_perimeter": 1000, 
                    "n_drones": 20, "n_nests": 1, "aerogel_length": 5, "aerogel_width": 1.5, "aerogel_thickness": 0.1, "deployment_accuracy": 0.1, "fire_break_width": 3}   
    uav_inputs = {"total_mission_time":1200, "total_mission_energy": 4000, "t_load": 1*60, "t_transition": 30, "t_scan": 60, "t_deploy": 5*60, "t_recharge": 5*60,
                  "P_load": 100, "P_r_VTOL": 3500, "P_r_FW": 1100, "P_a_transition": 4600, "P_r": 3500, "P_deploy": 4000}
    
    inputs = swarm_inputs.copy()
    inputs.update(uav_inputs)

    #mission = MissionProfile(inputs, inputs, inputs)

    Swarm = SizeSwarm(inputs, verbose=True)
    inputs = Swarm.update_parameters()

    print(inputs)
