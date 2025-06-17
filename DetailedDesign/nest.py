import numpy as np

'''
This is the file for the nest. It contains a single class.
'''

class Nest:

    def __init__(self, inputs: dict[str, float], components, verbose: bool = False) -> None:

        self.verbose = verbose
        self.inputs = inputs
        self.outputs = {} #self.inputs.copy()
        self.hardware = components

        
        # Mission parameters
        self.n_drones = inputs["number_of_UAVs"]
        self.number_of_trips = inputs["trips_for_mission"]

        self.mission_energy = inputs["required_capacity_wh"]
        self.nest_energy = self.mission_energy * self.number_of_trips  # minimum power the nest must be able to provide


        # UAV Dimensions 
        self.FW_span = inputs["wing_span"]
        self.uav_wing_area = inputs["wing_area"]
        self.FW_chord = inputs["mac"] #self.uav_wing_area / self.uav_span if self.uav_span != 0 else 0 
        self.FW_thickness = inputs["thickness_to_chord_ratio"] * inputs["mac"]

        self.uav_folded_length = 2.156 # 2155.529mm
        self.uav_folded_width = 1.724 # 1724mm
        #self.uav_folded_height = 0.893 # 892.943mm
        self.uav_folded_height = 0.491 # 490.307mm - staggering

        self.uav_mass = inputs["M_to"]

       

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


        self.generator_efficiency = components["generator"]["generator_efficiency"]
        self.generator_length = components["generator"]["generator_length"]
        self.generator_width = components["generator"]["generator_width"]
        self.generator_height = components["generator"]["generator_height"]
        self.generator_power_output = components["generator"]["generator_power_output"]
        self.generator_power_factor = components["generator"]["generator_power_factor"]
        self.generator_mass = components["generator"]["generator_mass"]
        self.generator_fuel_tank_volume = components["generator"]["generator_fuel_tank"]

        self.generator_x = components["generator"]["generator_x"]
        self.generator_y = components["generator"]["generator_y"]
        self.generator_z = components["generator"]["generator_z"]

        self.nest_length = components["container"]["container_length"]
        self.nest_width = components["container"]["container_width"]
        self.nest_height = components["container"]["container_height"]
        self.container_mass = components["container"]["container_tare_mass"]
        self.max_payload_mass = components["container"]["container_max_payload"]  # Maximum payload mass the container can carry


        self.available_volume_per_container = self.nest_length * self.nest_width * self.nest_height

        self.nest_components = ["container", "heating_system", "ventilation_system", "thermal_sensor",
                           "generator", "PDU", "UPS", "battery_charger",
                           "RF_antenna", "4G_antenna", "Satellite_antenna",
                           "mesh_base", "router", "Sattelite_modem",
                           "switch", "firewall", "computer"]


    # def uav_dimensions(self):
    #     pass
        

    def generator_sizing(self):  # AKA: energy sizing

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

        self.nest_trips_capacity = self.total_available_energy // self.mission_energy
        self.nest_cycle_capacity = self.nest_trips_capacity // self.n_drones

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



    # def misc_sizing(self):


    #     # Assigning fractions for electronics and equipment
    #     v_locker = 0.5*0.5
    #     VF_electronics = 0.05
    #     VF_equipment = 0.05
    #     MF_electronics = 0.05
    #     MF_equipment = 0.05


    #     self.area_human = self.nest_height * 0.6  # m^2
    #     self.v_electronics = VF_electronics * self.available_volume_per_container 
    #     self.v_equipment = VF_equipment * self.available_volume_per_container
    #     self.v_locker = v_locker

    def power_sizing(self):
        
        power_generator = self.generator_power_output * self.generator_power_factor  # in W
        
        total_power = 0

        for component in self.nest_components:
            if component in self.hardware:
            # Special case for battery_charger: multiply by number of UAVs
                if component == "battery_charger":
                    for key, value in self.hardware[component].items():
                        if key.endswith("_power"):
                            total_power += value * self.n_drones
                else:
                    for key, value in self.hardware[component].items():
                        if key.endswith("_power"):
                            total_power += value

        self.total_power = total_power  # in W, total power required by the nest components

        # Check if the generastor can provide enough power
        if power_generator < total_power:
            raise ValueError(f"Generator power output ({power_generator:.2f} W) is less than total power required by nest components ({total_power:.2f} W). Increase generator capacity or reduce power requirements.")

        if self.verbose:
            print(f"Generator power output: {power_generator:.2f} W")
            print(f"Total power required by nest components: {total_power:.2f} W")


    def volume_sizing(self):

        """
        
        Parameters that must be defined:
        - VF_generator: fraction of nest volume for generator
        - VF_UAV_battery: fraction of UAV volume for battery
        - VF_UAV_margin: fraction of UAV volume for margin (between drones)



        """
        self.generator_sizing()        

        print("\n\n\n~~~ Volume Sizing ~~~\n\n")
        # Remaining length with generator addition:
        l_remaining = self.nest_length - self.generator_length  # in m, remaining length after adding the generator

        margin = 0.1

        n_uavs_gennest = l_remaining // (self.uav_folded_height * (1 + margin) )
        n_uavs_nogennest = self.nest_length // (self.uav_folded_height * (1 + margin) )
        self.n_uavs_gennest = int(n_uavs_gennest)  
        self.n_uavs_nogennest = int(n_uavs_nogennest)

        print(f"nest length: {self.nest_length:.2f} m")
        print(f'uav folded height: {self.uav_folded_height:.2f} m')

        if n_uavs_gennest < self.n_drones: # if generator nest cannot accommodate all UAVs
            n_uavs_remaining = self.n_drones - n_uavs_gennest
            n_extra_nests = np.ceil(n_uavs_remaining / n_uavs_nogennest)  # number of extra nests required to accommodate the remaining UAVs
            self.n_total_uavs = n_extra_nests * n_uavs_nogennest + n_uavs_gennest  # total number of UAVs that can be accommodated in the nests
            self.n_containers = n_extra_nests + 1  # total number of containers required (1 for the generator nest and the rest for the extra nests)
        else:
            n_extra_nests = 0
            self.n_total_uavs = n_uavs_gennest # total number of UAVs that can be stored in the generator nest
            self.n_containers = 1

        if self.verbose:
            print(f"Number of uavs in generator nest: {n_uavs_gennest}")
            print(f"Number of uavs in extra nests: {n_uavs_nogennest}")




    def mass_sizing(self):

        total_mass = 0

        nest_components = ["container", "heating_system", "ventilation_system", "thermal_sensor",
                           "generator", "PDU", "UPS", "battery_charger",
                           "RF_antenna", "4G_antenna", "Satellite_antenna",
                           "mesh_base", "router", "Sattelite_modem",
                           "switch", "firewall", "computer"]


        for component in nest_components:
            if component in self.hardware:
            # Special case for battery_charger: multiply by number of UAVs
                if component == "battery_charger":
                    for key, value in self.hardware[component].items():
                        if key.endswith("_mass"):
                            total_mass += value * self.n_drones
                else:
                    for key, value in self.hardware[component].items():
                        if key.endswith("_mass"):
                            total_mass += value

        self.total_mass = total_mass

        # check if the total mass exceeds the maximum payload mass of the container
        if self.total_mass > self.max_payload_mass:
            raise ValueError(f"Total mass of nest components ({self.total_mass:.2f} kg) exceeds maximum payload mass of the container ({self.max_payload_mass:.2f} kg). Reduce the number of components or increase the container's payload capacity.")

        if self.verbose:
            print(f"Total mass of nest components: {self.total_mass:.2f} kg")



    def deployment_time():
        pass


    # ~~~ Output functions ~~~ 

    def get_all(self) -> dict[str, float]:

        
        
        self.power_sizing()
        self.volume_sizing()
        self.mass_sizing()

        #self.outputs["number_of_nests"] = self.n_nests
        #self.outputs["number_of_UAVs"] = self.n_drones

        #self.outputs["nests_volume"] = self.nests_volume
        #self.outputs["volume_fueltank"] = self.total_fuel_tank_volume
        #self.outputs["refills_for_mission"] = self.refills_for_mission
        
        #self.outputs["Nest_mass"] = ...

        self.outputs["number_of_containers"] = self.n_containers
        self.outputs["capacity_gen"] = self.n_uavs_gennest
        self.outputs["capacity_nogen"] = self.n_uavs_nogennest
        #self.outputs["number_of_UAVs"] = self.n_total_uavs

        self.outputs["nest_trips_capacity"] = self.nest_trips_capacity
        self.outputs["nest_cycles_capacity"] = self.nest_cycle_capacity
        self.outputs["fuel_refills_for_mission"] = self.refills_for_mission


        self.outputs["total_nest_power_required"] = self.total_power
        self.outputs["total_nest_mass"] = self.total_mass

        return self.outputs
    
if __name__ == '__main__':
    # Example usage

    from inputs import initial_inputs
    from hardware_inputs import components
    from hardware import Hardware

    initial_inputs["number_of_UAVs"] = 20  # Example number of UAVs
    initial_inputs["trips_for_mission"] = 3  # Example number of trips for the mission
    initial_inputs["required_capacity_wh"] = 761.0912836715547  # Example required capacity in Wh

    hardware = Hardware(initial_inputs, components)
    hardware_outputs = hardware.get_all()

    nest = Nest(hardware_outputs, components, verbose=True)
    outputs = nest.get_all()
    print("\n\nFinal outputs after nest sizing:")
    print("========================================")
    for key, value in outputs.items():
        print(f"{key}: {value}")
    