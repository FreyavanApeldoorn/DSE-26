import numpy as np
from scipy.optimize import minimize

from Contraints_for_mass_calculations import powerLoading, Constraints
from electric_propulsion_mass_sizing import PropMass
from vtol_propulsion_sizing import VTOLProp
from Battery_Mass_Calculations import BattMass

# ~~~ Inputs Dictionary ~~~
inputs = {
    "rho": 0.9013,
    "MTOW": 30 * 9.81,
    "V_cruise": 100 / 3.6,
    "Vstall": 13.8,
    "CD0": 0.040,
    "n_p": 0.85,
    "R_C_service": 0.5,
    "CLmax": 1.34,
    "e": 0.7,
    "AR": 10.3,
    "stot_s_w": 1.35,
    "eta_prop": 0.83,
    "U_max": 25.5,
    "F1": 0.889,
    "E1": -0.288,
    "E2": 0.1588,
    "f_install_cruise": 1,
    "f_install_vtol": 1,
    "n_mot_cruise": 1,
    "n_mot_vtol": 4,
    "K_material": 0.6,
    "n_props_cruise": 1,
    "n_props_vtol": 4,
    "n_blades_cruise": 4,
    "n_blades_vtol": 4,
    "K_p": 0.0938,
    "t_hover": 4 * 60,
    "t_loiter": 0,
    "E_spec": 168,
    "Eta_bat": 0.95,
    "f_usable": 6000,
    "Eta_electric": 0.95,
    "LD_max": 12,
    "CL": 0.846,
    "CD": 0.04,
    "T": 30 * 9.81,
    "h_end": 100,
    "h_start": 0,
    "MF_struct": 0.35,
    "MF_avion": 0.05,
    "MF_Subsyst": 0.07,
    "M_payload": 5,
    "amount_of_iterations": 10
}

# ~~~ Iteration Loop ~~~
def iteration(M_TO, w_s, p_w, VTOL_prop_mod: VTOLProp, prop_mass: PropMass, batt_mass: BattMass):
    count = 0
    MTOW = M_TO * 9.81
    while True:
        count += 1
        s = MTOW / w_s
        P_max_cruise = MTOW * p_w

        VTOL_prop_mod.MTOW = MTOW
        p_req_VTOL, S_prop, DL, T = VTOL_prop_mod.power_required_vtol()
        D_prop_VTOL = 2 * (S_prop / np.pi) ** 0.5

        prop_mass.P_max_vtol = p_req_VTOL
        prop_mass.D_prop_vtol = D_prop_VTOL

        motor_mass_cruise, _, motor_mass_VTOL, _ = prop_mass.calculate_motor_mass()
        esc_mass_cruise, _, esc_mass_VTOL, _ = prop_mass.calculate_esc_mass()
        propeller_mass_cruise, _, propeller_mass_VTOL, _ = prop_mass.calculate_propeller_mass()
        M_FW_Prop, M_Vtol_Prop = prop_mass.calculate_propulsion_mass()

        batt_mass.M_to = M_TO
        batt_mass.DL = DL
        batt_mass.T = T

        MF_Batt, _ = batt_mass.Batt_Mass_Total()

        new_M_TO = (M_Vtol_Prop + M_FW_Prop + inputs["M_payload"]) / (
            1 - (MF_Batt + inputs["MF_struct"] + inputs["MF_Subsyst"] + inputs["MF_avion"])
        )

        if abs(new_M_TO - M_TO) / M_TO < 0.001:
            return count, M_TO, MF_Batt * M_TO, p_req_VTOL, P_max_cruise, T / MTOW, D_prop_VTOL, s
        else:
            M_TO = new_M_TO
            MTOW = M_TO * 9.81

