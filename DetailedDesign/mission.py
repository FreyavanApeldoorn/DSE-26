'''
This is the file for the mission. It contains a single class.
'''

class Mission:

    def __init__(self, inputs: dict[str, float]) -> None:
        self.inputs = inputs
        self.outputs = self.inputs.copy()

    # ~~~ Intermediate Functions ~~~
    

    def time_preparation(self) -> float:
        pass


    def time_operation(self) -> float:
        pass


    def time_wrapup(self) -> float:
        pass


    def total_mission_time(self) -> float:

        
        return self.time_preparation + time_operation + time_wrapup

    # ~~~ Output functions ~~~ 

    def get_all(self) -> dict[str, float]:



        self.inputs["total_mission_time"] = self.total_mission_time

        updated_inputs = True
        return updated_inputs
    

if __name__ == '__main__':
    # Perform sanity checks here
    ...