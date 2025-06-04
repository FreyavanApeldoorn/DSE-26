'''
This is the file for the aerodynamics subsystem. It contains a single class.
'''

class Aerodynamics:

    def __init__(self, inputs: dict[str, float]) -> None:
        self.inputs = inputs
        self.outputs = self.inputs.copy()

        #Wing Parameters
        self.aspect_ratio = inputs["aspect_ratio"]  # Wing aspect ratio 
        self.wing_area = inputs["wing_area"]  # Wing area in m^2 
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



    # ~~~ Intermediate Functions ~~~

    def calculate_wing_parameters(self) -> dict[str, float]:
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
        self.vertical_tail_aspect_ratio = self.aspect_ratio * self.vertical_tail_aspect_ratio # Assuming hald the aspect ratio for vertical tail
        self.vertical_tail_span = (self.vertical_tail_area * self.vertical_tail_aspect_ratio) ** 0.5
        self.vertical_tail_chord = self.vertical_tail_area / self.vertical_tail_span  # Vertical tail chord in m
        self.vertical_tail_root_chord = (2 * self.vertical_tail_chord) / (1 + self.taper_ratio_vertical_tail)  # Root chord length for vertical tail m
        self.vertical_tail_tip_chord = self.taper_ratio_vertical_tail * self.vertical_tail_root_chord  # Tip chord length for vertical tail m
        self.vertical_tail_MAC = (2 / 3) * self.vertical_tail_root_chord * ((1 + self.taper_ratio_vertical_tail + self.taper_ratio_vertical_tail**2) / (1 + self.taper_ratio_vertical_tail))  # Mean Aerodynamic Chord for vertical tail m


    # ~~~ Output functions ~~~ 

    def get_all(self) -> dict[str, float]:

        # These are all the required outputs for this class. Plz consult the rest if removing any of them!

        #outputs["CL_cruise"] = ...
        #outputs["CD_cruise"] = ...
        #outputs["CL_max"] = ...
        #outputs["CD_max"] = ...
        
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
        self.outptuts["horizontal_tail_area"] = self.horizontal_tail_area
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
    # Perform sanity checks here
    ...