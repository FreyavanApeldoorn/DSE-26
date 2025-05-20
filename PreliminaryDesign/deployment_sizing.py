
class SizeDeployment:

    def __init__(self, inputs: dict[str, float | int], verbose: bool = False):
        
        self.inputs = inputs

    def size_deployment(self):

        self.inputs["deployment_mass"] = 2.31   # kg
        self.inputs["deployment_cable_specific_mass"]  = 0.027 # kg/m
        self.inputs["deployment_cable_length"] = 15 # m
        self.inputs["deployment_speed"] = 0.3 # m/s
        self.inputs["deployment_time"] = 2.5*60 # s
        self.inputs["deployment_accuracy"] = 1.5 # m (uncertainty of the deployment)  