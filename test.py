from PreliminaryDesign.electric_propulsion_mass_sizing import PropMass

Prop_Mass = PropMass(
    P_max_cruise=1400,
    P_max_vtol=5500,
    U_max=25.5,
    F1=0.889,
    E1=-0.288,
    E2=0.1588,
    f_install_cruise=1.0,
    f_install_vtol=1.0,
    n_mot_cruise=1,
    n_mot_vtol=4,
    K_material=1.0,
    n_props_cruise=2,
    n_props_vtol=2,
    n_blades_cruise=3,
    n_blades_vtol=3,
    D_prop_vtol=1.0,
    K_p=1,
)

motor_mass_cruise, _, motor_mass_vtol, _ = Prop_Mass.calculate_motor_mass()
print("Motor Mass Cruise: ", motor_mass_cruise)
print("Motor Mass VTOL: ", motor_mass_vtol)
