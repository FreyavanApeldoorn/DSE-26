"""
This is the file for the Structures subsystem. It contains a single class.
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy import integrate

import sys
from pathlib import Path
from typing import Any


PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.append(str(PROJECT_ROOT))

from DetailedDesign.funny_inputs import funny_inputs as fi


import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

import numpy as np

class Structures:

    def __init__(self, inputs: dict[str, float], hardware: dict[str, float] = None, verbose=False) -> None:
        self.inputs = inputs
        self.outputs = self.inputs.copy()
        self.hardware = hardware
        self.verbose = False

        self.wing_span = inputs["wing_span"]
        self.mtow = self.inputs['MTOW']
        self.span = self.inputs['wing_span']
        self.rho = self.inputs['rho_0']
        # self.V_max = self.inputs['V_cruise']

        # self.mass_margin = inputs["mass_margin"]

        self.mass_payload = inputs["payload_mass"]
        # self.mass_hardware = inputs["mass_hardware"]
        self.mass_battery = inputs["mass_battery"]
        self.battery_length = inputs['battery_length']
        self.mass_propulsion = inputs["mass_propulsion"]
        self.taper_ratio = inputs['taper_ratio']
        
        self.wing_span = inputs["wing_span"]
        self.mass_wing = 3

        self.motor_mass_VTOL = inputs['motor_mass_VTOL']
        self.propeller_mass_VTOL = inputs['propeller_mass_VTOL']
        self.propeller_diameter_VTOL = inputs['propeller_diameter_VTOL']

        self.VTOL_boom_length = inputs['VTOL_boom_length']
        self.titanium_density = inputs['titanium_density']
        self.titanium_E = inputs['titanium_E']
        self.max_deflection_VTOL_boom = inputs['max_deflection_VTOL_boom']
        self.load_factor = inputs['max_load_factor']

        self.fuselage_diameter = inputs['fuselage_diameter']
        self.y_prop = max(self.propeller_diameter_VTOL / 2 - self.fuselage_diameter / 2, self.battery_length*2)
        self.wind_speed = inputs['wind_speed']
        self.rho_0 = inputs['rho_0']
        self.wing_area = inputs['wing_area']

        self.conductivity_alu = inputs['conductivity_alu']
        self.conductivity_foam = inputs['conductivity_foam']
        self.shear_strength_foam = inputs['shear_strength_foam']
        self.shear_strength_alu = inputs['shear_strength_alu']
        self.tensile_strength_foam = inputs['tensile_strength_foam']
        self.tensile_strength_alu = inputs['tensile_strength_alu']
        self.E_foam = inputs['E_foam']
        self.E_alu = inputs['E_alu']
        self.density_alu = inputs['density_alu']
        self.boom_inner_diameter = inputs['boom_inner_diameter']


        self.VTOL_boom_thickness = self.determine_VTOL_boom_thickness()
        self.VTOL_boom_mass = (np.pi*(self.boom_inner_diameter + self.VTOL_boom_thickness)**2 - np.pi*self.boom_inner_diameter**2)*self.VTOL_boom_length*self.density_alu


                

    # ~~~ Intermediate Functions ~~~


    def calc_wing_mass(self) -> float:
        pass

    def calc_structure_mass(self) -> float:
        
        MF_structure = 0.3  # THIS NEEDS TO BE UPDATED
        self.mass_structure = self.M_to * MF_structure

    def mass_fractions(self):
        pass

        """
        Components:

        - Sensors
        - Propulsion
        - Battery
        - Structure + fuselage
        - Wing_group (including tail)
        - 
        - Payload (aerogel)
        """


        mass_sensors = 10

        self.MF_sensors = 5/self.M_to # NEEDS TO BE UPDATED
        self.MF_propulsion = self.mass_propulsion / self.M_to
        self.MF_winggroup = 2/self.M_to # NEEDS TO BE UPDATED
        self.MF_battery = self.mass_battery / self.M_to
        self.MF_structure = 4/self.M_to # NEEDS TO BE UPDATED
        self.MF_payload = self.mass_payload / self.M_to

        MF_non_payload = np.array([self.mass_margin, self.MF_sensors, self.MF_propulsion, self.MF_battery, self.MF_winggroup, self.MF_structure])
        self.MF_payload = 1 - np.sum(MF_non_payload)

        if self.verbose:
            print(f"Sensor mass fraction: {self.MF_sensors:.4f}")
            print(f"Propulsion mass fraction: {self.MF_propulsion:.4f}")
            print(f"Battery mass fraction: {self.MF_battery:.4f}")
            print(f"Wing group mass fraction: {self.MF_winggroup:.4f}")
            print(f"Structure mass fraction: {self.MF_structure:.4f}")
            print(f"Payload mass fraction: {self.MF_payload:.4f}")


        if self.MF_payload < 0:
            raise ValueError("The mass fraction for the payload is negative. Please check the mass fractions of the other components.")

        # Update payload mass
        self.mass_payload = self.M_to * self.MF_payload
        



    def NVM_cruise(self, return_root_values=False, return_max_values=False) -> None:
        """
        This function calculates the NVM (Normal, Shear, and Bending Moment) for the UAV wing during cruise flight.
        It considers the distributed loads from the wing weight, battery weight and lift, and the point loads from the propellers.
        It then plots the distributed load, shear force, and bending moment along the span of the wing.

        load factor is from the gust loads

        Down is considered positive in this context, as per the provided reference and convention for aircraft coordinate systems.

        The load factor is 1
        """

        # https://uotechnology.edu.iq/dep-MechanicsandEquipment/Lectures%20and%20Syllabus/Lectures/Aircraft/Foruth%20Grade/Aircraft%20Design3.pdf

        # DOWN IS POSITIVE

        half_span = self.span / 2.0
        y = np.linspace(0, half_span, 500)  # 0 (root) to b/2 (tip)

        # Distributed load from the battery

        W_batt = np.array([2*self.mass_battery*9.81 / (2*self.battery_length) if i < self.battery_length*2 else 0 for i in y])

        # Distributed load from the wing weight

        x_0 = self.mass_wing*9.81 / (half_span*(self.taper_ratio + 0.5*(1-self.taper_ratio)))
        W_wing = [-(((1-self.taper_ratio)*x_0 / half_span)* i - x_0) for i in y]

        # Point load from the propellers

        F_prop = 9.81*(2*(self.propeller_mass_VTOL + self.motor_mass_VTOL) + self.VTOL_boom_mass)

        V_prop = [F_prop if i < self.y_prop else 0 for i in y]

        # Distributed lift load from the lift assuming elliptical lift distribution
        L_y = -self.load_factor*((4*self.mtow) / (np.pi*self.span)) * np.sqrt(1 - ((2*y)/self.span)**2)
        total_forces = W_batt +L_y + W_wing
        forces_rev = total_forces[::-1]

        V_rev = integrate.cumulative_simpson(forces_rev, x=y)  + V_prop[::-1][:-1]
        M_rev = integrate.cumulative_simpson(V_rev, x=y[:-1])

        V = V_rev[::-1]
        M = -M_rev[::-1]
                
        fig, axs = plt.subplots(3, 1, figsize=(10, 10), sharex=True)

        if return_root_values:
            return total_forces[0], V[0], M[0]
        elif return_max_values:
            return max(total_forces), max(V), max(M)

        axs[0].plot(y, total_forces, color='tab:blue', linewidth=2, label="Distributed Load")
        axs[0].fill_between(y, total_forces, color='tab:blue', alpha=0.3)
        axs[0].set_ylabel("Load [N]")
        axs[0].set_xlabel("Spanwise Position $y$ (m)")
        axs[0].grid(True)

        axs[1].plot(y[:-1], V, color='tab:orange', linewidth=2, label="Shear Force")
        axs[1].fill_between(y[:-1], V, color='tab:orange', alpha=0.3)
        axs[1].set_ylabel("Shear [N]")
        axs[1].set_xlabel("Spanwise Position $y$ (m)")
        axs[1].grid(True)

        axs[2].plot(y[:-2], M, color='tab:green', linewidth=2, label="Bending Moment")
        axs[2].fill_between(y[:-2], M, color='tab:green', alpha=0.3)
        axs[2].set_ylabel("Moment [N·m]")
        axs[2].set_xlabel("Spanwise Position $y$ (m)")
        axs[2].grid(True)

        plt.tight_layout(rect=[0, 0, 1, 0.97])
        plt.savefig("DetailedDesign/subsystems/Plots/NVM_plot_cruise.png", dpi=300)
        plt.show()

        if return_root_values:
            return total_forces[0], V[0], M[0]
    
    def NVM_VTOL(self, return_root_values=False, return_max_values=False) -> None:
        """
        This function calculates the NVM (Normal, Shear, and Bending Moment) for the UAV during cruise hover.
        It considers the distributed loads from the wing weight, battery weight gust loads and lift, which is now generated by the propellers.
        It then plots the distributed load, shear force, and bending moment along the span of the wing.

        Down is considered positive in this context, as per the provided reference and convention for aircraft coordinate systems.

        Gust loads are considered for a 30 km/h wind from straight below.
        """

        # https://uotechnology.edu.iq/dep-MechanicsandEquipment/Lectures%20and%20Syllabus/Lectures/Aircraft/Foruth%20Grade/Aircraft%20Design3.pdf

        # DOWN IS POSITIVE

        half_span = self.span / 2.0
        y = np.linspace(0, half_span, 500)  # 0 (root) to b/2 (tip)

        W_batt = np.array([2*self.mass_battery*9.81 / (2*self.battery_length) if i < self.battery_length*2 else 0 for i in y])

        # Distributed load from the wing weight

        x_0 = self.mass_wing*9.81 / (half_span*(self.taper_ratio + 0.5*(1-self.taper_ratio)))
        W_wing = np.array([-(((1-self.taper_ratio)*x_0 / half_span)* i - x_0) for i in y])

        F_gust = -0.5*self.rho_0* self.wind_speed**2 * (self.wing_area / 2)
        W_gust = np.array([F_gust / self.span for _ in y])

        # Point load from the propellers

        F_prop = 9.81*(2*(self.propeller_mass_VTOL + self.motor_mass_VTOL) + self.VTOL_boom_mass) - 0.5*self.mtow


        V_prop = [F_prop if i < self.y_prop else 0 for i in y]

        total_forces = W_wing + W_batt + W_gust
        forces_rev = total_forces[::-1]

        # V = integrate.cumulative_simpson(total_forces, x=y)
        # M = integrate.cumulative_simpson(V, x=y[:-1])

        V_rev = integrate.cumulative_simpson(forces_rev, x=y)  + V_prop[::-1][:-1]
        # V_rev = V_prop[::-1][:-1]
        M_rev = integrate.cumulative_simpson(V_rev, x=y[:-1])

        V = V_rev[::-1]
        M = -M_rev[::-1]
                
        fig, axs = plt.subplots(3, 1, figsize=(10, 10), sharex=True)

        if return_root_values:
            return total_forces[0], V[0], M[0]
        elif return_max_values:
            return max(total_forces), max(V), max(M)

        axs[0].plot(y, total_forces, color='tab:blue', linewidth=2, label="Distributed Load")
        axs[0].fill_between(y, total_forces, color='tab:blue', alpha=0.3)
        axs[0].set_ylabel("Load [N]")
        axs[0].set_xlabel("Spanwise Position $y$ (m)")
        axs[0].grid(True)

        axs[1].plot(y[:-1], V, color='tab:orange', linewidth=2, label="Shear Force")
        axs[1].fill_between(y[:-1], V, color='tab:orange', alpha=0.3)
        axs[1].set_ylabel("Shear [N]")
        axs[1].set_xlabel("Spanwise Position $y$ (m)")
        axs[1].grid(True)

        axs[2].plot(y[:-2], M, color='tab:green', linewidth=2, label="Bending Moment")
        axs[2].fill_between(y[:-2], M, color='tab:green', alpha=0.3)
        axs[2].set_ylabel("Moment [N·m]")
        axs[2].set_xlabel("Spanwise Position $y$ (m)")
        axs[2].grid(True)

        plt.tight_layout(rect=[0, 0, 1, 0.97])
        plt.savefig("DetailedDesign/subsystems/Plots/NVM_plot_hover.png", dpi=300)
        plt.show()

    
    def NVM_propeller_boom(self, size_thickness = False) -> float | None:
        """
        This function calculates the NVM (Normal, Shear, and Bending Moment) for the boom that supports the VTOL propellers.
        It considers the distributed loads from the wind, the boom weight, the weight from the propellers and motors and the lift that those generate.
        It then plots the distributed load, shear force, and bending moment along the span of the wing.

        Down is considered positive in this context, as per the provided reference and convention for aircraft coordinate systems.
        """

        # https://uotechnology.edu.iq/dep-MechanicsandEquipment/Lectures%20and%20Syllabus/Lectures/Aircraft/Foruth%20Grade/Aircraft%20Design3.pdf

        # DOWN IS POSITIVE
        y = np.linspace(-0.5*self.VTOL_boom_length, 0.5*self.VTOL_boom_length, 500)

        # Distributed load from the boom weight

        I_circle = (np.pi / 4)* ((self.boom_inner_diameter/2+self.VTOL_boom_thickness)**4 - (self.boom_inner_diameter/2)**4)
        boom_weight = (0.5*self.VTOL_boom_thickness)**2 * np.pi * self.VTOL_boom_length * self.density_alu *9.81
        #print('boom_mass', boom_weight / 9.81)
        W_boom = np.array([boom_weight / self.VTOL_boom_length for _ in y])

        F_gust = -0.5*self.rho_0* self.wind_speed**2 * (self.boom_inner_diameter + 2*self.VTOL_boom_thickness / 2)
        W_gust = np.array([F_gust / self.VTOL_boom_length for _ in y])

        # Point load from the propeller

        F_prop = 9.81*(self.propeller_mass_VTOL + self.motor_mass_VTOL) - 0.25*self.mtow
        V_prop = [-F_prop if i < 0 else F_prop for i in y]

        total_forces = W_boom + W_gust
        forces_rev = W_boom[::-1]

        V_left = integrate.cumulative_simpson(total_forces, x=y) - V_prop[:-1]

        V_rev = integrate.cumulative_simpson(forces_rev, x=y) + V_prop[::-1][:-1]
        V = np.concatenate((-V_left[:len(y)//2], V_rev[::-1][len(y)//2:]))

        M_left = integrate.cumulative_simpson(V_left, x=y[:-1])  
        M_rev = integrate.cumulative_simpson(V_rev, x=y[:-1])

        M = np.concatenate((-M_left[:len(y)//2], -M_rev[::-1][len(y)//2:]))

        deflection_left = -(1/(self.E_alu*I_circle))* integrate.cumulative_simpson(integrate.cumulative_simpson(M_left, x=y[:-2]), x=y[:-3])
        deflection_rev = -(1/(self.E_alu*I_circle))* integrate.cumulative_simpson(integrate.cumulative_simpson(M_rev, x=y[:-2]), x=y[:-3])

        deflection = np.concatenate((deflection_rev[::-1][len(y)//2:], deflection_left[:len(y)//2]))

        if size_thickness:
            return max(deflection)

        fig, axs = plt.subplots(4, 1, figsize=(10, 10), sharex=True)

        axs[0].plot(y, total_forces, color='tab:blue', linewidth=2, label="Distributed Load")
        axs[0].fill_between(y, total_forces, color='tab:blue', alpha=0.3)
        axs[0].set_ylabel("Load [N/m]")
        axs[0].set_xlabel("Spanwise Position $y$ (m)")
        axs[0].grid(True)

        axs[1].plot(y[:-1], V, color='tab:orange', linewidth=2, label="Shear Force")
        axs[1].fill_between(y[:-1], V, color='tab:orange', alpha=0.3)
        axs[1].set_ylabel("Shear [N]")
        axs[1].set_xlabel("Spanwise Position $y$ (m)")
        axs[1].grid(True)

        axs[2].plot(y[:-2], M, color='tab:green', linewidth=2, label="Bending Moment")
        axs[2].fill_between(y[:-2], M, color='tab:green', alpha=0.3)
        axs[2].set_ylabel("Moment [N·m]")
        axs[2].set_xlabel("Spanwise Position $y$ (m)")
        axs[2].grid(True)

        axs[3].plot(y[:len(deflection)], deflection, color='tab:pink', linewidth=2, label="Bending Moment")
        axs[3].fill_between(y[:len(deflection)], deflection, color='tab:pink', alpha=0.3)
        axs[3].set_ylabel("deflection [m]")
        axs[3].set_xlabel("Spanwise Position $y$ (m)")
        axs[3].grid(True)

        plt.tight_layout(rect=[0, 0, 1, 0.97])
        plt.savefig("DetailedDesign/subsystems/Plots/NVM_plot_propeller_boom.png", dpi=300)
        plt.show()

        return None
    
    def determine_VTOL_boom_thickness(self) -> float:
        t_range = np.linspace(0.001, 0.05, 100)
        for t in t_range:
            self.VTOL_boom_thickness = t
            deflection = self.NVM_propeller_boom(size_thickness=True)
            if deflection <= self.max_deflection_VTOL_boom:
                return round(t, 4) #rounded to half a mm
        return None
    
    def determine_fuselage_thickness(self) -> float:
        '''
        This function determines the thickness of the fuselage based on the maximum shear and stress limits of titanium.
        It calculates the required thickness based on the maximum shear force and bending moment during cruise and VTOL operations, 
        which occurs at the connection to the wing.
        
        Thin walled approx.
        '''

        _, V_cruise, M_cruise = self.NVM_cruise(return_root_values=True)
        _, V_VTOL, M_VTOL = self.NVM_VTOL(return_root_values=True)

        V = 2 * max(abs(V_cruise), abs(V_VTOL))
        M = 2 * max(abs(M_cruise), abs(M_VTOL))

        t_V = V / (self.max_shear_titanium*np.pi*self.fuselage_diameter)
        t_M = (8*M) / (np.pi*self.fuselage_diameter**3*self.max_stress_titanium)

        # Because of manufacturing
        if max(t_V, t_M) >= 0.001:
            return max(t_V, t_M)
        else:
            return 0.001
        
    def sandwich(self):

        alu_t = np.array([0.8, 1, 1.25, 1.5]) / 1000
        core_t = np.array([3, 5, 10, 20]) / 1000

        viable = []

        for t_a in alu_t:
            for t_c in core_t:
                k_eff = (2*t_a + t_c) / (2*t_a / self.conductivity_alu + t_c / self.conductivity_foam)
                max_tensile_load = max(2*t_a*self.tensile_strength_alu, t_c*self.tensile_strength_foam)
                max_shear_load = self.shear_strength_foam*t_c #This is per meter width
                E = (self.E_alu*t_a*2 + self.E_foam*t_c) / (2*t_a + t_c)
                print(f'Aluminium thickness: {t_a*1000} mm, Core thickness: {t_c*1000} mm, Effective conductivity: {round(k_eff, 3)} W/mK, max tensile stress: {max_tensile_load} N, max shear load / meter: {max_shear_load}, E: {E / 10**9}')

        return 

    # ~~~ Output functions ~~~

    def get_all(self) -> dict[str, float]:
        

        # These are all the required outputs for this class. Plz consult the rest if removing any of them!
        
        self.mass_fractions()
        self.calc_structure_mass()

        self.outputs["payload_mass"] = self.mass_payload   # updated mass of the payload (with an added margin to avoid exceeding the MTOW requirement)
        self.outputs['mass_structure'] = self.mass_structure # kg


        #self.outputs["Volume_uav"] = ...

        #CG calculations:
        #self.outputs["CG"] = ...

        return self.outputs
    
    def req_structure(self):
        pass

if __name__ == "__main__":  # pragma: no cover
    a = Structures(fi)
    #print(a.determine_VTOL_boom_thickness())
    a.NVM_VTOL()
    a.NVM_cruise()
    a.NVM_propeller_boom()
    # a.sandwich()
    print(a.mass_battery)
