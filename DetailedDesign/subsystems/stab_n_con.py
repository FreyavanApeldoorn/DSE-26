'''
This is the file for stability and control subsystem. It contains a single class.
'''

class StabCon:

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

        outputs["Power_required"] = ... # New requirement for power in order to get the right control authority

        outputs["Propeller_arm_length"] = ...
        outputs["Tail_arm"] = ...
        outputs["Tail_area"] = ...


        outputs["CG_x_max"] = ...
        outputs["CG_y_max"] = ...
        outputs["CG_x_min"] = ...
        outputs["CG_y_min"] = ...

        # something about control surfaces


        return self.outputs
    
if __name__ == '__main__': # pragma: no cover
    # Perform sanity checks here
    ...