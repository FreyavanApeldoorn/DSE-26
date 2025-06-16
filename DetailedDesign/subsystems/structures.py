"""
This is the file for the Structures subsystem. It contains a single class.
"""

import numpy as np
import matplotlib.pyplot as plt
import scipy as sp
from scipy import integrate
import pandas as pd


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

        self.root_chord = inputs['root_chord']    
        self.first_spar_position = inputs['first_spar_position'] * self.root_chord
        self.second_spar_position = inputs['second_spar_position'] *self.root_chord

        self.E_glass_fibre = 21.9*10**9 #Pa
        self.density_glass_fibre = 1840 #kg/m3
        self.max_shear_glass_fibre = 85*10**9
        self.max_stress_glass_fibre = 304*10**6 # best orientation


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
        boom_weight = (0.5*self.VTOL_boom_thickness)**2 * np.pi * self.VTOL_boom_length * self.density_glass_fibre *9.81
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

        deflection_left = -(1/(self.E_glass_fibre*I_circle))* integrate.cumulative_simpson(integrate.cumulative_simpson(M_left, x=y[:-2]), x=y[:-3])
        deflection_rev = -(1/(self.E_glass_fibre*I_circle))* integrate.cumulative_simpson(integrate.cumulative_simpson(M_rev, x=y[:-2]), x=y[:-3])

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
        t_range = np.linspace(0.0001, 0.05, 1000)
        for t in t_range:
            self.VTOL_boom_thickness = t
            deflection = self.NVM_propeller_boom(size_thickness=True)
            if deflection <= self.max_deflection_VTOL_boom:
                return round(t, 5)*1.5 #rounded to half a mm, 1.5 safety factor
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

        t_V = V / (self.max_shear_glass_fibre*np.pi*self.fuselage_diameter)
        t_M = (8*M) / (np.pi*self.fuselage_diameter**3*self.max_stress_glass_fibre)

        # Because of manufacturing
        if max(t_V, t_M) >= 0.00026:
            return max(t_V, t_M)
        else:
            return 0.00026
        
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

    def get_airfoil_coordinates(self): 
        with open("DetailedDesign\data\e1212_Lednicer.DAT", 'r') as f:
            lines = f.readlines()[2:]  # Skips the first two lines
        # Process coordinates
        coords = []
        for line in lines:
            line = line.strip()
            if line == "":
                coords.append("BREAK")  # Mark the break between upper and lower surfaces
                continue
            parts = line.split()
            if len(parts) == 2:
                coords.append((float(parts[0]), float(parts[1])))

        # Split at "BREAK"
        if "BREAK" in coords:
            break_index = coords.index("BREAK")
            upper = coords[:break_index]
            lower = coords[break_index + 1:]
        else:
            # Fallback: Find second occurrence of (0.0, 0.0)
            zero_index = [i for i, p in enumerate(coords) if p == (0.0, 0.0)]
            if len(zero_index) > 1:
                break_index = zero_index[1]
                upper = coords[:break_index]
                lower = coords[break_index:]
            else:
                raise ValueError("Could not split upper and lower surfaces.")

        # Convert to DataFrames
        upper_df = pd.DataFrame(upper, columns=["x", "y"])
        lower_df = pd.DataFrame(lower, columns=["x", "y"])

        return upper_df, lower_df 

    def moment_intertia(self,t): 
        upper_df, lower_df = self.get_airfoil_coordinates() 
        upper_df = upper_df.multiply(self.root_chord)
        lower_df = lower_df.multiply(self.root_chord)

        #moment of intertia for upper boom 
        x_upper = upper_df['x'].values
        y_upper = upper_df['y'].values

        dy_dx_upper = np.gradient(y_upper, x_upper)  # Central differences
        integrand_upper = y_upper **2 * np.sqrt(1 + dy_dx_upper**2)
        I_upper = t* sp.integrate.simps(integrand_upper, x_upper)

        #moment of intertia for lower boom 
        x_lower = lower_df['x'].values
        y_lower = lower_df['y'].values

        dy_dx_lower = np.gradient(y_lower, x_lower)  # Central differences
        integrand_lower = y_lower **2 * np.sqrt(1 + dy_dx_lower**2)
        I_lower = t* sp.integrate.simps(integrand_lower, x_lower)

        #moment of intertia for front spar 
        top_of_front_spar = np.interp(self.first_spar_position, upper_df["x"], upper_df["y"] ) 
        bottom_of_front_spar = np.interp(self.first_spar_position, lower_df["x"], lower_df["y"] )
        front_spar_length = top_of_front_spar - bottom_of_front_spar
        I_front_spar = t * front_spar_length **3/12 + t * front_spar_length * (bottom_of_front_spar + front_spar_length/2)

        #moment of intertia for end spar 
        top_of_end_spar = np.interp(self.second_spar_position, upper_df["x"], upper_df["y"] ) 
        bottom_of_end_spar = np.interp(self.second_spar_position, lower_df["x"], lower_df["y"] )
        end_spar_length = top_of_end_spar - bottom_of_end_spar
        I_end_spar = t * end_spar_length **3/12 + t * end_spar_length * (bottom_of_end_spar + end_spar_length/2)

        I = I_upper + I_lower + I_front_spar + I_end_spar

        return I, top_of_front_spar

    def first_moment_of_intertia(self,t): 
        upper_df, lower_df = self.get_airfoil_coordinates() 
        upper_df = upper_df.multiply(self.root_chord)
        lower_df = lower_df.multiply(self.root_chord)

        # cutting the skin at the spar positions for the length

        upper_df_skin = upper_df.query('x >= @first_spar_position and x <= @second_spar_position ')
        lower_df_skin = lower_df.query('x >= @first_spar_position and x <= @second_spar_position ')

        #moment of intertia for front spar 
        top_of_front_spar = np.interp(self.first_spar_position, upper_df["x"], upper_df["y"] ) 
        bottom_of_front_spar = np.interp(self.first_spar_position, lower_df["x"], lower_df["y"] )
        front_spar_length = top_of_front_spar - bottom_of_front_spar

        #moment of intertia for end spar 
        top_of_end_spar = np.interp(self.second_spar_position, upper_df["x"], upper_df["y"] ) 
        bottom_of_end_spar = np.interp(self.second_spar_position, lower_df["x"], lower_df["y"] )
        end_spar_length = top_of_end_spar - bottom_of_end_spar

        #length of upper and lower 
        length_upper = np.sum(np.sqrt(np.diff(upper_df_skin['x'])**2 + np.diff(upper_df_skin['y'])**2))
        length_lower = np.sum(np.sqrt(np.diff(lower_df_skin['x'])**2 + np.diff(lower_df_skin['y'])**2))

        Q_front_spar = t * front_spar_length/2 * ( bottom_of_front_spar + front_spar_length/2 + front_spar_length/4)
        Q_end_spar = t * end_spar_length/2 * ( bottom_of_end_spar + end_spar_length/2 + end_spar_length/4)
        Q_upper = t * length_upper * (top_of_front_spar - top_of_end_spar)
        Q_lower = t * length_lower * (bottom_of_front_spar - bottom_of_end_spar)

        Q = Q_front_spar + Q_end_spar + Q_upper + Q_lower

        return Q

    def normal_stress(self,t): 
        I, top_of_front_spar = self.moment_intertia(t)
        bending_moment = 60    #[N]
        y =  top_of_front_spar 
        normal_stress = bending_moment*y/I

        return normal_stress

    def shear_stress_calc(self,t):
        shear_force = -100
        I, top_of_front_spar = self.moment_intertia(t)
        Q = self.first_moment_of_intertia(t)
        shear_stress = shear_force * Q / (I* t)
        return shear_stress

    def torsion_stress_calc(self,t): 
        prop_mass = 0.073
        motor_mass = 0.825
        l_boom_placement = 0.0380
        torsion = 9.81 * (prop_mass+motor_mass) * l_boom_placement
        upper_df, lower_df = self.get_airfoil_coordinates() 
        upper_df = upper_df.multiply(self.root_chord)
        lower_df = lower_df.multiply(self.root_chord)

        #calculating the area 
        x_interp = np.linspace(self.first_spar_position,self.second_spar_position, 300)
        y_upper_interp = np.interp(x_interp, upper_df["x"], upper_df["y"])
        y_lower_interp = np.interp(x_interp, lower_df["x"], lower_df["y"])

        total_area = np.trapz(y_upper_interp - y_lower_interp,x_interp)

        torsion_stress = torsion / (2*t*total_area)
                            
        return torsion_stress

    def skin_buckling(self,b): 
        t_ribs = 0.001
        k_c = 0.5 
        D = 70 * 10**9

        buckling_stress = k_c * np.pi **2 * D * (t_ribs)/ b**2 
        return buckling_stress

    def thickness(self): 
        bending_stress = 1200000
        safety_factor = 2 
        yield_strength = 10**6 #[pa]
        t = np.linspace(0.00001,0.100, 100000)
        #while bending_stress > yield_strength * 1/safety_factor : 
        for i in t : 
            t_final_bending = i 
            bending_stress = self.normal_stress(i)
            if abs(bending_stress) < abs(yield_strength) * 1/safety_factor: 
                break 

        shear_stress = 1200000
        max_shear_stress = 10**6 
        for i in t: 
            t_final_shear = i 
            shear_stress = self.shear_stress_calc(i)
            #print("shear stress:", shear_stress)
            if abs(shear_stress)< abs(max_shear_stress) * 1/safety_factor: 
                break 

        torsion_stress = 1200000
        max_torsion_stress = 10**6 
        for i in t: 
            t_final_torsion = i 
            torsion_stress = self.torsion_stress_calc(i)
            if abs(torsion_stress)< abs(max_torsion_stress) * 1/safety_factor: 
                break 

        return t_final_bending, t_final_shear, t_final_torsion

    def rib_placement_calc(self): 
        buckling_stress = 12000
        yield_strength = 10**6 #[pa]
        safety_factor = 2
        b = np.linspace(0,2, 100) #[m]
        #while bending_stress > yield_strength * 1/safety_factor : 
        for i in b : 
            rib_placement = i 
            buckling_stress = self.skin_buckling(i)
            if abs(buckling_stress) > abs(yield_strength) * safety_factor: 
                break 
        return rib_placement

    # ~~~ Output functions ~~~

    def get_all(self) -> dict[str, float]:
        

        # These are all the required outputs for this class. Plz consult the rest if removing any of them!
        
        self.mass_fractions()
        self.calc_structure_mass()
        t_final_bending, t_final_shear, t_final_torsion= self.thickness()
        rib_placement = self.rib_placement_calc()

        self.outputs["payload_mass"] = self.mass_payload   # updated mass of the payload (with an added margin to avoid exceeding the MTOW requirement)
        self.outputs['mass_structure'] = self.mass_structure # kg
        self.outputs['final_t'] = t_final_bending
        self.outputs['rib_placement'] = rib_placement

        #self.outputs["Volume_uav"] = ...

        #CG calculations:
        #self.outputs["CG"] = ...

        return self.outputs
    
    def req_structure(self):
        pass

if __name__ == "__main__":  # pragma: no cover
    a = Structures(fi)
    #print(a.determine_VTOL_boom_thickness())
    # a.NVM_VTOL()
    # a.NVM_cruise()
    # a.NVM_propeller_boom()
    # a.sandwich()
    print(a.VTOL_boom_thickness)
    print(a.determine_fuselage_thickness())
