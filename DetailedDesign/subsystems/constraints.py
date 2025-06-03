'''
This is the file for the constraints analysis. It contains a single class.
'''

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

import matplotlib.pyplot as plt
import numpy as np



def powerLoading(T_W, V, n_p):
    P_W = T_W * V / n_p
    return P_W


class Constraints:
    def __init__(self, inputs: dict[str, float])-> None:

        self.inputs = inputs
        self.V_stall = inputs['V_stall']
        self.V_max = inputs['V_cruise'] 
        self.e = inputs ['e']
        self.AR = inputs['AR']
        self.CL_max = inputs ['CL_max']
        self.CD_0 = inputs ['CD_0']
        self.eff_prop = inputs ['eff_prop']
        self.R_C_service = inputs ['ROC_service']
        self.mtow = inputs['MTOW']

        self.rho_0 = inputs["rho_0"]
        self.rho_service = inputs["rho_service"]
        self.r_c = inputs["ROC_cruise"]

        self.outputs = self.inputs.copy()
    

    @property
    def k(self):
        return 1 / (np.pi * self.e * self.AR)

    @property
    def q(self):
        return 0.5 * self.rho_service * self.V_max**2

    def thrustLoadingCruise(self, W_S):
        T_W_cruise = self.q * self.CD_0 * 1 / (W_S) + self.k * 1 / self.q * W_S
        return T_W_cruise

    def Vroc(self, W_S):
        Vroc = np.sqrt(2 / self.rho_service * W_S * np.sqrt(self.k / (3 * self.CD_0)))
        return Vroc

    def q_climb(self, Vroc):
        q_climb = 0.5 * self.rho_service * Vroc**2
        return q_climb

    def thrustLoadingClimb(self, Vroc, W_S, R_C, q):
        T_W_climb = R_C / Vroc + q / W_S * self.CD_0 + self.k / q * W_S
        return T_W_climb

    def WingLoading_Vstall(self):
        W_S_stall = 0.5 * self.V_stall**2 * self.rho_service * self.CL_max
        return W_S_stall

    def form_variable_lists(self) -> tuple[list | float]:

        W_S = np.arange(0, 600, 1)  # [N/m^2] variable

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
                    self.Vroc(i), i, self.r_c, self.q_climb(self.Vroc(i))
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
            P_W_cruise.append(powerLoading(T_W_cruise[i], self.V_max, self.eff_prop))
            P_W_climb.append(
                powerLoading(T_W_climb[i], self.Vroc(W_S[i]), self.eff_prop)
            )  # self.Vroc(self.W_S[i])
            P_W_service.append(
                powerLoading(T_W_service[i], self.Vroc(W_S[i]), self.eff_prop)
            )
        
        opt_P_W = P_W_climb[int(self.WingLoading_Vstall())] 
         
        optimal_cruise_power = opt_P_W * self.mtow

        return W_S, P_W_cruise, P_W_climb, P_W_service, W_S_stall, optimal_cruise_power

        
    def get_all(self) -> dict[str, float]:
            outputs = self.inputs.copy()
            W_S, P_W_cruise, P_W_climb, P_W_service, W_S_stall, optimal_cruise_power = self.form_variable_lists()
            
            outputs["wing_loading"] = W_S_stall[0]
            outputs["P_W_cruise"] = P_W_cruise[int(self.WingLoading_Vstall())]
            outputs["P_W_climb"] = P_W_climb[int(self.WingLoading_Vstall())]
            outputs["P_W_service"] = P_W_service[int(self.WingLoading_Vstall())]

            outputs["power_required_cruise"] = optimal_cruise_power

            return outputs

    
if __name__ == '__main__': # pragma: no cover
    from DetailedDesign.funny_inputs import funny_inputs
    # Perform sanity checks here
    constraints = Constraints(funny_inputs)
    W_S, P_W_cruise, P_W_climb, P_W_service, W_S_stall, optimal_cruise_power = constraints.form_variable_lists()

    #Plotting the constraints diagram 
    plt.plot(W_S, P_W_cruise, label="Cruise P_W", color="blue")
    plt.fill_between(W_S, P_W_cruise, alpha=0.3, color="blue")

    plt.plot(W_S, P_W_climb, label="Climb P_W", color="pink")
    plt.fill_between(W_S, P_W_climb, alpha=0.3, color="pink")

    plt.plot(W_S, P_W_service, label="Serivice P_W", color="green")
    plt.fill_between(W_S, P_W_service, alpha=0.3, color="green")

    # plt.plot(W_S, W_S_stall, label = "Stall Speed W_S")
    plt.vlines(
        W_S_stall, 0, 100, label="Stall Speed W_S", color="red"
    )
    # plt.fill_between(
    #     np.arange(W_S_stall, W_S[-1], 1),
    #     np.arange(W_S_stall, W_S[-1], 1),
    #     alpha=0.5,
    #     color="red",
    # )
    plt.xlabel("Wing Loading [N/m^2]")
    plt.ylabel("Power Loading [N/W]")
    plt.title("Constraints Diagram")
    plt.ylim(0, 25)
    plt.xlim(20, int(W_S_stall[0]) + 40)
    plt.legend()
    #plt.savefig('PreliminaryDesign\Plots\constraints')
    plt.show()
