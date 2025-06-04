import numpy as np

'''
This is the file for the nest. It contains a single class.
'''

class Nest:

    def __init__(self, inputs: dict[str, float], verbose: bool = False) -> None:

        self.verbose = verbose
        self.inputs = inputs
        self.outputs = self.inputs.copy()
        
        # Mission parameters
        self.n_drones = inputs["number_of_UAVs"]
        self.number_of_trips = inputs["trips_for_mission"]

        self.mission_energy = inputs["required_capacity_wh"]
        self.nest_energy = self.mission_energy * self.number_of_trips  # minimum power the nest must be able to provide



        # UAV Dimensions 
        self.uav_span = inputs["wing_span"]
        self.uav_wing_area = inputs["wing_area"]
        self.FW_height = 0.3 # inputs["FW_height"]  # NEEDS TO BE UPDATED
        self.FW_width = 2.25 # inputs["FW_width"]  # NEEDS TO BE UPDATED
        self.uav_chord = self.uav_wing_area / self.uav_span if self.uav_span != 0 else 0 

        self.uav_mass = inputs["M_to"]

        # Aerogel dimensions
        self.aerogel_width = inputs["aerogel_width"]  # width of the aerogel
        self.aerogel_diameter = inputs["aerogel_diameter"]  # diameter of the aerogel

        # Generator parameters
        self.generator_efficiency = inputs["generator_efficiency"] 
        self.diesel_energy_density = inputs["biodiesel_energy_density"] # in Wh/kg
        self.diesel_density = inputs["biodiesel_density"] # in kg/liter
        self.generator_length = inputs["generator_length"] # 
        self.generator_width = inputs["generator_width"]
        self.generator_height = inputs["generator_height"]
        self.power_generator = inputs["generator_power"] * inputs["generator_power_factor"] # in W, assumed power output of the generator
        self.mass_generator = inputs["generator_mass"]
        self.internal_fuel_tank_volume = inputs["generator_internal_fuel_tank"]

        # Misc parameters


        # Nest contraints
        self.nest_length = inputs["nest_length"]
        self.nest_width = inputs["nest_width"]
        self.nest_height = inputs["nest_height"]
        self.nest_mass = inputs["nest_empty_mass"]

        self.available_volume_per_container = self.nest_length * self.nest_width * self.nest_height


    def uav_dimensions(self):

        """
        
        """

        uav_span = self.uav_span
        uav_width_FW = self.FW_width
        uav_heigh_FW = self.FW_height
        v_UAV_FW = uav_span * uav_width_FW * uav_heigh_FW  # m^3

        fuselage_length_margin = 0   # == MOVE TO INPUTS
        delta_fuselage_length = 0.5   # == MOVE TO INPUTS
        fuselage_width_margin = 0.5   # == MOVE TO INPUTS
        uav_fuselage_length = self.aerogel_width * (1 + fuselage_length_margin) + delta_fuselage_length  # m   ! this part might need to be adjusted based on the actual fuselage design
        uav_fuselage_width = self.aerogel_diameter * (1 + fuselage_width_margin)  # m
        v_UAV_fuselage = uav_fuselage_length * uav_fuselage_width * uav_fuselage_width

        self.uav_volume = v_UAV_FW + v_UAV_fuselage  # m^3


    def generator_sizing(self):
        
        """
        
        Choose:
        - Generator length, width, height (chosen to be an ISO container)
        - Generator efficiency
        - 
        """

        # Generator volume:
        self.volume_generator = self.generator_length * self.generator_width * self.generator_height    # calculating the volume of the generator in m^3

        # Fuel tank: 
        fuel_tank_margin = 0.1 # margin added for the fuel tank volume, to account for the space taken by the fuel tank structure and fittings
        self.external_fuel_tank_volume = self.generator_width * (self.nest_width * (1 - fuel_tank_margin)) * ((self.nest_height - self.generator_height) * (1 - fuel_tank_margin))

        diesel_volumetric_energy_density = self.diesel_energy_density * self.diesel_density  # in Wh/m^3, converting from Wh/kg to Wh/m^3 
        
        self.total_fuel_tank_volume = self.internal_fuel_tank_volume + self.external_fuel_tank_volume
        
        self.external_fuel_tank_capacity = self.external_fuel_tank_volume * diesel_volumetric_energy_density  # in Wh, total energy capacity of the fuel tank
        
        self.total_available_energy = (self.internal_fuel_tank + self.external_fuel_tank_capacity) * self.generator_efficiency

        percentage_energy_achieved = self.total_available_energy / self.mission_energy

        if percentage_energy_achieved >= 1:
            self.refills_for_mission = 0
        else:
            self.refills_for_mission = np.ceil(1 / percentage_energy_achieved)

        self.nest_trips_capacity = self.total_available_energy / self.mission_energy

        # Remaining length with generator addition:
        l_op = self.nest_length - self.generator_width   # Assuming the generator is placed with its length along the nest's width
        self.l_minus_gen = l_op 


        if self.verbose:
            print(f"Volume of generator: {self.volume_generator:.2f} m^3")
            print(f"External fuel tank volume: {self.external_fuel_tank_volume:.2f} m^3")
            print(f"Internal fuel tank capacity: {self.internal_fuel_tank:.2f} L")
            print(f"External fuel tank capacity: {self.external_fuel_tank_capacity:.2f} Wh")
            print(f"Total available energy: {self.total_available_energy:.2f} Wh")
            print(f"Refills needed for the mission: {self.refills_for_mission}")



    def misc_sizing(self):


        # Assigning fractions for electronics and equipment
        v_locker = 0.5*0.5
        VF_electronics = 0.05
        VF_equipment = 0.05
        MF_electronics = 0.05
        MF_equipment = 0.05

        self.v_electronics = VF_electronics * self.available_volume_per_container 
        self.v_equipment = VF_equipment * self.available_volume_per_container

        self.v_locker = v_locker


        area_human = self.nest_height * 0.6  # m^2
        v_operating_space = area_human * self.l_minus_gen
        self.v_operating_space_gen = v_operating_space
        self.v_operating_space_nogen = area_human * self.nest_length

        if self.verbose:
            print(f"Volume of electronics: {self.v_electronics:.2f} m^3")
            print(f"Volume of equipment: {self.v_equipment:.2f} m^3")
            print(f"Volume of locker: {self.v_locker:.2f} m^3")
            print(f"Volume of operating space with generator: {self.v_operating_space_gen:.2f} m^3")
            print(f"Volume of operating space without generator: {self.v_operating_space_nogen:.2f} m^3")



    def uavs_battery_sizing(self):


        # UAVs volume:
        VF_UAV_margin = 0.1   # fraction of UAV volume for margin
        uav_volume = (self.uav_volume) * (1 + VF_UAV_margin) # UAV volume in m^3


        # UAV batteries volume:
        VF_UAV_battery = 0.3   # fraction of UAV volume for battery
        battery_size = VF_UAV_battery * uav_volume # battery size in m^3

        self.v_uav_bat = uav_volume + battery_size

        if self.verbose:
            print(f"Volume of UAVs: {uav_volume:.2f} m^3")
            print(f"Volume of batteries: {battery_size:.2f} m^3")
            print(f"Total volume of UAVs and batteries: {self.v_uav_bat:.2f} m^3")


    def volume_sizing(self):

        """
        
        Parameters that must be defined:
        - VF_generator: fraction of nest volume for generator
        - VF_UAV_battery: fraction of UAV volume for battery
        - VF_UAV_margin: fraction of UAV volume for margin (between drones)



        """
        # Calculate the total volume available for one nest
        available_volume_per_nest = self.nest_length * self.nest_width * self.nest_height

        self.uav_dimensions()  
        self.uavs_battery_sizing()
        self.generator_sizing()        
        self.misc_sizing()
        

        v_op_gen = available_volume_per_nest - self.volume_generator - self.v_locker - self.v_operating_space_gen
        v_op_nogen = available_volume_per_nest - self.v_locker - self.v_operating_space_nogen
        



        # if self.verbose:
        #     print(f"v_op_gen: {v_op_gen:.2f} m^3")
        #     print(f"v_op_nogen: {v_op_nogen:.2f} m^3")


        v_tot_uav_bat = self.v_uav_bat * self.n_drones

        if v_op_gen > v_tot_uav_bat:
            n_containers = 1
            n_cap_nest_gen = int(v_op_gen // self.v_uav_bat)
            empty_slots = n_cap_nest_gen - self.n_drones

        else:
            n_cap_nest_gen = int(v_op_gen // self.v_uav_bat)  # Number of whole drones (with battery) that fit in v_op
            n_remaining = int(self.n_drones - n_cap_nest_gen)

            # print(f"number of remaining drones: {n_remaining}")

            # n_cap_nest_nogen = int(v_op_nogen // self.v_uav_bat)  # Number of drones in overflow container
            # n_nest_nogen = n_remaining // n_cap_nest_nogen  # Number of overflow containers needed

            # empty_slots = (n_cap_nest_nogen * n_nest_nogen) - n_remaining

            # if self.verbose
            #     print(f"Number of drones that fit in generator nest: {n_cap_nest_gen}")
            #     print(f"Number of drones remaining: {n_remaining}")
            #     print(f"Number of drones that fit in non-generator nest: {n_cap_nest_nogen}")
            #     print(f"Number of overflow nests needed: {n_nest_nogen}")
            #     print(f"Empty slots in last overflow nest: {empty_slots}")

            # n_containers = 1 + n_nest_nogen
            n_cap_nest_nogen = int(v_op_nogen // self.v_uav_bat)  # Number of drones in overflow container
            n_nest_nogen = int(np.ceil(n_remaining / n_cap_nest_nogen))  # Number of overflow containers needed

            # Number of drones in the last overflow nest
            drones_in_last_nest = n_remaining % n_cap_nest_nogen
            if drones_in_last_nest == 0:
                empty_slots = 0
            else:
                empty_slots = n_cap_nest_nogen - drones_in_last_nest

            if self.verbose:
                print(f"Number of drones that fit in generator nest: {n_cap_nest_gen}")
                print(f"Number of drones remaining: {n_remaining}")
                print(f"Number of drones that fit in non-generator nest: {n_cap_nest_nogen}")
                print(f"Number of overflow nests needed: {n_nest_nogen}")
                print(f"Empty slots in last overflow nest: {empty_slots}")

            n_containers = 1 + n_nest_nogen


        self.n_nests = n_containers
        self.n_extra = empty_slots
        self.n_drones = self.n_drones + empty_slots

        self.nests_volume = self.n_nests * available_volume_per_nest

        if self.verbose:
            print(f"Number of nests needed: {self.n_nests}")
            print(f"Number of extra slots in the last nest: {self.n_extra}")
            print(f"Volume available per nest: {available_volume_per_nest:.2f} m^3")
            print(f"Volume of generator: {self.volume_generator:.2f} m^3")
            print(f"Volume of electronics and equipment (locker): {self.v_locker:.2f} m^3")
            print(f"Volume of operating space with generator: {self.v_operating_space_gen:.2f} m^3")
            print(f"Volume of operating space without generator: {self.v_operating_space_nogen:.2f} m^3")
            print(f"Volume of UAVs and batteries: {v_tot_uav_bat:.2f} m^3")


    def mass_sizing(self):

        pass


    def energy_sizing(self):
        pass

    def deployment_time():
        pass


    # ~~~ Output functions ~~~ 

    def get_all(self) -> dict[str, float]:

        self.volume_sizing()

        self.outputs["number_of_nests"] = self.n_nests
        #self.outputs["number_of_UAVs"] = self.n_drones

        self.outputs["nests_volume"] = self.nests_volume
        self.outputs["volume_fueltank"] = self.fuel_tank_volume
        self.outputs["refills_for_mission"] = self.refills_for_mission
        
        #self.outputs["Nest_mass"] = ...

        return self.outputs
    
if __name__ == '__main__':
    # Example usage

    misc_elemenets = {
        "mop_": 0.5 
    }

    inputs = {
        # Mission parameters
        "number_of_UAVs": 20,
        "trips_for_mission": 10,
        "required_capacity_wh": 1000,  # Total energy required for the mission in Wh

        # UAV Dimensions
        "wing_span": 3.0,
        "wing_area": 1.8,
        "FW_height": 0.3,
        "FW_width": 2.25,
        "M_to": 30.0,  # Maximum takeoff mass of the UAV in kg

        # Aerogel dimensions 
        "aerogel_width": 1.5,  # width of the aerogel in m
        "aerogel_diameter": 0.2,  # diameter of the aerogel in m

        # NEST PARAMETERS ======================================================

        # Generator parameters
        "generator_efficiency": 0.3,
        "biodiesel_energy_density": 9.94,  # in Wh/kg
        "biodiesel_density": 0.88,  # in kg/liter
        #- https://www.cat.com/en_MX/products/new/power-systems/electric-power/diesel-generator-sets/106402.html
        "generator_length": 2.278,  # [m] length of the generator
        "generator_width": 0.9,  # [m] width of the generator
        "generator_height": 1.322,  # [m] height of the generator
        "generator_power": 65*1000,  # [VA] assumed power output of the generator
        "generator_power_factor": 0.8,  # power factor of the generator
        "generator_mass": 1031 ,  # [kg] mass of the generator
        "generator_internal_fuel_tank": 103, # [L] internal fuel tank capacity of the generator
        "generator_cost": None,
        "operating_temperature": 55, # operating temperature of the generator in Celsius 

        # Misc parameters
        "nest_locker_length": 0.5,  # length of the locker in m
        "next_locker_width": 0.5,  # width of the locker in m


        # Nest parameters
        "nest_empty_mass": 100.0,  
        "nest_length": 5.9,  # length of the nest in m
        "nest_width": 2.35,  # width of the nest in m
        "nest_height": 2.39  # height of the nest in m

    }

    nest = Nest(inputs, verbose=True)
    outputs = nest.get_all()
    for key, value in outputs.items():
        print(f"{key}: {value}")
    