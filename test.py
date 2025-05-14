from PreliminaryDesign.electric_propulsion_mass_sizing import PropMass

Prop_Mass = PropMass(
    P_max_cruise=1400,
    P_max_vtol=1400,
    U_max=25.5,
    F1=0.889,
    E1=-0.288,
    E2=0.1588,
    f_install_cruise=1.0,
    f_install_vtol=1.0,
    n_mot_cruise=1,
    n_mot_vtol=1,
    K_material=1.0,
    n_props_cruise=1,
    n_props_vtol=1,
    n_blades_cruise=4,
    n_blades_vtol=4,
    D_prop_vtol=1.0,
    K_p=1,
)

motor_mass_cruise, _, motor_mass_vtol, _ = Prop_Mass.calculate_motor_mass()
print("Motor Mass Cruise: ", motor_mass_cruise)
print("Motor Mass VTOL: ", motor_mass_vtol)

# Calculate ESC mass
esc_mass_cruise, _, esc_mass_vtol, _ = Prop_Mass.calculate_esc_mass()
print("ESC Mass Cruise: ", esc_mass_cruise)
print("ESC Mass VTOL: ", esc_mass_vtol)

# Calculate propeller mass
propeller_mass_cruise, _, propeller_mass_vtol, _ = Prop_Mass.calculate_propeller_mass()
print("Propeller Mass Cruise: ", propeller_mass_cruise)
print("Propeller Mass VTOL: ", propeller_mass_vtol)

# Calculate propulsion mass
M_FW_Prop, M_Vtol_Prop = Prop_Mass.calculate_propulsion_mass()
print("Propulsion Mass Forward: ", M_FW_Prop)
print("Propulsion Mass VTOL: ", M_Vtol_Prop)
