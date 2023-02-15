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
    horizontal_top = "╦"
    horizontal_bottom = "╩"


class Cube:
    def __init__(
        self,
        size=3,
        scrambled=False,
        seed=42,
        show_letter=True,
        add_reverse_and_double_moves=False,
    ):
        self.size = size
        self.seed = seed
        self.show_letter = show_letter
        # self.add_reverse_and_double_moves = add_reverse_and_double_moves TODO
        self.console_colors = {
            "g": "\033[1;32m",
            "y": "\033[1;33m",
            "r": "\033[1;31m",
            # 'w': '\033[37m',
            "w": "\033[38;5;255m",
            "b": "\033[1;34m",
            "o": "\033[38;5;214m",
            # now a debug color
            "x": "\033[38;5;255m",
            "reset": "\033[0m",
        }
        self.colors = ["w", "o", "g", "r", "b", "y"]
        self.face_to_index = {
            "U": 0,
            "L": 1,
            "F": 2,
            "R": 3,
            "B": 4,
            "D": 5,
        }
        self.faces = self.face_to_index.keys()
        self.combinations = self.generate_solved_cube(size)
        if scrambled:
            self.scramble()

    def is_solved(self):
        for face_index in range(6):
            first_color = self.combinations[face_index][0]
            for i in range(self.size):
                for j in range(self.size):
                    if self.combinations[face_index][i * self.size + j] != first_color:
                        return False
        return True

    def generate_solved_cube(self, size):
        combinations = []
        for i in range(6):
            combinations.append([*self.colors[i] * (size**2)])

        # lets put an x to the first element of each face so we can easily see the rotation
        for i in range(6):
            combinations[i][0] = "x"
        return np.array(combinations)

    def make_move(self, move: str):
        # see if move is valid
        if move not in self.get_possible_moves():
            raise ValueError("Invalid move")

        if move[-1] == "'":
            self.make_move(move[:-1])
            self.make_move(move[:-1])
            self.make_move(move[:-1])
        elif move[-1] == "2":
            self.make_move(move[:-1])
            self.make_move(move[:-1])

        # first lets deal with the rotational moves
        if move in self.faces:
            self._rotate_face(move, -1)
            # also we should rotate the slice
            if move == "F":
                ...

        elif move == "y":
            self._rotate_face(0, 0)

    def _rotate_face(self, face: str, direction: int):
        """
        Rotate a face of the cube

        Arguments:
            face: can be F, R, U, L, B, D
            direction: 1 for clockwise, -1 for counter clockwise
        """
        # print(self.combinations.shape)
        face_idx = self.face_to_index[face]
        face = self.combinations[face_idx]
        # lets use numpy to rotate the face 90 degrees
        rotated_face = np.rot90(face.reshape(self.size, self.size), direction)
        self.combinations[face_idx] = rotated_face.reshape(self.size**2)

        
        

    def get_possible_moves(self):
        # get moves that are possible for any sized cube
        # i am going to implement my own notation to work with higher sized cubes
        # but for 3x3x3 cube, it will be the same as rubiks cube notation
        # there wont be any way to turn more than 1 slice at a time
        # https://ruwix.com/the-rubiks-cube/notation/

        # actually, reverse and double moves is kinda redundant

        rotational_moves = [*"xyz", "x'", "y'", "z'"]
        face_moves = [*"UDFBRL"]
        face_moves.extend([move + "2" for move in face_moves])
        face_moves.extend([move + "'" for move in face_moves])

        # m1F means we will be rotating the slice of the cube that 1 layer away from the front face
        # m1R means we will be rotating the slice of the cube that 1 layer away from the right face
        # for a 3x3x3 cube, the 3 slices are m1F, m1R, and m1U

        # for a 4x4x4 cube, the 4 slices are m1F, m2F, m1R, m2R, m1U, m2U
        middle_layer_moves = []
        for i in range(1, self.size - 1):
            for face in ["F", "R", "U"]:
                move = f"m{i}{face}"
                middle_layer_moves.extend(
                    [move, move + "'", move + "2"]
                )  # move, move reverse, move double

        return [
            *rotational_moves,
            *face_moves,
            *middle_layer_moves,
        ]

    def _print_letter(self, letter: str):
        color = self.console_colors[letter]
        print(color, end="")

        if self.show_letter:
            print(letter * 2, end="")
        else:
            print("██", end="")

        print(self.console_colors["reset"], end="")

    def print(self):
        # draw top pipes of the top face of cube
        print(
            " " * (self.size * 2 + 1),
            Pipes.top_left,
            Pipes.horizontal,
            "U",
            Pipes.horizontal * (self.size * 2 - 2),
            Pipes.top_right,
            sep="",
        )

        for i in range(self.size):
            print(" " * (self.size * 2 + 1), end="")
            print(Pipes.vertical, end="")
            for j in range(self.size):
                self._print_letter(self.combinations[0][i * self.size + j])
            print(Pipes.vertical)

        # draw 3 faces of cube next to each other
        print(
            Pipes.top_left,
            Pipes.horizontal,
            "L",
            Pipes.horizontal * (self.size * 2 - 2),
            Pipes.intersection,
            Pipes.horizontal,
            "F",
            Pipes.horizontal * (self.size * 2 - 2),
            Pipes.intersection,
            Pipes.horizontal,
            "R",
            Pipes.horizontal * (self.size * 2 - 2),
            Pipes.horizontal_top,
            Pipes.horizontal,
            "B",
            Pipes.horizontal * (self.size * 2 - 2),
            Pipes.top_right,
            sep="",
        )

        for i in range(self.size):
            for j in range(1, 5):
                print(Pipes.vertical, end="")
                for k in range(self.size):
                    self._print_letter(self.combinations[j][i * self.size + k])


            print(Pipes.vertical)
        print(
            Pipes.bottom_left,
            Pipes.horizontal * (self.size * 2),
            Pipes.intersection,
            Pipes.horizontal,
            "D",
            Pipes.horizontal * (self.size * 2 - 2),
            Pipes.intersection,
            Pipes.horizontal * (self.size * 2),
            Pipes.horizontal_bottom,
            Pipes.horizontal * (self.size * 2),
            Pipes.bottom_right,
            sep="",
        )

        for i in range(self.size):
            print(" " * (self.size * 2 + 1), end="")
            print(Pipes.vertical, end="")
            for j in range(self.size):
                self._print_letter(self.combinations[5][i * self.size + j])
            print(Pipes.vertical)

        print(
            " " * (self.size * 2 + 1),
            Pipes.bottom_left,
            Pipes.horizontal * (self.size * 2),
            Pipes.bottom_right,
            sep="",
        )

if __name__ == "__main__":
    cube = Cube(size=5, show_letter=True, scrambled=False)

    print("All possible moves:", len(cube.get_possible_moves()))

    cube.print()
    cube.make_move("F")
    cube.print()
