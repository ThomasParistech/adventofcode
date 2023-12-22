# /usr/bin/python3
"""Day 16."""
from dataclasses import dataclass
import copy
from typing import Dict
from typing import List, Tuple
from typing import Optional

import numpy as np

from aoc.python.utils.parsing import read_lines
from aoc.python.utils.parsing import split_first
from aoc.python.utils.parsing import split_last
from aoc.python.utils.parsing import split_list_int
from aoc.python.utils.utils import last_index

from aoc.python.utils.parsing import block_as_np_str_grid
from aoc.python.utils.parsing import read_lines, block_as_np_str_grid, read
from aoc.python.utils.display import print_2d_array

from enum import IntEnum


class Direction(IntEnum):
    UP = 0
    BOTTOM = 1
    LEFT = 2
    RIGHT = 3

    def move(self, i: int, j: int) -> Tuple[int, int]:
        if self == Direction.LEFT:
            j -= 1
        elif self == Direction.RIGHT:
            j += 1
        elif self == Direction.UP:
            i -= 1
        else:
            i += 1
        return i, j


TRANSITIONS: Dict[str, Dict[Direction, Direction]] = {
    "/": {
        Direction.BOTTOM: Direction.LEFT,
        Direction.UP: Direction.RIGHT,
        Direction.LEFT: Direction.BOTTOM,
        Direction.RIGHT: Direction.UP
    },
    "\\": {
        Direction.BOTTOM: Direction.RIGHT,
        Direction.UP: Direction.LEFT,
        Direction.LEFT: Direction.UP,
        Direction.RIGHT: Direction.BOTTOM
    }
}


@dataclass
class DirectionQueue:
    data: List[Tuple[int, int, Direction]]

    def __init__(self, init_i: int, init_j: int, src_direction: Direction):
        self.data = [(init_i, init_j, src_direction)]

    def append(self, src_i: int, src_j: int, direction: Direction):
        new_i, new_j = direction.move(src_i, src_j)
        self.data.append((new_i, new_j, direction))

    def empty(self) -> bool:
        return len(self.data) == 0

    def pop(self) -> Tuple[int, int, Direction]:
        return self.data.pop()


def get_energized_mask(grid: np.ndarray, i: int, j: int, direction: Direction) -> np.ndarray:
    seen_cache = np.zeros((grid.shape[0], grid.shape[1], 4), dtype=bool)

    queue = DirectionQueue(i, j, direction)

    while not queue.empty():
        i, j, direction = queue.pop()

        if not (0 <= i < grid.shape[0] and 0 <= j < grid.shape[1]):
            continue
        if seen_cache[i, j, direction]:
            continue

        seen_cache[i, j, direction] = True

        symbol = grid[i, j]
        if symbol == "-":
            if direction in (Direction.UP, Direction.BOTTOM):
                queue.append(i, j, Direction.LEFT)
                queue.append(i, j, Direction.RIGHT)
                continue
        elif symbol == "|":
            if direction in (Direction.LEFT, Direction.RIGHT):
                queue.append(i, j, Direction.UP)
                queue.append(i, j, Direction.BOTTOM)
                continue
        elif symbol in ("\\", "/"):
            queue.append(i, j, TRANSITIONS[symbol][direction])
            continue

        queue.append(i, j, direction)

    return np.any(seen_cache, axis=-1)


def part_one(path: str) -> int:
    grid = block_as_np_str_grid(read_lines(path))
    energized = get_energized_mask(grid, 0, 0, Direction.RIGHT)

    return int(np.count_nonzero(energized))


def part_two(path: str) -> int:
    grid = block_as_np_str_grid(read_lines(path))

    candidates = [(i, 0, Direction.RIGHT)
                  for i in range(grid.shape[0])]
    candidates += [(i, grid.shape[0]-1, Direction.LEFT)
                   for i in range(grid.shape[0])]
    candidates += [(0, j, Direction.BOTTOM)
                   for j in range(grid.shape[1])]
    candidates += [(grid.shape[1]-1, j, Direction.UP)
                   for j in range(grid.shape[1])]

    max_n_energized = 0
    for i, j, direction in candidates:
        energized = get_energized_mask(grid, i, j, direction)
        n_energized = int(np.count_nonzero(energized))

        if n_energized > max_n_energized:
            max_n_energized = n_energized

    return max_n_energized
