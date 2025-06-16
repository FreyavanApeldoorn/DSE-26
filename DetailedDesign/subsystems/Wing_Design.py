import numpy as np 
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import scipy as sp

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

def get_airfoil_coordinates(): 
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

root_chord = 0.458 # [m] 
first_spar_position = 0.14 * root_chord
second_spar_position = 0.5 * root_chord  


def moment_intertia(t): 
    upper_df, lower_df = get_airfoil_coordinates() 
    upper_df = upper_df.multiply(root_chord)
    lower_df = lower_df.multiply(root_chord)

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
    top_of_front_spar = np.interp(first_spar_position, upper_df["x"], upper_df["y"] ) 
    bottom_of_front_spar = np.interp(first_spar_position, lower_df["x"], lower_df["y"] )
    front_spar_length = top_of_front_spar - bottom_of_front_spar
    I_front_spar = t * front_spar_length **3/12 + t * front_spar_length * (bottom_of_front_spar + front_spar_length/2)

    #moment of intertia for end spar 
    top_of_end_spar = np.interp(second_spar_position, upper_df["x"], upper_df["y"] ) 
    bottom_of_end_spar = np.interp(second_spar_position, lower_df["x"], lower_df["y"] )
    end_spar_length = top_of_end_spar - bottom_of_end_spar
    I_end_spar = t * end_spar_length **3/12 + t * end_spar_length * (bottom_of_end_spar + end_spar_length/2)

    I = I_upper + I_lower + I_front_spar + I_end_spar

    return I, top_of_front_spar

def first_moment_of_intertia(t): 
    upper_df, lower_df = get_airfoil_coordinates() 
    upper_df = upper_df.multiply(root_chord)
    lower_df = lower_df.multiply(root_chord)

    # cutting the skin at the spar positions for the length

    upper_df_skin = upper_df.query('x >= @first_spar_position and x <= @second_spar_position ')
    lower_df_skin = lower_df.query('x >= @first_spar_position and x <= @second_spar_position ')

    #moment of intertia for front spar 
    top_of_front_spar = np.interp(first_spar_position, upper_df["x"], upper_df["y"] ) 
    bottom_of_front_spar = np.interp(first_spar_position, lower_df["x"], lower_df["y"] )
    front_spar_length = top_of_front_spar - bottom_of_front_spar

    #moment of intertia for end spar 
    top_of_end_spar = np.interp(second_spar_position, upper_df["x"], upper_df["y"] ) 
    bottom_of_end_spar = np.interp(second_spar_position, lower_df["x"], lower_df["y"] )
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

def normal_stress(t): 
    I, top_of_front_spar = moment_intertia(t)
    bending_moment = 60    #[N]
    y =  top_of_front_spar 
    normal_stress = bending_moment*y/I

    return normal_stress

def shear_stress_calc(t):
    shear_force = -100
    I, top_of_front_spar = moment_intertia(t)
    Q = first_moment_of_intertia(t)
    shear_stress = shear_force * Q / (I* t)
    return shear_stress

def torsion_stress_calc(t): 
    prop_mass = 0.073
    motor_mass = 0.825
    l_boom_placement = 0.0380
    torsion = 9.81 * (prop_mass+motor_mass) * l_boom_placement
    upper_df, lower_df = get_airfoil_coordinates() 
    upper_df = upper_df.multiply(root_chord)
    lower_df = lower_df.multiply(root_chord)

    #calculating the area 
    x_interp = np.linspace(first_spar_position,second_spar_position, 300)
    y_upper_interp = np.interp(x_interp, upper_df["x"], upper_df["y"])
    y_lower_interp = np.interp(x_interp, lower_df["x"], lower_df["y"])

    total_area = np.trapz(y_upper_interp - y_lower_interp,x_interp)

    torsion_stress = torsion / (2*t*total_area)
                          
    return torsion_stress

def skin_buckling(b): 
    t_ribs = 0.001
    k_c = 0.5 
    D = 70 * 10**9

    buckling_stress = k_c * np.pi **2 * D * (t_ribs)/ b**2 
    return buckling_stress

def thickness(): 
    bending_stress = 1200000
    safety_factor = 2 
    yield_strength = 10**6 #[pa]
    t = np.linspace(0.00001,0.100, 100000)
    #while bending_stress > yield_strength * 1/safety_factor : 
    for i in t : 
        t_final_bending = i 
        bending_stress = normal_stress(i)
        if abs(bending_stress) < abs(yield_strength) * 1/safety_factor: 
            break 

    shear_stress = 1200000
    max_shear_stress = 10**6 
    for i in t: 
        t_final_shear = i 
        shear_stress = shear_stress_calc(i)
        #print("shear stress:", shear_stress)
        if abs(shear_stress)< abs(max_shear_stress) * 1/safety_factor: 
            break 

    torsion_stress = 1200000
    max_torsion_stress = 10**6 
    for i in t: 
        t_final_torsion = i 
        torsion_stress = torsion_stress_calc(i)
        if abs(torsion_stress)< abs(max_torsion_stress) * 1/safety_factor: 
            break 

    return t_final_bending, t_final_shear, t_final_torsion

def rib_placement_calc(): 
    buckling_stress = 12000
    yield_strength = 10**6 #[pa]
    safety_factor = 2
    b = np.linspace(0,2, 100) #[m]
    #while bending_stress > yield_strength * 1/safety_factor : 
    for i in b : 
        rib_placement = i 
        buckling_stress = skin_buckling(i)
        if abs(buckling_stress) > abs(yield_strength) * safety_factor: 
            break 
    return rib_placement



t_final_bending, t_final_shear, t_final_torsion= thickness()
rib_placement = rib_placement_calc() 

print("thickness for bending:", t_final_bending, "thickness for shear", t_final_shear, "thickness for torsion", t_final_torsion)
print("rib spacing:", rib_placement)









