import numpy as np
from .cube import Cube
from typing import Callable

def same_color_amount(combinations: np.array) -> int:
    """Sum of the largest amount of same colors on a face.
    On a 5x5x5 cube largest possible amount is 6*5*5 = 150.
    *bigger the better*

    Args:
        combinations (np.array): A combination of a cube. shape: (6, n, n)

    Returns:
        int: Value of the heuristic.
    """
    
    # check if the colors are the same on the same face
    same_color_amount = 0
    for face in combinations:
        value_counts = np.unique(face, return_counts=True)[1]
        same_color_amount += np.max(value_counts)

    # but we need a function that returns a smaller value for a better solution
    # so we subtract the value from the maximum possible value
    max_possible_value = 6*combinations.shape[1]*combinations.shape[2]
    return max_possible_value - same_color_amount



class AStarSolver():
    def __init__(self, cube: Cube, heuristic: Callable):
        """Initialize the solver.

        Args:
            combinations (np.array): A combination of a cube.
        """
        self.cube = cube
        self.heuristic = heuristic
        self.possible_moves = cube.get_possible_moves() # possible moves are constant

        # lets remove rotational moves from the possible moves
        self.possible_moves = [move for move in self.possible_moves if not (("x" in move) or ("y" in move) or ("z" in move))]
    
    def make_str(self, combinations: np.array) -> str:
        """Make a string from the combinations.

        Args:
            combinations (np.array): A combination of a cube.

        Returns:
            str: The string.
        """
        return "".join(["".join(x_row) for face in combinations for x_row in face])


    def solve(self) -> str:
        """Solve the cube.

        Returns:
            str: The solution.
        """
        if self.cube.is_solved():
            print("Cube is already solved!")
            return ""

        # current combinations of the cube
        initial_combinations = self.cube.combinations.copy()

        visited = [str(initial_combinations)]
        queue = [(initial_combinations, (), self.heuristic(initial_combinations))]
        # queue elements in the form of (combinations, path, value)

        print("current best cube value: ", queue[0][2])


        while queue:
            # sort the queue by the value of the elements
            
            queue = sorted(queue, key=lambda x: len(x[1])+ x[2]) # length of the path + evaluation value

            # get the element with the lowest value
            combinations, path, value = queue.pop(0)

            # check if the cube is solved
            new_cube = Cube.from_combinations(combinations)

            if new_cube.is_solved():
                return path

            for move in self.possible_moves:
                child_cube = Cube.from_combinations(combinations.copy())
                child_cube.make_move(move)
                new_combinations = child_cube.combinations
                # check if the new combinations are already visited
                if str(new_combinations) not in visited:
                    visited.append(str(new_combinations))
                    queue_element = (new_combinations.copy(), (*path, move), self.heuristic(new_combinations))
                    queue.append(queue_element)
                    
                    if child_cube.is_solved():
                        return queue_element[1]

        raise ValueError("Invalid cube!")

