'''
This is the file for the deployment subsystem. It contains a single class.
'''

class Deployment:

    def __init__(self, inputs: dict[str, float]) -> None:
        self.aerogel_mass = 5

    # ~~~ Intermediate Functions ~~~

    def example_function(self):
        '''
        This is an example intermediate function
        '''
        return True

    # ~~~ Output functions ~~~ 

    def get_all(self) -> dict[str, float]:

        updated_inputs = True
        return updated_inputs
    
if __name__ == '__main__':
    # Perform sanity checks here
    ...