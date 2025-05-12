import numpy as np


def thrust_to_weight_vtol(rho: float, w_s: float, r_c: float, stot_sw: float):
    """
    Calculate the thrust-to-weight ratio for a VTOL mode.

    Parameters:
    rho (float): Air density (kg/m^3)
    w_s (float): Wing loading (N/m^2)
    r_c (float): VTOL rate of climb (m/s)
    s_tot_s_w (float): Total projected aircraft area to wing area ratio

    Returns:
    float: Thrust-to-weight ratio
    """
    return 1.2 * (1 + (1 / w_s) * rho * r_c**2 * stot_sw)


def power_required_vtol(T: float, M_TO: float, eta_prop: float, rho: float, r_c: float):
    """
    Calculate the power required for VTOL mode.

    Parameters:s
    T (float): Thrust (N)
    M_TO (float): Takeoff mass (kg)
    eta_prop (float): Propeller efficiency
    rho (float): Air density (kg/m^3)
    r_c (float): VTOL rate of climb (m/s)

    Returns:
    float: Power required (W)
    """
    # Calculate the FM based on the thrust value, based on statistical relationship [FOR T = 0 - 100 N, EXTRAPOLATING OUTSIDE].
    FM = 0.4742 * T**0.0793

    # Calculate propeller disc loading DL, based on statistical relationship [FOR M_TO = 0 - 20 kg, EXTRAPOLATING OUTSIDE].
    DL = 3.2261 * M_TO + 74.991

    # Calculate propeller disc area S_prop
    S_prop = (M_TO * 9.81) / (DL * eta_prop)

    # Calculate induced hover velocity v_h
    v_h = np.sqrt(T / (2 * rho * S_prop))

    # Calculate induced axial climb velocity v_i
    v_i = v_h * (-r_c / (2 * v_h) + np.sqrt((r_c / (2 * v_h)) ** 2 + 1))

    return (T * v_i) / FM
