import matplotlib.pyplot as plt
import numpy as np

# scale = 1: 247

# Tail Design for controllability

Cruise_V = 141  # m/s
Approach_V = 58  # m/s  or 113 kts
Vh_V_2 = (
    0.95  # 0.85 for fuselage mounted stabiliser, 0.95 for fin mounted and 1 for T-tail.
)

x_cg_bar = np.linspace(-1, 1, 1000)  # changes to plot
SM = 0.05

a_cr = 309
a_app = 343

rho_cr = 0.551
rho_app = 1.225
W = 23000 * 9.81  # weight of aircraft kg


# Wing characteristics
S = 61  # surface area of wing m^2
A = 12  # aspect ratio
sweep1_4 = 3 * np.pi / 180  # sweep at 1/4 chord
bf = 2.77  # width fuselage
lf = 27.166  # length of fuselage
hf = 2.32  # height fuselage
lfn = 10.8  # length from nose to wing
lam = 0.59  # taper ratio
b = 27.05  # wing span
cg = S / b  # mean geometric chord
c_bar = 2.19  # Mean aerodynamic chord


# Horizontal tail characteristics
S_h = 11.7  # area of horizontal tail
Sweep_half_Ch = 8 * np.pi / 180  # sweep at half chord of horizontal tail
lh = 13.57
A_h = 4.57


# Calculations of pararameters for Stability Equations ####################################################################################
def Beta_calc(V, a):
    V = V  # make use of Critical speed for stability assesment
    Vh = np.sqrt(Vh_V_2) * V
    M = Vh / a
    Beta = np.sqrt(1 - M**2)
    return Beta


def CLah_calc(Ar, Sweep, V, a):
    Beta = Beta_calc(V, a)  # Compressebility factor
    eta = 0.95  # efficiency contant
    # sweep_0.5_Ch

    ClaAh = (
        2
        * np.pi
        * Ar
        / (
            2
            + np.sqrt(
                4 + ((Ar * Beta / eta) ** 2) * (1 + (np.tan(Sweep) ** 2) / (Beta**2))
            )
        )
    )
    return ClaAh


CLah_Vcr = CLah_calc(A_h, Sweep_half_Ch, Cruise_V, a_cr)  # Stability Clah


def CLaAh_calc(V, a):
    cr = 2.626
    S_net = (
        S - bf * cr
    )  # equal to S less the projection of the central wing part inside the fuselage
    CLaAh = CLah_calc(A, sweep1_4, V, a) * (1 + 2.15 * bf / b) * (
        S_net / S
    ) + np.pi * bf**2 / (2 * S)
    return CLaAh


CLaAh_Vcr = CLaAh_calc(Cruise_V, a_cr)  # Stability ClaAh


def aerodynamic_center(x_ac_w, CLaAh, V, a):
    Bp = 6
    Dp = 3.93
    ln = 1 / 4 * 10.77
    bn = 1.3

    x_ac_bar_w = x_ac_w
    x_ac_bar_f = -1.8 / CLaAh * (bf * hf * lfn) / (S * c_bar) + 0.273 / (1 + lam) * (
        bf * cg * (b - bf)
    ) / (c_bar**2 * (b + 2.15 * bf)) * np.tan(sweep1_4)
    # x_ac_bar_p = - 0.05* Bp*Dp**2*lp/(S*c_bar*CLaAh_calc(V,a)) * 2
    x_ac_bar_n = 2 * (-4) * bn**2 * ln / (S * c_bar * CLaAh_calc(V, a))
    x_ac_bar = x_ac_bar_w + x_ac_bar_f + x_ac_bar_n
    return x_ac_bar


x_ac_w_cr = (
    0.24  # get from graph on slide  36 STABILITY lambda = 0.6 , sweep B = 3.3 deg
)
x_ac_bar_cr = aerodynamic_center(
    x_ac_w_cr, CLaAh_Vcr, Cruise_V, a_cr
)  # contribution of wing fuselage and nacelle
print(aerodynamic_center(x_ac_w_cr, CLaAh_Vcr, Cruise_V, a_cr))


def de_da_calc(rho):
    mtv = 0.5 * 7.65 * 2 / b
    r = lh * 2 / b
    Pbr = 2132  # shaft horse power at max cruise  (MAX TAKE OFF WEIGHT)
    CL = W / (0.5 * rho * Cruise_V**2 * S)  # must be at cruise
    KEA = (0.1124 + 0.1264 * sweep1_4 + 0.1766 * sweep1_4**2) / r**2 + 0.1024 / r + 2
    KEA0 = 0.1124 / r**2 + 0.1024 / r + 1
    de_da_one = (
        KEA
        / KEA0
        * (
            r / (r**2 + mtv**2) * 0.4876 / (np.sqrt(r**2 + 0.6319 + mtv**2))
            + (1 + (r**2 / (r**2 + 0.7915 + 5.0734 * mtv**2)) ** (0.3113))
            * (1 - np.sqrt(mtv**2 / (1 + mtv**2)))
        )
        * CLah_calc(A, sweep1_4, Cruise_V, a_cr)
        / (np.pi * A)
    )
    phi = np.arcsin(mtv / r)
    prop_eff = (
        6.5
        * (rho * Pbr**2 * S**3 * CL**3 / (lh**4 * W**3)) ** (1 / 4)
        * (np.sin(6 * phi)) ** 2.5
    )
    de_da = de_da_one + prop_eff
    return de_da


