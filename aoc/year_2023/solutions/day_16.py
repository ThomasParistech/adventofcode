# /usr/bin/python3
"""Day 16."""
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


def part_one(path: str) -> int:
    grid = block_as_np_str_grid(read_lines(path))

    seen_cache = np.zeros((grid.shape[0], grid.shape[1], 4), dtype=bool)

    queue: List[Tuple[int, int, Direction]] = [(0, -1, Direction.RIGHT)]

    while len(queue) != 0:
        i, j, direction = queue.pop()

        i, j = direction.move(i, j)

        if not (0 <= i < grid.shape[0] and 0 <= j < grid.shape[1]):
            continue
        if seen_cache[i, j, direction]:
            continue

        seen_cache[i, j, direction] = True

        symbol = grid[i, j]
        if symbol == "-":
            if direction in (Direction.UP, Direction.BOTTOM):
                queue.append((i, j, Direction.LEFT))
                queue.append((i, j, Direction.RIGHT))
                continue
        elif symbol == "|":
            if direction in (Direction.LEFT, Direction.RIGHT):
                queue.append((i, j, Direction.UP))
                queue.append((i, j, Direction.BOTTOM))
                continue
        elif symbol in ("\\", "/"):
            queue.append((i, j, TRANSITIONS[symbol][direction]))
            continue

        queue.append((i, j, direction))

    energized = np.any(seen_cache, axis=-1)
    return int(np.count_nonzero(energized))


def part_two(path: str) -> int:
    return -1
