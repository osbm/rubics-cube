import random
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from typing import List, Tuple, Dict, Union, Optional


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
        self.matplotlib_colors = {
            "w": "white",
            "o": "orange",
            "g": "green",
            "r": "red",
            "b": "blue",
            "y": "yellow",
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
        self.faces = list(self.face_to_index.keys())
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
        combinations = np.empty((6, size, size), dtype=str)

        for i in range(6):
            combinations[i] = self.colors[i]

        # lets put an x to the first element of each face so we can easily see the rotation
        # for i in range(6):
        #     combinations[i][1][0] = "x"
        return combinations

    def make_move(self, move: str, print_move: bool = False, print_cube: bool = False):
        # sanity check
        assert move in self.get_possible_moves(), f"Move {move} is invalid."

        if print_move:
            print("Making move:", move)

        if move[-1] == "'":
            self.make_move(move[:-1], print_move=False, print_cube=False)
            self.make_move(move[:-1], print_move=False, print_cube=False)
            self.make_move(move[:-1], print_move=False, print_cube=False)

            if print_cube:
                self.print()
            return
        elif move[-1] == "2":
            self.make_move(move[:-1], print_move=False, print_cube=False)
            self.make_move(move[:-1], print_move=False, print_cube=False)

            if print_cube:
                self.print()
            return

        # print("Apply move: ", move)
        # first lets deal with the rotational moves
        if move in self.faces:
            self._rotate_face(move, -1)
            # also we should rotate the slice
            if move == "F":
                # L -> U -> R -> D
                copy_of_combinations = self.combinations.copy()
                rows = [
                    copy_of_combinations[self.face_to_index["L"]][:, -1],  #
                    copy_of_combinations[self.face_to_index["U"]][-1],
                    copy_of_combinations[self.face_to_index["R"]][:, 0],  #
                    copy_of_combinations[self.face_to_index["D"]][0],
                ]
                self.combinations[self.face_to_index["L"]][:, -1] = rows[3]
                self.combinations[self.face_to_index["U"]][-1] = rows[0][::-1]
                self.combinations[self.face_to_index["R"]][:, 0] = rows[1]
                self.combinations[self.face_to_index["D"]][0] = rows[2][::-1]

            elif move == "R":
                # F -> U -> B -> D
                copy_of_combinations = self.combinations.copy()
                rows = [
                    copy_of_combinations[self.face_to_index["F"]][:, -1],
                    copy_of_combinations[self.face_to_index["U"]][:, -1],
                    copy_of_combinations[self.face_to_index["B"]][:, 0],
                    copy_of_combinations[self.face_to_index["D"]][:, -1],
                ]
                self.combinations[self.face_to_index["F"]][:, -1] = rows[3]
                self.combinations[self.face_to_index["U"]][:, -1] = rows[0]
                self.combinations[self.face_to_index["B"]][:, 0] = rows[1][::-1]
                self.combinations[self.face_to_index["D"]][:, -1] = rows[2][::-1]

            elif move == "U":
                # F -> L -> B -> R
                copy_of_combinations = self.combinations.copy()
                rows = [
                    copy_of_combinations[self.face_to_index["F"]][0],
                    copy_of_combinations[self.face_to_index["L"]][0],
                    copy_of_combinations[self.face_to_index["B"]][0],
                    copy_of_combinations[self.face_to_index["R"]][0],
                ]
                self.combinations[self.face_to_index["F"]][0] = rows[3]
                self.combinations[self.face_to_index["L"]][0] = rows[0]
                self.combinations[self.face_to_index["B"]][0] = rows[1]
                self.combinations[self.face_to_index["R"]][0] = rows[2]

            elif move == "L":
                # B -> U -> F -> D
                copy_of_combinations = self.combinations.copy()
                rows = [
                    copy_of_combinations[self.face_to_index["B"]][:, -1],  #
                    copy_of_combinations[self.face_to_index["U"]][:, 0],
                    copy_of_combinations[self.face_to_index["F"]][:, 0],
                    copy_of_combinations[self.face_to_index["D"]][:, 0],  #
                ]
                self.combinations[self.face_to_index["B"]][:, -1] = rows[3][::-1]
                self.combinations[self.face_to_index["U"]][:, 0] = rows[0][::-1]
                self.combinations[self.face_to_index["F"]][:, 0] = rows[1]
                self.combinations[self.face_to_index["D"]][:, 0] = rows[2]

            elif move == "B":
                # R -> U -> L -> D
                copy_of_combinations = self.combinations.copy()
                rows = [
                    copy_of_combinations[self.face_to_index["R"]][:, -1],
                    copy_of_combinations[self.face_to_index["U"]][0],
                    copy_of_combinations[self.face_to_index["L"]][:, 0],
                    copy_of_combinations[self.face_to_index["D"]][-1],
                ]
                self.combinations[self.face_to_index["R"]][:, -1] = rows[3][::-1]
                self.combinations[self.face_to_index["U"]][0] = rows[0]
                self.combinations[self.face_to_index["L"]][:, 0] = rows[1][::-1]
                self.combinations[self.face_to_index["D"]][-1] = rows[2]

            elif move == "D":
                # F -> R -> B -> L
                copy_of_combinations = self.combinations.copy()
                rows = [
                    copy_of_combinations[self.face_to_index["F"]][-1],
                    copy_of_combinations[self.face_to_index["R"]][-1],
                    copy_of_combinations[self.face_to_index["B"]][-1],
                    copy_of_combinations[self.face_to_index["L"]][-1],
                ]
                self.combinations[self.face_to_index["F"]][-1] = rows[3]
                self.combinations[self.face_to_index["R"]][-1] = rows[0]
                self.combinations[self.face_to_index["B"]][-1] = rows[1]
                self.combinations[self.face_to_index["L"]][-1] = rows[2]

        # then lets deal with the rotations
        # in rotations 2 faces are rotated
        # and rest of the faces are moved in a certain direction
        elif move == "x":
            # L and R are rotated
            self._rotate_face("L", 1)
            self._rotate_face("R", -1)
            ...
            # F -> U -> B -> D
            copy_of_combinations = self.combinations.copy()
            faces = [
                copy_of_combinations[self.face_to_index["F"]],
                copy_of_combinations[self.face_to_index["U"]],
                copy_of_combinations[self.face_to_index["B"]],
                copy_of_combinations[self.face_to_index["D"]],
            ]
            self.combinations[self.face_to_index["F"]] = faces[3]
            self.combinations[self.face_to_index["U"]] = faces[0]
            self.combinations[self.face_to_index["B"]] = faces[1]
            self.combinations[self.face_to_index["D"]] = faces[2]

            self._rotate_face("D", 1)
            self._rotate_face("D", 1)

            self._rotate_face("B", 1)
            self._rotate_face("B", 1)

        elif move == "y":
            # U and D are rotated
            self._rotate_face("U", -1)
            self._rotate_face("D", 1)
            ...
            # F -> L -> B -> R
            copy_of_combinations = self.combinations.copy()
            faces = [
                copy_of_combinations[self.face_to_index["F"]],
                copy_of_combinations[self.face_to_index["L"]],
                copy_of_combinations[self.face_to_index["B"]],
                copy_of_combinations[self.face_to_index["R"]],
            ]
            self.combinations[self.face_to_index["F"]] = faces[3]
            self.combinations[self.face_to_index["L"]] = faces[0]
            self.combinations[self.face_to_index["B"]] = faces[1]
            self.combinations[self.face_to_index["R"]] = faces[2]

        elif move == "z":
            # F and B are rotated
            self._rotate_face("F", -1)
            self._rotate_face("B", 1)
            ...
            # U -> R -> D -> L
            copy_of_combinations = self.combinations.copy()
            faces = [
                copy_of_combinations[self.face_to_index["U"]],
                copy_of_combinations[self.face_to_index["R"]],
                copy_of_combinations[self.face_to_index["D"]],
                copy_of_combinations[self.face_to_index["L"]],
            ]
            self.combinations[self.face_to_index["U"]] = faces[3]
            self.combinations[self.face_to_index["R"]] = faces[0]
            self.combinations[self.face_to_index["D"]] = faces[1]
            self.combinations[self.face_to_index["L"]] = faces[2]

            self._rotate_face("L", -1)
            self._rotate_face("D", -1)
            self._rotate_face("R", -1)
            self._rotate_face("U", -1)

        # move is slicing move
        # lets get the face and the direction
        # the number between m and F, R, U
        else:
            face = move[-1]
            index = int(move[1:-1])

            if face == "F":
                # U -> R -> D -> L
                copy_of_combinations = self.combinations.copy()
                slices = [
                    copy_of_combinations[self.face_to_index["U"]][-index - 1],
                    copy_of_combinations[self.face_to_index["R"]][:, index],
                    copy_of_combinations[self.face_to_index["D"]][index],
                    copy_of_combinations[self.face_to_index["L"]][:, -index - 1],
                ]
                self.combinations[self.face_to_index["U"]][-index - 1] = slices[3][::-1]
                self.combinations[self.face_to_index["R"]][:, index] = slices[0]
                self.combinations[self.face_to_index["D"]][index] = slices[1][::-1]
                self.combinations[self.face_to_index["L"]][:, -index - 1] = slices[2]

            elif face == "R":
                # U -> B -> D -> F
                copy_of_combinations = self.combinations.copy()
                slices = [
                    copy_of_combinations[self.face_to_index["U"]][:, -index-1],
                    copy_of_combinations[self.face_to_index["B"]][:, index],
                    copy_of_combinations[self.face_to_index["D"]][:, -index-1],
                    copy_of_combinations[self.face_to_index["F"]][:, -index-1],
                ]
                self.combinations[self.face_to_index["U"]][:, -index-1] = slices[3]
                self.combinations[self.face_to_index["B"]][:, index] = slices[0][::-1]
                self.combinations[self.face_to_index["D"]][:, -index-1] = slices[1][::-1]
                self.combinations[self.face_to_index["F"]][:, -index-1] = slices[2]

            elif face == "U":
                # F -> L -> B -> R
                copy_of_combinations = self.combinations.copy()
                slices = [
                    copy_of_combinations[self.face_to_index["F"]][index],
                    copy_of_combinations[self.face_to_index["L"]][index],
                    copy_of_combinations[self.face_to_index["B"]][index],
                    copy_of_combinations[self.face_to_index["R"]][index],
                ]
                self.combinations[self.face_to_index["F"]][index] = slices[3]
                self.combinations[self.face_to_index["L"]][index] = slices[0]
                self.combinations[self.face_to_index["B"]][index] = slices[1]
                self.combinations[self.face_to_index["R"]][index] = slices[2]

        if print_cube:
            self.print()

    def _rotate_face(self, face: str, direction: int):
        """
        Rotate a face of the cube

        Arguments:
            face: can be F, R, U, L, B, D
            direction: 1 for clockwise, -1 for counter clockwise
        """
        face_idx = self.face_to_index[face]
        face = self.combinations[face_idx]
        # lets use numpy to rotate the face 90 degrees
        rotated_face = np.rot90(face, direction)
        self.combinations[face_idx] = rotated_face

    def get_possible_moves(self):
        # get moves that are possible for any sized cube
        # i am going to implement my own notation to work with higher sized cubes
        # but for 3x3x3 cube, it will be the same as rubiks cube notation
        # there wont be any way to turn more than 1 slice at a time
        # https://ruwix.com/the-rubiks-cube/notation/

        # actually, reverse and double moves is kinda redundant

        rotational_moves = [*"xyz", "x'", "y'", "z'"]
        # copy of self.faces
        face_moves = self.faces.copy()
        face_moves.extend([move + "2" for move in self.faces])
        face_moves.extend([move + "'" for move in self.faces])

        # m1F means we will be rotating the slice of the cube that 1 layer away from the front face
        # m1R means we will be rotating the slice of the cube that 1 layer away from the right face
        # for a 3x3x3 cube, the 3 slices are m1F, m1R, and m1U

        # for a 4x4x4 cube, the 4 slices are m1F, m2F, m1R, m2R, m1U, m2U
        middle_layer_moves = []
        for i in range(1, self.size - 1):
            for face in ["F", "R", "U"]:
                move = f"m{i}{face}"
                middle_layer_moves.extend([move, move + "'", move + "2"])
                # move, move reverse, move double

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
                self._print_letter(self.combinations[0][i][j])
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
                    self._print_letter(self.combinations[j][i][k])

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
                self._print_letter(self.combinations[5][i][j])
            print(Pipes.vertical)

        print(
            " " * (self.size * 2 + 1),
            Pipes.bottom_left,
            Pipes.horizontal * (self.size * 2),
            Pipes.bottom_right,
            sep="",
        )

    def render_3d(
        self,
        indicate_axis: bool = False,
        indicate_faces: bool = True,
        filename: Optional[str] = None,
    ):
        """
        Render the cube in 3d using matplotlib
        """
        fig, ax = plt.subplots(subplot_kw={"projection": "3d"})

        # draw a cube
        # self.combinations shape == (6, size, size)
        # all faces 2 d which means every face has a dimension that is the same as the cube
        # draw the top face
        square_size = 1 / self.size
        for x_idx in range(self.size):
            for y_idx in range(self.size):
                x = [
                    x_idx * square_size,
                    x_idx * square_size,
                    (x_idx + 1) * square_size,
                    (x_idx + 1) * square_size,
                ]
                y = [
                    y_idx * square_size,
                    (y_idx + 1) * square_size,
                    (y_idx + 1) * square_size,
                    y_idx * square_size,
                ]

                z = [
                    1 for _ in range(4)
                ]  # z dimension is the same for all points in the top face
                verts = [list(zip(x, y, z))]
                ax.add_collection3d(
                    Poly3DCollection(
                        verts,
                        facecolors=self.matplotlib_colors[
                            self.combinations[0][-y_idx - 1][x_idx]
                        ],
                        linewidths=1,
                        edgecolors="black",
                    )
                )

        # draw the front face
        for z_idx in range(self.size):
            for x_idx in range(self.size):
                z = [
                    z_idx * square_size,
                    (z_idx + 1) * square_size,
                    (z_idx + 1) * square_size,
                    z_idx * square_size,
                ]
                x = [
                    x_idx * square_size,
                    x_idx * square_size,
                    (x_idx + 1) * square_size,
                    (x_idx + 1) * square_size,
                ]
                y = [0 for _ in range(4)]
                verts = [list(zip(x, y, z))]
                color = self.matplotlib_colors[
                    self.combinations[self.face_to_index["F"]][-z_idx - 1][x_idx]
                ]

                ax.add_collection3d(
                    Poly3DCollection(
                        verts,
                        facecolors=color,
                        linewidths=1,
                        edgecolors="black",
                    )
                )

        # draw the right face
        for z_idx in range(self.size):
            for y_idx in range(self.size):
                z = [
                    z_idx * square_size,
                    (z_idx + 1) * square_size,
                    (z_idx + 1) * square_size,
                    z_idx * square_size,
                ]
                y = [
                    y_idx * square_size,
                    y_idx * square_size,
                    (y_idx + 1) * square_size,
                    (y_idx + 1) * square_size,
                ]
                x = [1 for _ in range(4)]
                verts = [list(zip(x, y, z))]
                ax.add_collection3d(
                    Poly3DCollection(
                        verts,
                        facecolors=self.matplotlib_colors[
                            self.combinations[self.face_to_index["R"]][-z_idx - 1][
                                y_idx
                            ]
                        ],
                        linewidths=1,
                        edgecolors="black",
                    )
                )

        # indicate axis
        if indicate_axis:
            ax.set_xlabel("X")
            ax.set_ylabel("Y")
            ax.set_zlabel("Z")

        if indicate_faces:
            ax.text(1.1, 1.1, 0, "U")
            ax.text(1.1, 0, 1.1, "F")
            ax.text(0, 1.1, 1.1, "R")

        # remove the grid
        ax.grid(False)

        # remove the axes
        ax.set_axis_off()
        if filename is not None:
            plt.savefig(filename)
        else:
            plt.show()
