import sys
import os
import numpy as np

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from scipy.optimize import minimize
from DetailedDesign.funny_inputs import funny_inputs
# from power import Power
from propulsion import Propulsion
from DetailedDesign.mission import Mission
from DetailedDesign.deployment import Deployment 


class Thermal:
    '''
    The thermal class contains the thermal subsystem sizing. 
    '''

    def __init__(self, inputs: dict[str, float], hardware=None) -> None:
        self.inputs = inputs
        self.hardware = hardware
        
        # Power required for each phase
        self.power_required_VTOL = inputs["power_required_VTOL"]
        self.power_required_cruise = inputs["power_required_cruise"]
        self.power_required_hover = inputs["power_required_hover"]
        self.power_deployment = inputs["power_deploy"]
        self.power_required_winch = inputs["power_required_winch"]

        # Duration of each phase
        self.time_ascent = inputs["time_ascent"] 
        self.time_descent = inputs["time_descent"]
        self.time_cruise_max = inputs["time_cruise_max"]
        self.time_cruise_min = inputs["time_cruise_min"]
        self.time_scan = inputs["time_scan"] # time during hover without having the winch activated
        self.time_deploy = inputs["time_deploy"] # time during hover with having the winch activated
        self.time_uav = inputs["time_uav"] # total time for one uav trip from ascend to return to nest

        # Battery parameters
        self.n_battery = inputs["n_battery"]
        self.battery_capacity = inputs["battery_capacity"] # Ah
        self.battery_potential = inputs["battery_potential"] # V
        self.battery_resistance = inputs["battery_resistance"] # Ohm

        # Other
        self.winch_eff = inputs["winch_eff"] # fraction (i.e. "0.65" means that 1 - 0.65 = 0.35 of the winch power required will be heat)
        self.processor_heat_diss = inputs["processor_heat_diss"] # given from the specifications

        

        # Shell specifications
        self.wing_eff_area = inputs["wing_eff_area"]
        self.fuselage_eff_area = inputs["fuselage_eff_area"]
        self.thickness_foam_wing = inputs["thickness_foam_wing"]
        self.thickness_alu_wing = inputs["thickness_alu_wing"]
        self.thickness_foam_fuselage = inputs["thickness_foam_fuselage"]
        self.thickness_alu_fuselage = inputs["thickness_alu_fuselage"]
        self.conductivity_foam = inputs["conductivity_foam"]
        self.conductivity_alu = inputs["conductivity_alu"]

        # Temperatures
        self.T_amb_onsite = inputs["T_amb_onsite"]
        self.T_amb_enroute = inputs["T_amb_enroute"]
        self.T_int = inputs["T_int"]

    # ~~~ Intermediate Functions ~~~

    def Q_env_leak(self, time: float, T_amb: float,) -> float:

        # Thermal resistance per unit effective surface area
        R_total_wing = (2 * self.thickness_alu_wing / self.conductivity_alu) + (self.thickness_foam_wing / self.conductivity_foam) # K/W
        R_total_fuselage = (2 * self.thickness_alu_fuselage / self.conductivity_alu) + (self.thickness_foam_fuselage / self.conductivity_foam) # K/W

        # Heat entering the wing due to outside temperature
        heat_env_leak_wing = (T_amb - self.T_int) * self.wing_eff_area * (1 / R_total_wing) # W
        Q_env_leak_wing = heat_env_leak_wing * time # J

        # Heat entering the fuselage due to outside temperature
        heat_env_leak_fuselage = (T_amb - self.T_int) * self.fuselage_eff_area * (1 / R_total_fuselage) # W
        Q_env_leak_fuselage = heat_env_leak_fuselage * time # J

        # Total heat entering the UAV due to outside temperature
        heat_env_leak = heat_env_leak_wing + heat_env_leak_fuselage
        Q_env_leak = Q_env_leak_wing + Q_env_leak_fuselage

        return heat_env_leak, Q_env_leak
    
    def simulate(self, x) -> float:
        
        pcm_mass, sink_area, insulation_thickness = x
        all_heat = self.create_heat_dissipated()
        
        # Times
        time_onsite = self.time_scan + self.time_descent + self.time_deploy + self.time_ascent
        time_approach = self.time_ascent + self.time_cruise_min
        time_return = self.time_cruise_min + self.time_descent

        # Heat entering due to outside temperature
        _, Q_env_onsite = self.Q_env_leak(time_onsite, self.T_amb_onsite) # J
        heat_env_approach, Q_env_approach = self.Q_env_leak(time_approach, self.T_amb_enroute) # W, J, same as return if time_ascent = time_descent
        heat_env_return, Q_env_return = self.Q_env_leak(time_return, self.T_amb_enroute) # W, J 

    def optimize(self):
        bounds = [(0.01, 3.0), (0.01, 0.5), (0., 0.05)]  # pcm_mass (kg), sink_area (m^2), insulation_thickness (m)
        x0 = [1.0, 0.1, 0.] # initial: pcm_mass (kg), sink_area (m^2), insulation_thickness (m)
        return minimize(self.simulate, x0=x0, bounds=bounds, method="SLSQP")

    
    def battery_heat_dissipated(self, power_required: float, time: float,) -> float:
        '''
        Return the heat dissipated during a specific phase by all batteries and the total heat energy from all batteries based on the power required and duration
        '''
        battery_current = power_required / (self.battery_potential * self.n_battery) # A, current per battery
        battery_heat = battery_current**2 * self.battery_resistance # W, heat dissipated per battery
        phase_battery_heat = battery_heat * self.n_battery # W, heat dissipated for all batteries combined
        phase_battery_Q = phase_battery_heat * time # J, heat energy generated by all batteries combined
        
        return phase_battery_heat, phase_battery_Q
    
    def winch_heat_dissipated(self) -> float:
        '''
        Return the heat dissipated and heat energy generated by the winch
        '''
        winch_heat = self.power_required_winch * (1 - self.winch_eff) # W
        winch_Q = winch_heat * self.time_deploy # J

        return winch_heat, winch_Q
    
    def processor_heat_dissipated(self, time: float,) -> float:
        '''
        Return the heat dissipated and heat energy generated by the processor
        '''
        return self.processor_heat_diss, (self.processor_heat_diss * time)
    
    def phase_heat_dissipated(self, power_required: float, time: float, phase: str,) -> float:
        '''
        Return the total heat dissipated and total heat energy generated per phase
        '''
        # Battery and processor heat and Q per phase
        phase_batt_heat, phase_batt_Q = self.battery_heat_dissipated(power_required, time)
        phase_processor_heat, phase_processor_Q = self.processor_heat_dissipated(time)

        # Add winch heat only in the deployment phase
        if phase == "deploy":
            winch_heat, winch_Q = self.winch_heat_dissipated()
            total_heat_dissipated += winch_heat
            total_Q += winch_Q

            return total_heat_dissipated, total_Q
        
        # Total heat and Q per phase
        phase_heat_dissipated, phase_Q = (phase_batt_heat + phase_processor_heat), (phase_batt_Q + phase_processor_Q)

        return phase_heat_dissipated, phase_Q
    
    def create_heat_dissipated(self):
        '''
        Create a dictionary containing all the significant heat contributions per phase from both within the fuselage as well as due to external conditions
        '''
        all_heat = {}

        all_heat['ascend'] = {}

        all_heat['ascend']['batt_heat'], all_heat['ascend']['batt_Q'] = self.battery_heat_dissipated(self.power_required_VTOL, self.time_ascent)
        all_heat['ascend']['processor_heat'], all_heat['ascend']['processor_Q'] = self.processor_heat_dissipated(self.time_ascent)
        all_heat['ascend']['phase_heat'], all_heat['ascend']['phase_Q'] = self.phase_heat_dissipated(self.power_required_VTOL, self.time_ascent)

        all_heat['descend'] = {}

        all_heat['descend']['batt_heat'], all_heat['descend']['batt_Q'] = self.battery_heat_dissipated(self.power_required_VTOL, self.time_descent)
        all_heat['descend']['processor_heat'], all_heat['descend']['processor_Q'] = self.processor_heat_dissipated(self.time_descent)
        all_heat['descend']['phase_heat'], all_heat['descend']['phase_Q'] = self.phase_heat_dissipated(self.power_required_VTOL, self.time_descent)

        all_heat['cruise_max'] = {}

        all_heat['cruise_max']['batt_heat'], all_heat['cruise_max']['batt_Q'] = self.battery_heat_dissipated(self.power_required_cruise, self.time_cruise_max)
        all_heat['cruise_max']['processor_heat'], all_heat['cruise_max']['processor_Q'] = self.processor_heat_dissipated(self.time_cruise_max)
        all_heat['cruise_max']['phase_heat'], all_heat['cruise_max']['phase_Q'] = self.phase_heat_dissipated(self.power_required_cruise, self.time_cruise_max)

        all_heat['cruise_min'] = {}

        all_heat['cruise_min']['batt_heat'], all_heat['cruise_min']['batt_Q'] = self.battery_heat_dissipated(self.power_required_cruise, self.time_cruise_min)
        all_heat['cruise_min']['processor_heat'], all_heat['cruise_min']['processor_Q'] = self.processor_heat_dissipated(self.time_cruise_min)
        all_heat['cruise_min']['phase_heat'], all_heat['cruise_min']['phase_Q'] = self.phase_heat_dissipated(self.power_required_cruise, self.time_cruise_min)

        all_heat['scan'] = {}

        all_heat['scan']['batt_heat'], all_heat['scan']['batt_Q'] = self.battery_heat_dissipated(self.power_required_hover, self.time_scan)
        all_heat['scan']['processor_heat'], all_heat['scan']['processor_Q'] = self.processor_heat_dissipated(self.time_scan)
        all_heat['scan']['phase_heat'], all_heat['scan']['phase_Q'] = self.phase_heat_dissipated(self.power_required_hover, self.time_scan)

        all_heat['deploy'] = {}

        all_heat['deploy']['batt_heat'], all_heat['deploy']['batt_Q'] = self.battery_heat_dissipated(self.power_required_hover, self.time_deploy)
        all_heat['deploy']['processor_heat'], all_heat['deploy']['processor_Q'] = self.processor_heat_dissipated(self.time_deploy)
        all_heat['deploy']['winch_heat'], all_heat['deploy']['winch_Q'] = self.winch_heat_dissipated()
        all_heat['deploy']['phase_heat'], all_heat['deploy']['phase_Q'] = self.phase_heat_dissipated(self.power_required_hover, self.time_deploy, phase='deploy')

        return all_heat
    
    def total_heat_storage(self):
        '''
        Compute the heat dissipated and heat energy generated during the hover + deployment phase in the "hot" zone.
        In the "hot" zone, it is not possible to dissipate heat using the heat sink, hence all this heat needs to be stored in the PCM.

        hover + deployment phase consists out of: scan > descend > deploy > ascend
        '''
        all_heat = self.create_heat_dissipated()
        
        total_heat_store = all_heat['scan']['phase_heat'] + all_heat['descend']['phase_heat'] + all_heat['deploy']['phase_heat'] + all_heat['ascend']['phase_heat']
        total_Q_store = all_heat['scan']['phase_Q'] + all_heat['descend']['phase_Q'] + all_heat['deploy']['phase_Q'] + all_heat['ascend']['phase_Q']

        return total_heat_store, total_Q_store
    
    def total_heat_approach_min(self):
        '''
        Compute the heat dissipated and heat energy generated during the shortest approach.
        All this heat has to be dissipated through the heat sink in this phase.
        
        Min. approach phase consists out of: ascend > cruise
        '''
        all_heat = self.create_heat_dissipated()
 
        total_heat_approach_min = all_heat['ascend']['phase_heat'] + all_heat['cruise_min']['phase_heat']
        total_Q_approach_min = all_heat['ascend']['phase_Q'] + all_heat['cruise_min']['phase_Q']

        return total_heat_approach_min, total_Q_approach_min
    
    def total_heat_return_min(self):
        '''
        Compute the heat dissipated and heat energy generated during the shortest return.
        All this heat + the excess from the "hot" has to be dissipated through the heat sink in this phase.
        
        Min. return phase consists out of: cruise > descend
        '''

        all_heat = self.create_heat_dissipated()
 
        total_heat_return_min = all_heat['cruise_min']['phase_heat'] + all_heat['descend']['phase_heat']
        total_Q_return_min = all_heat['cruise_min']['phase_Q'] + all_heat['descend']['phase_Q']

        return total_heat_return_min, total_Q_return_min




    # ~~~ Output functions ~~~ 

    # def get_all(self) -> dict[str, float]:
    #     '''
    #     Outputs:
        
    #     '''
    #     return outputs


if __name__ == '__main__':

    prop = Propulsion(funny_inputs)
    funny_inputs = prop.get_all()

    # power = Power(funny_inputs)
    # funny_inputs = power.get_all()

    mission = Mission(funny_inputs)
    funny_inputs = mission.get_all()

    deployment = Deployment(funny_inputs, strategy='perimeter', amt=funny_inputs['mission_perimeter'])
    funny_inputs = deployment.get_all()

    thermal = Thermal(funny_inputs)
    # outputs = thermal.get_all() 

    ther = Thermal(funny_inputs)

    # print('Dict/ total:', ther.create_heat_dissipated()['deploy'])
    # print('\n Winch', ther.winch_heat_dissipated())
    print(ther.total_heat_storage())