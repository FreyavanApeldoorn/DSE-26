def calculate_motor_mass(P_max: float, U_max: float, F1: float, E1: float, E2: float):
    """
    Calculate the motor mass based on the given parameters.

    Parameters:
    P_max (float): Maximum power (W)
    U_max (float): Maximum voltage (V)
    F1 (float): Motor constant (kg/W^E1 * V^E2) [CONSULT TABLE 4]
    E1 (float): Exponent for power [CONSULT TABLE 4]
    E2 (float): Exponent for voltage [CONSULT TABLE 4]

    Returns:
    float: Motor weight (N)
    """

    # Calculate motor weight to power ratio W_mot / P_max
    W_mot_P_max = F1 * P_max**E1 * U_max**E2

    return W_mot_P_max * P_max


def calculate_esc_mass(P_max: float, F_esc: float = 0.7383e-4, E1: float = 0.8854):
    """
    Calculate the ESC mass based on the given parameters.

    Parameters:
    P_max (float): Maximum power (W)
    F_esc (float): ESC constant (kg/W^E1) [DEFAULT FROM PAPER]
    E1 (float): Exponent for power [DEFAULT FROM PAPER]

    Returns:
    float: ESC mass (kg)
    """

    return F_esc * P_max**E1


def calculate_propeller_mass(
    K_material: float,
    K_prop: float,
    n_props: int,
    n_blades: int,
    D_prop: float,
    P_max: float,
):
    """
    Calculate the propeller mass based on the given parameters.

    Parameters:
    K_material (float): Material constant (kg/m^3) [1.3 for wooden, 1 for plastic, 0.6 for composite]
    K_prop (float): Propeller constant (kg/m^3) [15 reccomended for propellers with enginer power < 50 hp]
    n_props (int): Number of propellers
    n_blades (int): Number of blades per propeller
    D_prop (float): Propeller diameter (m)
    P_max (float): Maximum power of ALL (combined) propellers (W)

    Returns:
    float: Propeller mass (kg)
    """

    return (
        6.514e-3
        * K_material
        * K_prop
        * n_props
        * n_blades**0.391
        * ((D_prop * P_max) / (1000 * n_props)) ** 0.782
    )


def calculate_propulsion_mass(f_install, n_mot, W_mot_P_max, P_mot, M_esc, M_prop):
    """
    Calculate the propulsion mass based on the given parameters.

    Parameters:
    f_install (float): Installation factor
    n_mot (int): Number of motors
    W_mot_P_max (float): Motor weight to power ratio (kg/W)
    P_mot (float): Motor power (W)
    M_esc (float): ESC mass (kg)
    M_prop (float): Propeller mass (kg)

    Returns:
    float: Propulsion mass (kg)
    """

    return f_install * (n_mot * (W_mot_P_max * P_mot / 9.81 + M_esc) + n_mot + M_prop)
