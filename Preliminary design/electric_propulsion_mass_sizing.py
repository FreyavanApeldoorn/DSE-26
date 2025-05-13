g = 9.81  # Acceleration due to gravity (m/s^2)


class PropMass:

    def __init__(
        self,
        P_max_cruise: float,
        P_max_vtol: float,
        U_max: float,
        F1: float,
        E1: float,
        E2: float,
        f_install_cruise: float,
        f_install_vtol: float,
        n_mot_cruise: int,
        n_mot_vtol: int,
        K_material: float,
        n_props_cruise: int,
        n_props_vtol: int,
        n_blades_cruise: int,
        n_blades_vtol: int,
        D_prop_vtol: float,
        K_p: float,
    ):
        """
        Initialize the PropMass class with the given parameters.
        Parameters:
        P_max_cruise (float): Maximum power for cruise mode (W)
        P_max_vtol (float): Maximum power for VTOL mode (W)
        U_max (float): Maximum voltage (V)
        F1 (float): Motor constant (kg/W^E1 * V^E2) [CONSULT TABLE 4]
        E1 (float): Exponent for power [CONSULT TABLE 4]
        E2 (float): Exponent for voltage [CONSULT TABLE 4]
        F1_esc (float): ESC constant (kg/W^E1) [DEFAULT FROM PAPER]
        E1_esc (float): Exponent for power [DEFAULT FROM PAPER]
        f_install_cruise (float): Cruise propulsion installation factor
        f_install_vtol (float): VTOL propulsion installation factor
        n_mot_cruise (int): Number of cruise motors
        n_mot_vtol (int): Number of VTOL motors
        K_material (float): Material constant (kg/m^3) [1.3 for wooden, 1 for plastic, 0.6 for composite]
        K_prop (float): Propeller constant (kg/m^3) [15 reccomended for propellers with enginer power < 50 hp]
        n_props_cruise (int): Number of cruise propellers
        n_props_vtol (int): Number of VTOL propellers
        n_blades_cruise (int): Number of blades per cruise propeller
        n_blades_vtol (int): Number of blades per VTOL propeller
        D_prop_cruise (float): Cruise propeller diameter (m)
        D_prop_vtol (float): VTOL propeller diameter (m)
        K_p (float): Constant for propeller diameter calculation [0.1072, 0.0995, 0.0938 for two-, three-, and four-blade propellers]
        """

        self.P_max_cruise = P_max_cruise
        self.P_max_vtol = P_max_vtol
        self.U_max = U_max
        self.F1 = F1
        self.E1 = E1
        self.E2 = E2
        self.F1_esc = 0.7383e-4  # DEFAULT FROM PAPER
        self.E1_esc = 0.8854  # DEFAULT FROM PAPER
        self.f_install_cruise = f_install_cruise
        self.f_install_vtol = f_install_vtol
        self.n_mot_cruise = n_mot_cruise
        self.n_mot_vtol = n_mot_vtol
        self.K_material = K_material
        self.K_prop = 15  # Reccomended for propellers with engine power < 50 hp
        self.n_props_cruise = n_props_cruise
        self.n_props_vtol = n_props_vtol
        self.n_blades_cruise = n_blades_cruise
        self.n_blades_vtol = n_blades_vtol
        self.D_prop_vtol = D_prop_vtol
        self.K_p = K_p

    def calculate_motor_mass(self):
        """
        Calculate individual motor masses based on the given parameters for VTOL/cruise modes.
        Assumes that the motors are the same for both modes.

        Parameters:
        P_max (float): Maximum power (W)
        U_max (float): Maximum voltage (V)
        n_mot (int): Number of motors
        F1 (float): Motor constant (kg/W^E1 * V^E2) [CONSULT TABLE 4]
        E1 (float): Exponent for power [CONSULT TABLE 4]
        E2 (float): Exponent for voltage [CONSULT TABLE 4]


        Returns:
        float: Cruise motor mass (kg)
        int: Number of cruise motors [Confirm to user]
        float: VTOL motor mass (kg)
        int: Number of VTOL motors [Confirm to user]
        """

        # Calculate motor weight to power ratio W_mot / P_max
        W_mot_P_max_cruise = self.F1 * self.P_max_cruise**self.E1 * self.U_max**self.E2
        W_mot_P_max_vtol = self.F1 * self.P_max_vtol**self.E1 * self.U_max**self.E2

        return (
            W_mot_P_max_cruise * (self.P_max_cruise / self.n_mot_cruise) / g,
            self.n_mot_cruise,
            W_mot_P_max_vtol * (self.P_max_vtol / self.n_mot_vtol) / g,
            self.n_mot_vtol,
        )

    def calculate_esc_mass(self):
        """
        Calculate individiual ESC masses based on the given parameters.
        Assumes that the ESCs are the same for both modes.

        Parameters:
        P_max_cruise (float): Cruise maximum power (W)
        P_max_vtol (float): VTOL maximum power (W)
        n_mot_cruise (int): Number of cruise motors
        n_mot_vtol (int): Number of VTOL motors
        F1_esc (float): ESC constant (kg/W^E1) [DEFAULT FROM PAPER]
        E1_esc (float): Exponent for power [DEFAULT FROM PAPER]

        Returns:
        float: Cruise ESC mass (kg)
        int: Number of cruise ESCs [Confirm to user]
        float: VTOL ESC mass (kg)
        int: Number of VTOL ESCs [Confirm to user]
        """

        return (
            self.F1_esc * (self.P_max_cruise) ** self.E1_esc,
            self.n_mot_cruise,
            self.F1_esc * (self.P_max_vtol) ** self.E1_esc,
            self.n_mot_vtol,
        )

    def calculate_propeller_mass(self):
        """
        Calculate the total propeller mass based on the given parameters.
        Assumes that the propeller material is the same for both modes, but number of blades and diameter can differ for both modes.

        Parameters:
        K_material (float): Material constant (kg/m^3) [1.3 for wooden, 1 for plastic, 0.6 for composite]
        K_prop (float): Propeller constant (kg/m^3) [15 reccomended for propellers with enginer power < 50 hp]
        n_props_cruise (int): Number of cruise propellers
        n_props_vtol (int): Number of VTOL propellers
        n_blades_cruise (int): Number of blades per cruise propeller
        n_blades_vtol (int): Number of blades per VTOL propeller
        D_prop_cruise (float): Cruise propeller diameter (m)
        D_prop_vtol (float): VTOL propeller diameter (m)
        P_max_cruise (float): Cruise maximum power (W)
        P_max_vtol (float): VTOL maximum power (W)

        Returns:
        float: Individual cruise propeller mass (kg)
        int: Number of cruise propellers [Confirm to user]
        float: Individual VTOL propeller mass (kg)
        int: Number of VTOL propellers [Confirm to user]
        """

        return (
            6.514e-3
            * self.K_material
            * self.K_prop
            * self.n_props_cruise
            * self.n_blades_cruise**0.391
            * (
                (self.calculate_cruise_propeller_diameter() * self.P_max_cruise)
                / (1000 * self.n_props_cruise)
            )
            ** 0.782,
            self.n_props_cruise,
            6.514e-3
            * self.K_material
            * self.K_prop
            * self.n_props_vtol
            * self.n_blades_vtol**0.391
            * ((self.D_prop_vtol * self.P_max_vtol) / (1000 * self.n_props_vtol))
            ** 0.782,
            self.n_props_vtol,
        )

    def calculate_propulsion_mass(self):
        """
        Calculate the total propulsion system mass based on the given parameters.

        Parameters:
        f_install_cruise (float): Cruise propulsion installation factor
        f_install_vtol (float): VTOL propulsion installation factor
        n_mot_cruise (int): Number of cruise motors
        n_mot_vtol (int): Number of VTOL motors

        Returns:
        float: Cruise propulsion system mass (kg)
        float: VTOL propulsion system mass (kg)
        """

        return self.f_install_cruise * (
            self.n_mot_cruise
            * (self.calculate_motor_mass()[0] + self.calculate_esc_mass()[0])
            + self.calculate_propeller_mass()[0]
        ), self.f_install_vtol * (
            self.n_mot_vtol
            * (self.calculate_motor_mass()[2] + self.calculate_esc_mass()[2])
            + self.calculate_propeller_mass()[2]
        )

    def calculate_cruise_propeller_diameter(self):
        """
        Calculate the cruise propeller diameter based on the given parameters.

        Parameters:
        P_max_cruise (float): Cruise maximum power (W)
        n_props_cruise (int): Number of cruise propellers
        n_blades_cruise (int): Number of blades per cruise propeller
        K_material (float): Material constant (kg/m^3) [1.3 for wooden, 1 for plastic, 0.6 for composite]
        K_prop (float): Propeller constant (kg/m^3) [15 reccomended for propellers with enginer power < 50 hp]

        Returns:
        float: Cruise propeller diameter (m)
        """

        return self.K_p * (self.P_max_cruise / self.n_props_cruise) ** (1 / 4)
