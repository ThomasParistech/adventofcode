# /usr/bin/python3
"""Day 14."""
from typing import List
from typing import Optional
from typing import Tuple

import numpy as np

from aoc.python.utils.parsing import block_as_np_str_grid, read_lines
from aoc.python.utils.parsing import read_blocks, block_as_np_int_grid

from aoc.python.utils.utils import last_index, last_np_max

from aoc.python.utils.display import print_2d_array


def roll_north(grid: np.ndarray):
    grid = np.rot90(grid, k=1)
    roll_west(grid)
    return np.rot90(grid, k=-1)


def roll_west(grid: np.ndarray):
    for row in grid:
        for j in np.argwhere(row == "O").reshape(-1):
            if j != 0:
                obstacles = row[:j] != "."
                if np.any(obstacles):
                    j_closest_left_obstacle = last_np_max(row[:j] != ".")
                    if j_closest_left_obstacle == j-1:
                        continue
                    new_j = j_closest_left_obstacle+1
                else:
                    new_j = 0

                row[new_j] = "O"
                row[j] = "."


def part_one(path: str) -> int:
    grid = block_as_np_str_grid(read_lines(path))

    roll_north(grid)

    count_by_rows = np.count_nonzero(grid == "O", axis=1)

    return np.dot(count_by_rows, 1+np.arange(len(count_by_rows))[::-1])


def part_two(path: str) -> int:
    return -1
