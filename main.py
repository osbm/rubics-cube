import random
import numpy as np
class Cube:
    def __init__(self, size=3, scrambled=True, seed=42):
        self.size = size
        self.seed = seed

        self.colors = ['w', 'r', 'b', 'g', 'o', 'y']
    
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
        raise NotImplementedError

if __name__ == '__main__':
    cube = Cube(size=5, scrambled=False)
    cube.is_solved()
    import pprint
    pprint.pprint(cube.combinations)