# Code structure

## Classes

All files in the code contain a single class. This class always has the same layout. This layout is already implemented. If you are unsure about how to use classes, please go to the bottom of this document, if you are still unclear, ask me. An example is shown below:

class ExampleName:

    def __init__(inputs: dict[str, float]) -> None:
        ...

    # ~~~ Intermediate Functions ~~~

    def example_function(self):
        '''
        This is an example intermediate function
        '''
        return True

    # ~~~ Output functions ~~~ 

    def get_something(self):
        ''' This outputs something specific '''
        return something

    def get_all(self):
        ''' This returns all outputs '''

        updated_inputs = something
        return updated_inputs

Note that all output functions should start with get_... so that they are consistent and easy to use, you can have a get_specific_output or get_all, which would execute all the updates/functions

## Inputs and outputs

All classes only take a single input, the inputs dictionary which is defined in inputs.py. If you need to add any inputs you need to do so here. When initially coding, please use funny_inputs, this way, the original inputs don't get adjusted unless with the knowledge of the group. Once you are done, you can tell the group you are adjusting the inputs, the way to do this should be clear from the layout of the file. 

All output functions should return an updated version of the inputs dictionary, which then can be fed into another class or function. 

## Testing
There are three pytest files set up in DetailedDesign. One for unit tests, one for subsystem tests and one for system tests. Not that all test functions should begin with the word test, as otherwise pytest will not recognise them, and that would be sad.

If you want to set up pytest, either click the chemistry bottle at the left size of the screen, or do cntrl + shift + P and click Python:Configure Tests. Select Pytest and the DetailedDesign.

## __main__
There is a file called __main__.py, this is the part where the final code is executed. The naming convention means that if you type 'python DetailedDesign' in your terminal, it executes this file. There should be no functions in this file, only function calls.

## plots
I assume we're going to be making plots at some point, if you do, instead of calling plt.show(), call plt.savefig(DetailedDesign\plots\myplotname.png), this will save the plot into the plots folder, and saves you from having to run the code each time you need to look at it.

# General Rules

1. PLEASE USE TYPE CHECKING AND DOCSTRINGS THE CODE WILL BE AN UNREADABLE SPAGHETTI. All functions should look like this:

def my_function(var1: int, var2: list[float]) -> float:
    '''This is a docstring explaining what your function does'''
    return something

2. Only change the inputs file after communicating with the group as other people might be using it. If you want to try things out, use funny_inputs. When adding any inputs, add a comment with the description and unit. 

3. All code should be verified. You can verify your code in two ways, the first is to use the test files in the test folder, these use pytest (how you layout a test is in the files), or you can do sanity checks at the bottom of you file within your if __name__ == '__main__' statement. Ideally do both. 

4. It is usually better to have longer clear variable names over shorter ones. Also, generally use snake case, except with class names. 

5. All inputs that are not integers should be inputted as a floats. So not '5' but '5.0' or '5.'

# Classes explanation

The code for this is in Class example.py, feel free to mess with that to try things out

A class looks like this

class Square:
    def __init__(self, side: int, colour: str):         Your inputs go here
        self.side = side                                Here you turn your inputs into attributes
        self.colour = colour

    def print_side(self):                               You can then put a function in your class
        print(self.side)                                Don't forget to use self!

    def print_side_and_message(self, mess: str):        You can also have an input in that function
        print(self.side, mess)

    def update_with_diameter(self, diameter: int):
        self.side = (0.5*diameter**2)**0.5

You can then create an instance like this:

sqA = Square(4, 'blue')

You can change the attributes like this:

sqA.side = 5

Now if you would call

sqA.print_side()

It would print 5 instead of 4

There are a bunch more funny things you can do but this is the basics. With the update_with_diameter one you can kind of see how you can do internal updates. If you have any questions hmu






