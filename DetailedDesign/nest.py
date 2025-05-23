'''
This is the file for the nest. It contains a single class.
'''

class Nest:

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

        return self.outputs
    
if __name__ == '__main__':
    # Perform sanity checks here
    ...