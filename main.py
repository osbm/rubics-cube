import random
import numpy as np

class Pipes:
    top_left = "╔"
    top_right = "╗"
    bottom_left = "╚"
    bottom_right = "╝"
    horizontal = "═"
    vertical = "║"
    intersection = "╬"
    vertical_right = "╠"
    vertical_left = "╣"

class Cube:
    def __init__(self, size=3, scrambled=True, seed=42):
        self.size = size
        self.seed = seed
        self.console_colors = {
            "green": '\033[1;32m',
            "yellow": '\033[1;33m',
            "red": '\033[1;31m',
            'white': '\033[37m',
            "blue": '\033[1;34m',
            "orange": '\033[1;35m',
        }
        self.colors = ['g', 'y', 'r', 'w', 'b', 'o']
    
        self.combinations = self.generate_solved_cube(size)
        if scrambled:
            self.scramble()

    def is_solved(self):
        return self.combinations == self.generate_solved_cube(self.size)

    def generate_solved_cube(self, size):
        combinations = []
        for i in range(6):
            combinations.append([*self.colors[i] * (size **2)])
        return combinations

    def scramble(self):
        random.seed(self.seed)
        raise NotImplementedError

    def binary_search(self):
        raise NotImplementedError

    def make_move(self, move):
        raise NotImplementedError

    def get_possible_moves(self):
        raise NotImplementederror

    def __str__(self):
        
        # draw top pipes of the top face of cube
        print(" "*(self.size*2+1), end='')
        print(Pipes.top_left, end='')
        print(Pipes.horizontal * (self.size*2), end='')
        print(Pipes.top_right)

        for i in range(self.size):
            print(" "*(self.size*2+1), end='')
            print(Pipes.vertical, end='')
            for j in range(self.size):
                print((self.combinations[0][i*self.size+j])*2, end='')
            print(Pipes.vertical)

        # draw 3 faces of cube next to each other
        print(Pipes.top_left, end='')
        print(Pipes.horizontal * (self.size*2), end='')
        print(Pipes.intersection, end='')
        print(Pipes.horizontal * (self.size*2), end='')
        print(Pipes.intersection, end='')
        print(Pipes.horizontal * (self.size*2), end='')
        print(Pipes.top_right)

        for i in range(self.size):
            print(Pipes.vertical, end='')
            for j in range(self.size):
                print((self.combinations[1][i*self.size+j])*2, end='')
                
            print(Pipes.vertical, end='')
            for j in range(self.size):
                print((self.combinations[2][i*self.size+j])*2, end='')
                
            print(Pipes.vertical, end='')
            for j in range(self.size):
                print((self.combinations[3][i*self.size+j])*2, end='')
                
            print(Pipes.vertical)

        print(Pipes.bottom_left, end='')
        print(Pipes.horizontal * (self.size*2), end='')
        print(Pipes.intersection, end='')
        print(Pipes.horizontal * (self.size*2), end='')
        print(Pipes.intersection, end='')
        print(Pipes.horizontal * (self.size*2), end='')
        print(Pipes.bottom_right)

        for i in range(self.size):
            print(" "*(self.size*2+1), end='')
            print(Pipes.vertical, end='')
            for j in range(self.size):
                print((self.combinations[4][i*self.size+j])*2, end='')
            print(Pipes.vertical)

        print(" "*(self.size*2+1), end='')
        print(Pipes.vertical_right, end='')
        print(Pipes.horizontal * (self.size*2), end='')
        print(Pipes.vertical_left)
        for i in range(self.size):
            print(" "*(self.size*2+1), end='')
            print(Pipes.vertical, end='')
            for j in range(self.size):
                print((self.combinations[5][i*self.size+j])*2, end='')
            print(Pipes.vertical)

        print(" "*(self.size*2+1), end='')
        print(Pipes.bottom_left, end='')
        print(Pipes.horizontal * (self.size*2), end='')
        print(Pipes.bottom_right)

        return ""
        

if __name__ == '__main__':
    cube = Cube(size=10, scrambled=False)
    print(cube)
    import pprint
    #pprint.pprint(cube.combinations)