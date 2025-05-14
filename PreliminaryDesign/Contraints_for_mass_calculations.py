import matplotlib.pyplot as plt
import numpy as np

r_c = 3  # [m/s] rate of climb
rho = 0.9013  # density at 3000m


def powerLoading(T_W, V, n_p):
    P_W = T_W * V / n_p
    return P_W


class Constraints:
    def __init__(self, Vstall, Vmax, e, AR, CLmax, CD0, n_p, R_C_service):
        self.Vstall = Vstall
        self.Vmax = Vmax
        self.e = e
        self.AR = AR
        self.CLmax = CLmax
        self.CD0 = CD0
        self.n_p = n_p
        self.R_C_service = R_C_service

    @property
    def k(self):
        return 1 / (np.pi * self.e * self.AR)

    @property
    def q(self):
        return 0.5 * rho * self.Vmax**2

    def thrustLoadingCruise(self, W_S):
        T_W_cruise = self.q * self.CD0 * 1 / (W_S) + self.k * 1 / self.q * W_S
        return T_W_cruise

    def Vroc(self, W_S):
        Vroc = np.sqrt(2 / rho * W_S * np.sqrt(self.k / (3 * self.CD0)))
        return Vroc

    def q_climb(self, Vroc):
        q_climb = 0.5 * rho * Vroc**2
        return q_climb

    def thrustLoadingClimb(self, Vroc, W_S, R_C, q):
        T_W_climb = R_C / Vroc + q / W_S * self.CD0 + self.k / q * W_S
        return T_W_climb

    def WingLoading_Vstall(self):
        W_S_stall = 0.5 * self.Vstall**2 * rho * self.CLmax
        return W_S_stall

    def plot(self, opt = False):

        W_S = np.arange(0, 400, 1)  # [N/m^2] variable

        T_W_cruise = []
        T_W_climb = []
        P_W_cruise = []
        P_W_climb = []
        P_W_service = []
        W_S_stall = []
        T_W_service = []

        for i in W_S:
            # calculating thrust to weight ratios
            T_W_cruise.append(self.thrustLoadingCruise(i))
            T_W_climb.append(
                self.thrustLoadingClimb(
                    self.Vroc(i), i, r_c, self.q_climb(self.Vroc(i))
                )
            )
            T_W_service.append(
                self.thrustLoadingClimb(
                    self.Vroc(i), i, self.R_C_service, self.q_climb(self.Vroc(i))
                )
            )
            # calculating wing loading stall
            W_S_stall_value = self.WingLoading_Vstall()
            W_S_stall.append(W_S_stall_value)

        # Calculating Power loading
        for i in range(len(W_S)):
            P_W_cruise.append(powerLoading(T_W_cruise[i], self.Vmax, self.n_p))
            P_W_climb.append(
                powerLoading(T_W_climb[i], self.Vroc(W_S[i]), self.n_p)
            )  # self.Vroc(self.W_S[i])
            P_W_service.append(
                powerLoading(T_W_service[i], self.Vroc(W_S[i]), self.n_p)
            )

        if opt: 
            return W_S, P_W_cruise, P_W_climb, P_W_service, W_S_stall

        plt.plot(W_S, P_W_cruise, label="Cruise P_W", color="blue")
        plt.fill_between(W_S, P_W_cruise, alpha=0.3, color="blue")

        plt.plot(W_S, P_W_climb, label="Climb P_W", color="pink")
        plt.fill_between(W_S, P_W_climb, alpha=0.3, color="pink")

        plt.plot(W_S, P_W_service, label="Serivice P_W", color="green")
        plt.fill_between(W_S, P_W_service, alpha=0.3, color="green")

        # plt.plot(W_S, W_S_stall, label = "Stall Speed W_S")
        plt.vlines(
            self.WingLoading_Vstall(), 0, 100, label="Stall Speed W_S", color="red"
        )
        plt.fill_between(
            np.arange(self.WingLoading_Vstall(), W_S[-1], 1),
            np.arange(self.WingLoading_Vstall(), W_S[-1], 1),
            alpha=0.5,
            color="red",
        )

        plt.xlabel("Wing Loading [N/m^2]")
        plt.ylabel("Power Loading [N/W]")
        plt.title("Constraints Diagram")
        plt.ylim(0, 25)
        plt.xlim(20, 200)

        plt.legend()
        plt.show()