de_da_cr = de_da_calc(rho_cr)

# Calculations of parameters for Controllability equations ############################################################################################

CLah_App = CLah_calc(A_h, Sweep_half_Ch, Approach_V, a_app)  # Controlability CLah
CLaAh_App = CLaAh_calc(Approach_V, a_app)  # Controllability ClaAh
x_ac_w_app = 0.24  # get from graph on slide  36 CONTRALABILITY
x_ac_bar_app = aerodynamic_center(
    x_ac_w_app, CLaAh_App, Approach_V, a_app
)  # USE graph to check how it changes

print(x_ac_bar_app)


def Cmac_calc():
    cm0_airfoil = -0.1  # fromt tables on page 79  page 115
    CL0 = (
        -0.205
    )  # lift coeff of flapped wing at zero alpha, dont know how to get it just a guess # lift slope of 5.89 and alpha 0 of 2deg
    CL = 2.053  # CL at landing (all flaps deployed)
    mu_2 = 0.7
    mu_1 = 0.2
    dCl_max = 0.679  # CL increase due to flap extension at landing condition
    c_dash_c = 1.171  # ratio between chord of the airfloil with extended flap and the chord in clean config
    # page 92 hamburg doc
    Swf = 42.178  # flapped wing area
    mu_3 = 0.0425

    Cm_ac_w = cm0_airfoil * (A * np.cos(sweep1_4) ** 2 / (A + 2 * np.cos(sweep1_4)))
    Cm_ac_fus = (
        -1.8
        * (1 - (2.5 * bf) / (lf))
        * (np.pi * bf * hf * lf)
        / (4 * S * c_bar)
        * CL0
        / CLaAh_App
    )

    Cm_ac_flaps_1_4 = mu_2 * (
        -mu_1 * dCl_max * c_dash_c
        - (CL + dCl_max * (1 - Swf / S)) * 1 / 8 * c_dash_c * (c_dash_c - 1)
    ) + 0.7 * A / (1 + (2 / A)) * mu_3 * dCl_max * np.tan(sweep1_4)
    Cm_ac_flaps = Cm_ac_flaps_1_4 - CL * (0.25 - x_ac_bar_app)
    Cm_ac_nac = 0.02  # from tu delft report

    Cmac = Cm_ac_w + Cm_ac_flaps + Cm_ac_fus + Cm_ac_nac
    return Cmac


Cmac = Cmac_calc()  # zero lift pitching moment coeff of the a/c without tail

CLh = -0.8  # horizontal tail lift coefficient
# -1 for full moving tail, -0.8 for adjustable tail, -0.35 * Ah**(1/3) for fixed tail

CLAh = (
    20800 * 9.81 / (0.5 * rho_app * Approach_V**2 * S)
)  # a/c lift coefficient without tail (can be approximated with wing CL at landing)

# Final Result


def Stab_Control():
    Control = np.zeros(len(x_cg_bar))
    Stability = np.zeros(len(x_cg_bar))
    Stability_wSM = np.zeros(len(x_cg_bar))

    for i in range(len(x_cg_bar)):
        Control[i] = 1 / ((CLh / CLAh) * (lh / c_bar) * Vh_V_2) * x_cg_bar[i] + (
            (Cmac / CLAh) - x_ac_bar_app
        ) / ((CLh / CLAh) * (lh / c_bar) * Vh_V_2)
        Stability[i] = 1 / (
            (CLah_Vcr / CLaAh_Vcr) * (1 - de_da_cr) * (lh / c_bar) * Vh_V_2
        ) * x_cg_bar[i] - (x_ac_bar_cr - SM) / (
            (CLah_Vcr / CLaAh_Vcr) * (1 - de_da_cr) * (lh / c_bar) * Vh_V_2
        )
        Stability_wSM[i] = 1 / (
            (CLah_Vcr / CLaAh_Vcr) * (1 - de_da_cr) * (lh / c_bar) * Vh_V_2
        ) * x_cg_bar[i] - (x_ac_bar_cr) / (
            (CLah_Vcr / CLaAh_Vcr) * (1 - de_da_cr) * (lh / c_bar) * Vh_V_2
        )

    return Control, Stability, Stability_wSM


# Parametrs for task


# Plotting
Control, Stability, Stability_wSM = Stab_Control()
plt.axhline(y=0, color="black")
plt.axvline(x=0, color="black")
plt.plot(x_cg_bar, Control, label="Control", linewidth=0.6)
plt.plot(
    x_cg_bar, Stability, label="Stability including SM", color="green", linewidth=0.6
)
plt.plot(
    x_cg_bar,
    Stability_wSM,
    label="Stability without SM",
    color="green",
    linestyle="--",
    linewidth=0.6,
)


plt.legend()
plt.xlabel("x_cg_bar")
plt.ylabel("Sh/S")
plt.title("Scissor plot of ATR 72-600")
plt.fill_between(x_cg_bar, Control, color="red", alpha=0.2)
plt.fill_between(x_cg_bar, Stability, color="red", alpha=0.2)
plt.ylim((0, 0.5))
plt.xlim((-1, 1))
plt.grid(True)

plt.show()
