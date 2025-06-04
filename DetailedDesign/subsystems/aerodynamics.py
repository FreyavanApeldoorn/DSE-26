'''
This is the file for the aerodynamics subsystem. It contains a single class.
'''
import numpy as np
import matplotlib.pyplot as plt
import sys
import os

# Add the project root to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

class Aerodynamics:

    def __init__(self, inputs: dict[str, float]) -> None:
        self.inputs = inputs
        self.outputs = self.inputs.copy()

        #Wing Parameters
        self.maximum_takeoff_weight = inputs["MTOW"]
        self.aspect_ratio = inputs["AR"]  # Wing aspect ratio 
        self.taper_ratio = inputs["taper_ratio"]  # Wing taper ratio
        self.sweep_angle = inputs["sweep_angle"] # Sweep angle of the wing in degrees
        self.thickness_to_chord_ratio = inputs["thickness_to_chord_ratio"]  # Thickness to chord ratio for the wing max
        self.span_position = inputs["span_position"]  # Span position of interest main wing 

        #Horizontal Tail Parameters
        self.horizontal_tail_length = inputs["tail_length"]  # Length betweem ac tail horizontal and wing ac in m
        self.horizontal_tail_coefficient = inputs["horizontal_tail_coefficient"]  # Coefficient for horizontal tail area calculation
        self.taper_ratio_horizontal_tail = inputs["taper_ratio_horizontal_tail"]  # Taper ratio for horizontal tail
        self.sweep_angle_horizontal_tail = inputs["sweep_angle_horizontal_tail"]  # Sweep angle of the horizontal tail in degrees
        self.relative_horizontal_tail_aspect_ratio = inputs["relative_horizontal_tail_aspect_ratio"]  # Relative aspect ratio of the horizontal tail to the wing

        #Vertical Tail Parameters
        self.vertical_tail_length = inputs["vertical_tail_length"]  # Length betweem ac tail vertical and wing ac in m
        self.vertical_tail_coefficient = inputs["vertical_tail_coefficient"] # Coefficient for vertical tail area calculation
        self.taper_ratio_vertical_tail = inputs["taper_ratio_vertical_tail"]  # Taper ratio for vertical tail
        self.sweep_angle_vertical_tail = inputs["sweep_angle_vertical_tail"]  # Sweep angle of the vertical tail in degrees
        self.relative_vertical_tail_aspect_ratio = inputs["relative_vertical_tail_aspect_ratio"]  # Relative aspect ratio of the vertical tail to the wing

        #Gust inputs

        # manoeuvre inputs
        self.max_load_factor = inputs["max_load_factor"]  # Maximum load factor for maneuvering
        self.min_load_factor = inputs["min_load_factor"]  # Minimum load factor for maneuvering
        self.density_sea = inputs["rho_0"]  # Air density in kg/m^3
        self.density_3000 = inputs["rho_service"]  # Air density at 3000m in kg/m^3
        self.CL_max = inputs["CL_max"]  # Maximum lift coefficient
        self.wing_loading = inputs["wing_loading"]  # Wing loading in N/m^2
        self.cruise_velocity = inputs["V_cruise"]  # Cruise velocity in m/s


    # ~~~ Intermediate Functions ~~~

    def calculate_wing_parameters(self) -> dict[str, float]:
        self.wing_area = self.maximum_takeoff_weight / self.wing_loading  
        self.wing_span = (self.wing_area * self.aspect_ratio) ** 0.5  # Wing span in m
        self.wing_chord = self.wing_area / self.wing_span
        self.wing_root_chord = (2 * self.wing_chord) / (1 + self.taper_ratio) # Root chord length
        self.wing_tip_chord = self.taper_ratio * self.wing_root_chord
        self.MAC = (2 / 3) * self.wing_root_chord * ((1 + self.taper_ratio + self.taper_ratio**2) / (1 + self.taper_ratio))
        self.chord_percent_span = self.wing_root_chord - (((self.wing_root_chord - self.wing_tip_chord)/(self.wing_span * 0.5)) * self.wing_span * self.span_position)  # Chord length at a specific span position
        self.thickness_percent_span = self.thickness_to_chord_ratio * self.chord_percent_span # Thickness at % span
    
    def calculate_horizontal_tail_parameters(self) -> dict[str, float]:
        self.horizontal_tail_area = (self.horizontal_tail_coefficient * self.wing_area * self.wing_chord)/self.horizontal_tail_length  # Horizontal tail area in m^2
        self.horizontal_tail_aspect_ratio = self.aspect_ratio * self.relative_horizontal_tail_aspect_ratio  
        self.horizontal_tail_span = (self.horizontal_tail_area * self.horizontal_tail_aspect_ratio ) ** 0.5  # Horizontal tail span in m # Assuming half the aspect ratio for horizontal tail
        self.horizontal_tail_chord = self.horizontal_tail_area / self.horizontal_tail_span  # Horizontal tail chord in m
        self.horizontal_tail_root_chord = (2 * self.horizontal_tail_chord) / (1 + self.taper_ratio_horizontal_tail)  # Root chord length for horizontal tail m
        self.horizontal_tail_tip_chord = self.taper_ratio_horizontal_tail * self.horizontal_tail_root_chord  # Tip chord length for horizontal tail m
        self.horizontal_tail_MAC = (2 / 3) * self.horizontal_tail_root_chord * ((1 + self.taper_ratio_horizontal_tail + self.taper_ratio_horizontal_tail**2) / (1 + self.taper_ratio_horizontal_tail))  # Mean Aerodynamic Chord for horizontal tail m
    
    def calculate_vertical_tail_parameters(self) -> dict[str, float]:
        self.vertical_tail_area = (self.vertical_tail_coefficient * self.wing_area * self.wing_span)/self.vertical_tail_length
        self.vertical_tail_aspect_ratio = self.aspect_ratio * self.relative_vertical_tail_aspect_ratio # Assuming hald the aspect ratio for vertical tail
        self.vertical_tail_span = (self.vertical_tail_area * self.vertical_tail_aspect_ratio) ** 0.5
        self.vertical_tail_chord = self.vertical_tail_area / self.vertical_tail_span  # Vertical tail chord in m
        self.vertical_tail_root_chord = (2 * self.vertical_tail_chord) / (1 + self.taper_ratio_vertical_tail)  # Root chord length for vertical tail m
        self.vertical_tail_tip_chord = self.taper_ratio_vertical_tail * self.vertical_tail_root_chord  # Tip chord length for vertical tail m
        self.vertical_tail_MAC = (2 / 3) * self.vertical_tail_root_chord * ((1 + self.taper_ratio_vertical_tail + self.taper_ratio_vertical_tail**2) / (1 + self.taper_ratio_vertical_tail))  # Mean Aerodynamic Chord for vertical tail m

    def gust_diagram(self) -> dict[str, float]:

        raise NotImplementedError("Gust diagram calculation is not implemented yet.")
    
    def manoeuvre_diagram(self, dive_factor) -> dict[str, float]:
        dive_velocity = self.cruise_velocity * dive_factor
        total_velocity_range = np.arange(0, dive_velocity, 0.1)

        n_0A_sea = (0.5 * self.density_sea * total_velocity_range **2 * self.CL_max)/ self.wing_loading  # Load factor for maneuvering
        n_0A_3000 = (0.5 * self.density_3000 * total_velocity_range **2 * self.CL_max)/ self.wing_loading  # Load factor for maneuvering at 3000m

        n_0H_sea = -1 * (0.5 * self.density_sea * total_velocity_range **2 * self.CL_max)/ self.wing_loading
        n_0H_3000 = -1 * (0.5 * self.density_3000 * total_velocity_range **2 * self.CL_max)/ self.wing_loading

        # Find where n_0A_sea crosses max_load_factor
        idx_max_sea = np.argmax(n_0A_sea >= self.max_load_factor)
        v_max_sea = total_velocity_range[idx_max_sea] if np.any(n_0A_sea >= self.max_load_factor) else dive_velocity

        idx_max_3000 = np.argmax(n_0A_3000 >= self.max_load_factor)
        v_max_3000 = total_velocity_range[idx_max_3000] if np.any(n_0A_3000 >= self.max_load_factor) else dive_velocity

        # Find where n_0H_sea crosses min_load_factor
        idx_min_sea = np.argmax(n_0H_sea <= self.min_load_factor)
        v_min_sea = total_velocity_range[idx_min_sea] if np.any(n_0H_sea <= self.min_load_factor) else dive_velocity

        idx_min_3000 = np.argmax(n_0H_3000 <= self.min_load_factor)
        v_min_3000 = total_velocity_range[idx_min_3000] if np.any(n_0H_3000 <= self.min_load_factor) else dive_velocity

        plt.figure(figsize=(10, 6))
        # Plot only up to intersection points
        plt.plot(total_velocity_range[:idx_max_sea+1], n_0A_sea[:idx_max_sea+1], label='Load Factor vs Velocity (Sea)')
        plt.plot(total_velocity_range[:idx_max_3000+1], n_0A_3000[:idx_max_3000+1], label='Load Factor vs Velocity at 3000m')

        plt.plot(total_velocity_range[:idx_min_sea+1], n_0H_sea[:idx_min_sea+1], label='Negative Load Factor vs Velocity (Sea)')
        plt.plot(total_velocity_range[:idx_min_3000+1], n_0H_3000[:idx_min_3000+1], label='Negative Load Factor vs Velocity at 3000m')

        plt.plot(total_velocity_range, self.max_load_factor * np.ones_like(total_velocity_range), 'r--', label='Max Load Factor')
        plt.plot(total_velocity_range, self.min_load_factor * np.ones_like(total_velocity_range), 'g--', label='Min Load Factor')

        plt.axvline(x=dive_velocity, color='k', linestyle='--', label='Dive Velocity')
        plt.title('manoeuvre Diagram')
        plt.xlabel('Velocity (m/s)')
        plt.ylabel('Load Factor (n)')
        plt.xlim(0, dive_velocity * 1.1)
        plt.ylim(-self.max_load_factor * 1.3, self.max_load_factor * 1.3)
        plt.grid(True)
        plt.legend()
        plt.show()

    # ~~~ Output functions ~~~ 

    def get_all(self) -> dict[str, float]:

        self.calculate_wing_parameters()
        self.calculate_horizontal_tail_parameters()
        self.calculate_vertical_tail_parameters()

        self.outputs["Wing_area"] = self.wing_area
        self.outputs["Wing_span"] = self.wing_span
        self.outputs["Wing_aspect_ratio"] = self.aspect_ratio
        self.outputs["Wing_taper_ratio"] = self.taper_ratio
        self.outputs["Wing_chord"] = self.wing_chord
        self.outputs["Wing_sweep"] = self.sweep_angle
        self.outputs["Wing_root_chord"] = self.wing_root_chord
        self.outputs["Wing_tip_chord"] = self.wing_tip_chord
        self.outputs["Wing_MAC"] = self.MAC

        self.outputs["horizontal_tail_length"] = self.horizontal_tail_length
        self.outputs["horizontal_tail_area"] = self.horizontal_tail_area
        self.outputs["horizontal_tail_span"] = self.horizontal_tail_span
        self.outputs["horizontal_tail_chord"] = self.horizontal_tail_chord
        self.outputs["horizontal_tail_root_chord"] = self.horizontal_tail_root_chord
        self.outputs["horizontal_tail_tip_chord"] = self.horizontal_tail_tip_chord
        self.outputs["horizontal_tail_MAC"] = self.horizontal_tail_MAC
        self.outputs["horizontal_tail_aspect_ratio"] = self.horizontal_tail_aspect_ratio
        self.outputs["horizontal_tail_sweep"] = self.sweep_angle_horizontal_tail
        self.outputs["horizontal_tail_taper_ratio"] = self.taper_ratio_horizontal_tail

        self.outputs["vertical_tail_length"] = self.vertical_tail_length
        self.outputs["vertical_tail_area"] = self.vertical_tail_area
        self.outputs["vertical_tail_span"] = self.vertical_tail_span
        self.outputs["vertical_tail_chord"] = self.vertical_tail_chord
        self.outputs["vertical_tail_root_chord"] = self.vertical_tail_root_chord
        self.outputs["vertical_tail_tip_chord"] = self.vertical_tail_tip_chord
        self.outputs["vertical_tail_MAC"] = self.vertical_tail_MAC
        self.outputs["vertical_tail_aspect_ratio"] = self.vertical_tail_aspect_ratio
        self.outputs["vertical_tail_sweep"] = self.sweep_angle_vertical_tail
        self.outputs["vertical_tail_taper_ratio"] = self.taper_ratio_vertical_tail


        # potentially something about coefficients for control 
        # something about aerodynamic force during deployment for control

        return self.outputs
    
if __name__ == '__main__':
    from DetailedDesign.funny_inputs import aerodynamics_funny_inputs
    aerodynamics = Aerodynamics(aerodynamics_funny_inputs)
    aerodynamics.manoeuvre_diagram(1.4) # Example dive factor
    # Perform sanity checks here
    ...