class Square:
    def __init__(self, side: int, colour: str):         
        self.side = side                   
        self.colour = colour

    def print_side(self):
        print('The side has length:', self.side)

    def print_side_and_message(self, mess: str) -> None:        
        print(self.side, mess)

    def update_with_diameter(self, diameter: int) -> None:
        self.side = (0.5*diameter**2)**0.5


if __name__ == '__main__':
    sqA = Square(4, 'Blue')
    sqB = Square(7, 'Red')

    sqA.print_side()
    sqB.print_side()

    sqA.side = 5

    sqA.print_side()

    sqA.print_side_and_message('Hello World')

    sqA.update_with_diameter(5)
    print(sqA.side)