'''
This is the file for the aerodynamics subsystem. It contains a single class.
'''

class Aerodynamics:

    def __init__(self, inputs: dict[str, float]) -> None:
        self.inputs = inputs
        self.outputs = self.inputs.copy()

    # ~~~ Intermediate Functions ~~~

    def example_function(self):
        '''
        This is an example intermediate function
        '''
        return True

    # ~~~ Output functions ~~~ 

    def get_all(self) -> dict[str, float]:

        # These are all the required outputs for this class. Plz consult the rest if removing any of them!

        outputs["CL_cruise"] = ...
        outputs["CD_cruise"] = ...
        outputs["CL_max"] = ...
        outputs["CD_max"] = ...

        outputs["Wing_area"] = ...
        outputs["Wing_span"] = ...
        outputs["Wing_aspect_ratio"] = ...
        outputs["Wing_taper_ratio"] = ...
        outputs["Wing_chord"] = ...
        #outputs["Wing_sweep"] = ...

        # potentially something about coefficients for control 
        # something about aerodynamic force during deployment for control



        return self.outputs
    
if __name__ == '__main__':
    # Perform sanity checks here
    ...