def mass_sizing(inputs: dict[str, float | int]):

    # ~~~ Optimization Loop ~~~

    constraint_plot = Constraints(
    inputs["Vstall"],
    inputs["V_cruise"],
    inputs["e"],
    inputs["AR"],
    inputs["CLmax"],
    inputs["CD0"],
    inputs["n_p"],
    inputs["R_C_service"]
    )

    W_S, P_W_cruise, P_W_climb, P_W_service, W_S_stall = constraint_plot.plot(True)
    all_masses = []

    for i in range(len(W_S)):
        w_s = W_S[i]
        if w_s < W_S_stall[0] and w_s > 10:
            p_w = max([P_W_cruise[i], P_W_climb[i], P_W_service[i]])
            s = 30 * 9.81 / w_s
            P_max_cruise = 30 * 9.81 * p_w

            VTOL_prop_mod = VTOLProp(w_s, inputs["stot_s_w"], 30 * 9.81, inputs["eta_prop"])
            p_req_VTOL, S_prop, DL, T = VTOL_prop_mod.power_required_vtol()
            D_prop_VTOL = 2 * (S_prop / np.pi) ** 0.5

            prop_mass = PropMass(
                P_max_cruise,
                p_req_VTOL,
                inputs["U_max"],
                inputs["F1"],
                inputs["E1"],
                inputs["E2"],
                inputs["f_install_cruise"],
                inputs["f_install_vtol"],
                inputs["n_mot_cruise"],
                inputs["n_mot_vtol"],
                inputs["K_material"],
                inputs["n_props_cruise"],
                inputs["n_props_vtol"],
                inputs["n_blades_cruise"],
                inputs["n_blades_vtol"],
                D_prop_VTOL,
                inputs["K_p"]
            )

            batt_mass = BattMass(
                inputs["t_hover"],
                inputs["t_loiter"],
                30,
                inputs["E_spec"],
                inputs["Eta_bat"],
                inputs["f_usable"],
                inputs["Eta_electric"],
                T,
                DL,
                inputs["LD_max"],
                inputs["CL"],
                inputs["CD"],
                w_s,
                inputs["h_end"],
                inputs["h_start"],
                p_req_VTOL,
                inputs["n_props_vtol"]
            )

            _, M_TO, _, _, _, _, _, _ = iteration(30, w_s, p_w, VTOL_prop_mod, prop_mass, batt_mass)
            all_masses.append([M_TO, w_s, p_w])

    # Get final parameters
    best_config = min(all_masses, key=lambda x: x[0])
    w_s = best_config[1]
    p_w = best_config[2]
    s = inputs["MTOW"] / w_s
    P_max_cruise = inputs["MTOW"] * p_w

    VTOL_prop_mod = VTOLProp(w_s, inputs["stot_s_w"], inputs["MTOW"], inputs["eta_prop"])
    p_req_VTOL, S_prop, DL, T = VTOL_prop_mod.power_required_vtol()
    D_prop_VTOL = 2 * (S_prop / np.pi) ** 0.5

    prop_mass = PropMass(
        P_max_cruise,
        p_req_VTOL,
        inputs["U_max"],
        inputs["F1"],
        inputs["E1"],
        inputs["E2"],
        inputs["f_install_cruise"],
        inputs["f_install_vtol"],
        inputs["n_mot_cruise"],
        inputs["n_mot_vtol"],
        inputs["K_material"],
        inputs["n_props_cruise"],
        inputs["n_props_vtol"],
        inputs["n_blades_cruise"],
        inputs["n_blades_vtol"],
        D_prop_VTOL,
        inputs["K_p"]
    )

    motor_mass_cruise, _, motor_mass_VTOL, _ = prop_mass.calculate_motor_mass()
    esc_mass_cruise, _, esc_mass_VTOL, _ = prop_mass.calculate_esc_mass()
    propeller_mass_cruise, _, propeller_mass_VTOL, _ = prop_mass.calculate_propeller_mass()
    M_FW_Prop, M_Vtol_Prop = prop_mass.calculate_propulsion_mass()

    batt_mass = BattMass(
        inputs["t_hover"],
        inputs["t_loiter"],
        inputs["MTOW"] / 9.81,
        inputs["E_spec"],
        inputs["Eta_bat"],
        inputs["f_usable"],
        inputs["Eta_electric"],
        T,
        DL,
        inputs["LD_max"],
        inputs["CL"],
        inputs["CD"],
        w_s,
        inputs["h_end"],
        inputs["h_start"],
        p_req_VTOL,
        inputs["n_props_vtol"]
    )

    MF_Batt, battery_mass_endurance = batt_mass.Batt_Mass_Total()

    M_TO = (M_Vtol_Prop + M_FW_Prop + inputs["M_payload"]) / (
        1 - (MF_Batt + inputs["MF_struct"] + inputs["MF_Subsyst"] + inputs["MF_avion"])
    )
    inputs["MTOW"] = M_TO * 9.81

    return inputs['MTOW'] / 9.81

print(mass_sizing(inputs))



    



