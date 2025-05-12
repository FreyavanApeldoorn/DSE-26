*** Freya is a mean person and wants you to follow certain rules for the coding ***

1. Try to work within either functions or classes as much as possible. If you don't know how classes work don't worry I can help / just leave it. At the bottom of each file you should have:

if __name__ = '__main__':
    blablabla

Which should execute your functions.

2. PLEASE USE TYPE CHECKING AND DOCSTRINGS THE CODE WILL BE AN UNREADABLE SPAGHETTI. All functions should look like this:

def my_function(var1: int, var2: list[float]) -> float:
    '''This is a docstring explaining what your function does'''
    return something

3. FREYA'S CLASSES MASTERCLASS

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
