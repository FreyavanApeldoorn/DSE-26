import numpy as np
from scipy.optimize import minimize

from Classes.Contraints_for_mass_calculations import powerLoading, Constraints
from Classes.electric_propulsion_mass_sizing import PropMass
from Classes.vtol_propulsion_sizing import VTOLProp
from Classes.Battery_Mass_Calculations import BattMass

# ~~~ Iteration Loop ~~~
def iteration(M_TO: float, w_s: float, p_w: float, VTOL_prop_mod: VTOLProp, prop_mass: PropMass, M_batt: float, M_payload: float, MF_struct: float, MF_Subsyst: float, MF_avion: float) -> tuple[int, float, float, float, float, float, float, float]:
    '''
    Given a set w_s and p_w, iterate until the MTOW stabilizes
    '''
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

        M_FW_Prop, M_Vtol_Prop = prop_mass.calculate_propulsion_mass()
        

        new_M_TO = (M_Vtol_Prop + M_FW_Prop + M_payload + M_batt) / (
            1 - (MF_struct + MF_Subsyst + MF_avion)
        )
        #print(f"M_Vtol_Prop: {M_Vtol_Prop}, M_FW_Prop: {M_FW_Prop}, M_batt: {M_batt}, M_payload: {M_payload}, M_TO: {new_M_TO}")

        if abs(new_M_TO - M_TO) / M_TO < 0.001:
            return count, M_TO, M_batt, p_req_VTOL, P_max_cruise, T / MTOW, D_prop_VTOL, s
        else:
            M_TO = new_M_TO
            MTOW = M_TO * 9.81

def mass_sizing(inputs: dict[str, float | int]) -> dict[str, float | int]:

    '''
    Performs initial sizing based on the given inputs and returns the updated inputs.
    The function iterates over a range of wing loadings and power loadings to find the optimal configuration for the aircraft.
    '''

    # ~~~ Optimization Loop ~~~

    constraint_plot = Constraints(
    inputs["V_stall"],
    inputs["V_cruise"],
    inputs["e"],
    inputs["AR"],
    inputs["CL_max"],
    inputs["CD0"],
    inputs["propeller_efficiency_cruise"],
    inputs["RC_service"]
    )

    W_S, P_W_cruise, P_W_climb, P_W_service, W_S_stall = constraint_plot.plot(True)
    all_masses = []

    for i in range(len(W_S)):
        w_s = W_S[i]
        if w_s < W_S_stall[0] and w_s > 10:
            p_w = max([P_W_cruise[i], P_W_climb[i], P_W_service[i]])
            s = inputs['M_to'] * 9.81 / w_s
            P_max_cruise = inputs['M_to'] * 9.81 * p_w

            VTOL_prop_mod = VTOLProp(w_s, inputs["stot_s_w"], inputs['M_to'] * 9.81, inputs["n_propellers_vtol"])
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
                inputs["n_propellers_cruise"],
                inputs["n_propellers_vtol"],
                inputs["n_blades_cruise"],
                inputs["n_blades_vtol"],
                D_prop_VTOL,
                inputs["K_p"]
            )

            _, M_TO, _, _, _, _, _, _ = iteration(inputs['M_to'], w_s, p_w, VTOL_prop_mod, prop_mass, inputs["M_battery"], inputs['M_payload'], inputs['MF_struct'], inputs['MF_Subsyst'], inputs['MF_avion'])
            all_masses.append([M_TO, w_s, p_w])

    # ~~~ Get final parameters ~~~
    best_config = min(all_masses, key=lambda x: x[0])
    w_s = best_config[1]
    p_w = best_config[2]
    s = inputs["MTOW"] / w_s
    P_max_cruise = inputs["MTOW"] * p_w
    VTOL_prop_mod = VTOLProp(w_s, inputs["stot_s_w"], inputs["MTOW"], inputs["n_propellers_vtol"])
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
        inputs["n_propellers_cruise"],
        inputs["n_propellers_vtol"],
        inputs["n_blades_cruise"],
        inputs["n_blades_vtol"],
        D_prop_VTOL,
        inputs["K_p"]
    )

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
        inputs["CL_cruise"],
        inputs["CD_cruise"],
        w_s,
        inputs["h_cruise"],
        inputs["h_ground"],
        p_req_VTOL,
        inputs["n_propellers_vtol"]
    )

    count, M_TO, M_Batt, p_req_VTOL, P_max_cruise, t_w, D_prop_VTOL, s = iteration(inputs['MTOW'], w_s, p_w, VTOL_prop_mod, prop_mass, inputs['M_battery'], inputs['M_payload'], inputs['MF_struct'], inputs['MF_Subsyst'], inputs['MF_avion'])

    b = (s*inputs['AR'])**0.5

    inputs['M_to'] = M_TO
    inputs['MTOW'] = M_TO*9.81
    inputs['M_battery'] = M_Batt
    inputs['P_r_VTOL'] = p_req_VTOL
    inputs['P_r_FW'] = P_max_cruise
    inputs['t_w'] = t_w
    inputs['propeller_diameter'] = D_prop_VTOL
    inputs['S_wing'] = s
    inputs['b_wing'] = b
    inputs['w_s'] = w_s

    return inputs