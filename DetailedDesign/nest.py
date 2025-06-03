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
        self.diesel_energy_density = inputs["diesel_energy_density"]
        self.generator_length, self.generator_width, self.generator_height = 2.278, 0.9, 1.322 # - https://www.cat.com/en_MX/products/new/power-systems/electric-power/diesel-generator-sets/106402.html
        self.power_generator = 1000 # in W, assumed power output of the generator

        # Nest contraints
        self.number_of_trips = inputs["trips_for_mission"]
        self.required_energy = inputs["required_capacity_wh"]
        self.nest_energy = self.required_energy * self.number_of_trips
        self.nest_length = inputs["nest_length"]
        self.nest_width = inputs["nest_width"]
        self.nest_height = inputs["nest_height"]
        self.nest_mass = inputs["nest_empty_mass"]

        self.available_volume_per_nest = self.nest_length * self.nest_width * self.nest_height


    def uav_dimensions(self):

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
        
        required_energy = self.nest_energy # in Wh


        # Generator volume:
        #VF_generator = 0.1   # faction of nest volume for generator    ! === MOVE TO INPUTS
        #l_generator = 0.9   # width of generator in m                  ! === MOVE TO INPUTS

        #volume_generator = VF_generator * self.available_volume_per_nest


        self.volume_generator = self.generator_length * self.generator_width * self.generator_height

        fuel_tank_margin = 0.1
        self.fuel_tank_volume = self.generator_width * (self.nest_width * (1 - fuel_tank_margin)) * ((self.nest_height - self.generator_height) * (1 - fuel_tank_margin))

        l_op = self.nest_length - self.generator_width   # total length minus generator width
        self.l_op = l_op 

        # Calculate the amount of the mission we can power with one fuel tank fill
        diesel_energy_density_Wh_per_liter = 9167
        diesel_energy_density_Wh_per_m3 = diesel_energy_density_Wh_per_liter * 1000


        energy_in_fuel_tank = self.fuel_tank_volume * diesel_energy_density_Wh_per_m3
        available_energy = energy_in_fuel_tank * self.generator_efficiency

        percentage_energy_achieved = available_energy / required_energy

        if percentage_energy_achieved >= 1:
            self.refills_for_mission = 0
        else:
            self.refills_for_mission = np.ceil(1 / percentage_energy_achieved)

        if self.verbose:
            print(f"Volume of generator: {self.volume_generator:.2f} m^3")
            print(f"Volume of fuel tank: {self.fuel_tank_volume:.2f} m^3")
            print(f"Energy in fuel tank: {energy_in_fuel_tank/1000:.2f} kWh")
            print(f"Energy required for missions: {required_energy/1000:.2f} kWh")
            print(f"Refills needed for the mission: {self.refills_for_mission}")


    def misc_sizing(self):

        v_locker = 0.5*0.5
        VF_electronics = 0.05
        VF_equipment = 0.05
        MF_electronics = 0.05
        MF_equipment = 0.05

        self.v_electronics = VF_electronics * self.available_volume_per_nest 
        self.v_equipment = VF_equipment * self.available_volume_per_nest

        self.v_locker = v_locker


        area_human = self.nest_height * 0.6  # m^2
        v_operating_space = area_human * self.l_op
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
        self.generator_sizing()        
        self.misc_sizing()
        self.uavs_battery_sizing()

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
    inputs = {
        "wing_span": 3.0, 
        "wing_area": 1.8,
        "FW_height": 0.3,
        "FW_width": 2.25,

        "trips_for_mission": 10,
        "required_capacity_wh": 1000,  # in Wh
        "nest_empty_mass": 100.0,  #


        "uav_length": 2.5,
        "uav_width": 2.5,
        "uav_height": 0.5,
        "M_to": 30.0,
        "number_of_UAVs": 20,
        "generator_efficiency": 0.3,
        "diesel_energy_density": 9.94,
        "nest_energy": 4000*20,  # in Wh
        "nest_length": 5.9,
        "nest_width": 2.35,
        "nest_height": 2.39,
        "nest_mass": 100.0,
        "aerogel_width": 1.5,
        "aerogel_diameter": 0.2

    }
    nest = Nest(inputs, verbose=True)
    outputs = nest.get_all()
    for key, value in outputs.items():
        print(f"{key}: {value}")
    