import numpy as np

'''
This is the file for the nest. It contains a single class.
'''

class Nest:

    def __init__(self, inputs: dict[str, float], nest_components, verbose: bool = False) -> None:

        self.verbose = verbose
        self.inputs = inputs
        self.outputs = self.inputs.copy()
        self.hardware = nest_components
        
        # Mission parameters
        self.n_drones = 28 # inputs["number_of_UAVs"]
        self.number_of_trips = inputs["trips_for_mission"]

        self.mission_energy = inputs["required_capacity_wh"]
        self.nest_energy = self.mission_energy * self.number_of_trips  # minimum power the nest must be able to provide


        # UAV Dimensions 
        self.FW_span = inputs["wing_span"]
        self.uav_wing_area = inputs["wing_area"]
        self.FW_chord = inputs["mac"] #self.uav_wing_area / self.uav_span if self.uav_span != 0 else 0 
        self.FW_thickness = inputs["thickness_to_chord_ratio"] * inputs["mac"]

        self.FUS_length = 2
        self.FUS_width = 1.724
        self.FUS_height = 1.5

        self.uav_height = 1.5
        self.uav_length = 3
        self.uav_width = 2 


        self.uav_mass = inputs["M_to"]

        # Aerogel dimensions
        self.aerogel_width = inputs["aerogel_width"]  # width of the aerogel
        self.aerogel_diameter = inputs["aerogel_diameter"]  # diameter of the aerogel


        # Generator parameters
        #self.generator_efficiency = inputs["generator_efficiency"] 
        self.diesel_energy_density = inputs["biodiesel_energy_density"] # in Wh/kg
        self.diesel_density = inputs["biodiesel_density"] # in kg/liter
        #self.generator_length = inputs["generator_length"] # 
        #self.generator_width = inputs["generator_width"]
        #self.generator_height = inputs["generator_height"]
        #self.power_generator = inputs["generator_power"] * inputs["generator_power_factor"] # in W, assumed power output of the generator
        #self.mass_generator = inputs["generator_mass"]
        #self.internal_fuel_tank_volume = inputs["generator_internal_fuel_tank"]


        self.generator_efficiency = nest_components["generator"]["generator_efficiency"]
        self.generator_length = nest_components["generator"]["generator_length"]
        self.generator_width = nest_components["generator"]["generator_width"]
        self.generator_height = nest_components["generator"]["generator_height"]
        self.generator_power_output = nest_components["generator"]["generator_power_output"]
        self.generator_power_factor = nest_components["generator"]["generator_power_factor"]
        self.generator_mass = nest_components["generator"]["generator_mass"]
        self.generator_fuel_tank_volume = nest_components["generator"]["generator_fuel_tank"]

        self.generator_x = nest_components["generator"]["generator_x"]
        self.generator_y = nest_components["generator"]["generator_y"]
        self.generator_z = nest_components["generator"]["generator_z"]

        # Misc parameters


        # Container
        #self.nest_length = inputs["nest_length"]
        #self.nest_width = inputs["nest_width"]
        #self.nest_height = inputs["nest_height"]
        #self.nest_mass = inputs["nest_empty_mass"]

        self.nest_length = nest_components["container"]["container_length"]
        self.nest_width = nest_components["container"]["container_width"]
        self.nest_height = nest_components["container"]["container_height"]
        self.container_mass = nest_components["container"]["container_tare_mass"]


        self.available_volume_per_container = self.nest_length * self.nest_width * self.nest_height

        components = ["container", 
                      "generator", 
                      "heating_system", 
                      "computer", 
                      "RF_antenna", 
                      "4G_antenna", 
                      "Satellite_antenna", 
                      "ventilation_system", 
                      "lighting_system"]


    def uav_dimensions(self):

        """
        
        """
        #method = "wing-split"  
        method = "rectangular_prism" 

        if method == "wing-split":
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


        if method == "rectangular_prism":
            self.uav_volume = self.uav_length * self.uav_width * self.uav_height  # m^3, assuming a rectangular prism for the UAV dimensions


    def generator_sizing(self):
        
        """
        
        Choose:
        - Generator length, width, height (chosen to be an ISO container)
        - Generator efficiency
        - 
        """

        # Generator volume:
        self.generator_volume = self.generator_length * self.generator_width * self.generator_height    # calculating the volume of the generator in m^3


        include_external_fuel_tank = False  # whether to include an external fuel tank or not
        # Fuel tank: 
        if include_external_fuel_tank:
            fuel_tank_margin = 0.1 # margin added for the fuel tank volume, to account for the space taken by the fuel tank structure and fittings
            self.external_fuel_tank_volume = self.generator_width * (self.nest_width * (1 - fuel_tank_margin)) * ((self.nest_height - self.generator_height) * (1 - fuel_tank_margin))
        else:
            self.external_fuel_tank_volume = 0 # Excluding the external fuel tank for now, as it is not needed for the mission

        diesel_volumetric_energy_density = self.diesel_energy_density * self.diesel_density  # in Wh/m^3, converting from Wh/kg to Wh/m^3 
        
        self.total_fuel_tank_volume = self.generator_fuel_tank_volume + self.external_fuel_tank_volume
        self.total_fuel_capacity = (self.total_fuel_tank_volume) * diesel_volumetric_energy_density  # in Wh, total energy capacity of the fuel tank
        self.total_available_energy = self.total_fuel_capacity * self.generator_efficiency

        percentage_energy_achieved = self.total_available_energy / self.mission_energy

        if percentage_energy_achieved >= 1:
            self.refills_for_mission = 0
        else:
            self.refills_for_mission = np.ceil(1 / percentage_energy_achieved)

        self.nest_trips_capacity = self.total_available_energy / self.mission_energy


        if self.verbose:
            print(f"Generator volume: {self.generator_volume:.2f} m^3")
            print(f"Internal fuel tank volume: {self.generator_fuel_tank_volume:.2f} m^3")
            print(f"External fuel tank volume: {self.external_fuel_tank_volume:.2f} m^3")
            print(f"Total fuel tank volume: {self.total_fuel_tank_volume:.2f} m^3")
            print(f"Total fuel capacity (Wh): {self.total_fuel_capacity:.2f} Wh")
            print(f"Total available energy (after efficiency): {self.total_available_energy:.2f} Wh")
            print(f"Mission energy requirement: {self.mission_energy:.2f} Wh")
            print(f"Percentage of mission energy achieved: {percentage_energy_achieved*100:.2f}%")
            print(f"Refills required for mission: {self.refills_for_mission}")
            print(f"Nest trips capacity: {self.nest_trips_capacity:.2f}")
            #print(f"Remaining length after generator: {self.l_minus_gen:.2f} m")



    def misc_sizing(self):


        # Assigning fractions for electronics and equipment
        v_locker = 0.5*0.5
        VF_electronics = 0.05
        VF_equipment = 0.05
        MF_electronics = 0.05
        MF_equipment = 0.05


        self.area_human = self.nest_height * 0.6  # m^2
        self.v_electronics = VF_electronics * self.available_volume_per_container 
        self.v_equipment = VF_equipment * self.available_volume_per_container
        self.v_locker = v_locker

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
        
        # Remaining length with generator addition:

        layout = "gen_lengthwise"  # "gen_lengthwise" or "gen_crosswise"

        if layout == "gen_lengthwise_rails":
            volume_uavs = self.v_uav_bat * self.n_drones

            volume_service = self.generator_length * self.generator_width * self.nest_height
            
            service_components = [self.generator_volume,
                                  self.heating_system_volume,
                                  self.computer_volume,
                                  self.RF_antenna_volume,
                                  self.FourG_antenna_volume,
                                  self.satellite_antenna_volume,
                                  self.ventilation_system_volume]
            
            volume_service_left = volume_service - sum(service_components)

            if volume_service_left < 0:
                raise ValueError("Not enough space for service components in the generator layout.")

            volume_operating = self.available_volume_per_container - volume_service
            uav_fits = volume_operating // self.v_uav_bat

            if uav_fits < self.n_drones:
                print("Not enough space for all UAVs in the generator layout. Consider increasing the nest size or reducing the number of UAVs.")

            else:
                print("All UAVs fit in the generator layout.")




            volume_left = self.available_volume_per_container
        
        area_human = 0.6 * self.nest_height
        
        #v_operating_space = area_human * self.l_minus_gen
        #self.v_operating_space_gen = v_operating_space
        self.v_operating_space_nogen = area_human * self.nest_length

        components = ["container", 
                      "generator", 
                      "heating_system", 
                      "computer", 
                      "RF_antenna", 
                      "4G_antenna", 
                      "Satellite_antenna", 
                      "ventilation_system", 
                      "lighting_system"]

        # #v_op_gen = available_volume_per_nest - self.generator_volume - self.v_locker - self.v_operating_space_gen
        # v_op_nogen = available_volume_per_nest - self.v_locker - self.v_operating_space_nogen
        



        # # if self.verbose:
        # #     print(f"v_op_gen: {v_op_gen:.2f} m^3")
        # #     print(f"v_op_nogen: {v_op_nogen:.2f} m^3")


        # v_tot_uav_bat = self.v_uav_bat * self.n_drones

        # if v_op_gen > v_tot_uav_bat:
        #     n_containers = 1
        #     n_cap_nest_gen = int(v_op_gen // self.v_uav_bat)
        #     empty_slots = n_cap_nest_gen - self.n_drones

        # else:
        #     n_cap_nest_gen = int(v_op_gen // self.v_uav_bat)  # Number of whole drones (with battery) that fit in v_op
        #     n_remaining = int(self.n_drones - n_cap_nest_gen)

        #     # print(f"number of remaining drones: {n_remaining}")

        #     # n_cap_nest_nogen = int(v_op_nogen // self.v_uav_bat)  # Number of drones in overflow container
        #     # n_nest_nogen = n_remaining // n_cap_nest_nogen  # Number of overflow containers needed

        #     # empty_slots = (n_cap_nest_nogen * n_nest_nogen) - n_remaining

        #     # if self.verbose
        #     #     print(f"Number of drones that fit in generator nest: {n_cap_nest_gen}")
        #     #     print(f"Number of drones remaining: {n_remaining}")
        #     #     print(f"Number of drones that fit in non-generator nest: {n_cap_nest_nogen}")
        #     #     print(f"Number of overflow nests needed: {n_nest_nogen}")
        #     #     print(f"Empty slots in last overflow nest: {empty_slots}")

        #     # n_containers = 1 + n_nest_nogen
        #     n_cap_nest_nogen = int(v_op_nogen // self.v_uav_bat)  # Number of drones in overflow container
        #     n_nest_nogen = int(np.ceil(n_remaining / n_cap_nest_nogen))  # Number of overflow containers needed

        #     # Number of drones in the last overflow nest
        #     drones_in_last_nest = n_remaining % n_cap_nest_nogen
        #     if drones_in_last_nest == 0:
        #         empty_slots = 0
        #     else:
        #         empty_slots = n_cap_nest_nogen - drones_in_last_nest

        #     if self.verbose:
        #         print(f"Number of drones that fit in generator nest: {n_cap_nest_gen}")
        #         print(f"Number of drones remaining: {n_remaining}")
        #         print(f"Number of drones that fit in non-generator nest: {n_cap_nest_nogen}")
        #         print(f"Number of overflow nests needed: {n_nest_nogen}")
        #         print(f"Empty slots in last overflow nest: {empty_slots}")

        #     n_containers = 1 + n_nest_nogen


        # self.n_nests = n_containers
        # self.n_extra = empty_slots
        # self.n_drones = self.n_drones + empty_slots

        # self.nests_volume = self.n_nests * available_volume_per_nest

        # if self.verbose:
        #     print(f"Number of nests needed: {self.n_nests}")
        #     print(f"Number of extra slots in the last nest: {self.n_extra}")
        #     print(f"Volume available per nest: {available_volume_per_nest:.2f} m^3")
        #     print(f"Volume of generator: {self.generator_volume:.2f} m^3")
        #     print(f"Volume of electronics and equipment (locker): {self.v_locker:.2f} m^3")
        #     print(f"Volume of operating space with generator: {self.v_operating_space_gen:.2f} m^3")
        #     print(f"Volume of operating space without generator: {self.v_operating_space_nogen:.2f} m^3")
        #     print(f"Volume of UAVs and batteries: {v_tot_uav_bat:.2f} m^3")


    def mass_sizing(self):

        pass

        # Calculate the mass of the nest
        masses = [
            self.container_mass,
        ]


    def power_sizing(self):
        pass
        
        power_generator = self.generator_power_output * self.generator_power_factor  # in W
        
        # Sum the power requirements of all main hardware components explicitly
        total_power = 0
        total_power += self.hardware["battery_charger"]["battery_charger_power"] * self.n_drones  # Power for charging all UAV batteries
        total_power += self.hardware["heating_system"]["heating_system_power"]
        total_power += self.hardware["computer"]["computer_power"]
        total_power += self.hardware["RF_antenna"]["RF_antenna_power"]
        total_power += self.hardware["4G_antenna"]["4G_antenna_power"]
        total_power += self.hardware["Satellite_antenna"]["Satellite_antenna_power"]
        total_power += self.hardware["ventilation_system"]["ventilation_system_power"]
        total_power += self.hardware["lighting_system"]["lighting_system_power"]

        self.outputs["total_power_required"] = total_power


        if self.verbose:
            print(f"Generator power output: {power_generator:.2f} W")
            print(f"Total power required by nest components: {total_power:.2f} W")



    def deployment_time():
        pass


    # ~~~ Output functions ~~~ 

    def get_all(self) -> dict[str, float]:

        self.volume_sizing()
        self.mass_sizing()
        self.power_sizing()

        #self.outputs["number_of_nests"] = self.n_nests
        #self.outputs["number_of_UAVs"] = self.n_drones

        #self.outputs["nests_volume"] = self.nests_volume
        #self.outputs["volume_fueltank"] = self.total_fuel_tank_volume
        #self.outputs["refills_for_mission"] = self.refills_for_mission
        
        #self.outputs["Nest_mass"] = ...

        return self.outputs
    
if __name__ == '__main__':
    # Example usage

    from inputs import initial_inputs
    from hardware_inputs import components
    from hardware import Hardware

    hardware = Hardware(initial_inputs, components)
    hardware_outputs = hardware.get_all()

    nest = Nest(initial_inputs, hardware_outputs, verbose=True)
    outputs = nest.get_all()
    for key, value in outputs.items():
        print(f"{key}: {value}")
    