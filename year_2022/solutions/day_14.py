# /usr/bin/python3
"""Day 14."""

from typing import List, Tuple
import numpy as np
from enum import IntEnum


class Pixel(IntEnum):
    NONE = 0
    SAND = 1
    ROCK = 2
    NOZZLE = 3

    @staticmethod
    def imshow(grid: np.ndarray):
        import matplotlib.pyplot as plt
        plt.ioff()
        plt.matshow(grid)
        plt.show()


def _read_lines(path: str) -> Tuple[np.ndarray, int, int]:
    with open(path) as f:
        cmds = [[tuple(map(int, pos.split(",")))
                 for pos in row.strip().split(" -> ")]
                for row in f.readlines()]
        all_values = np.array([pos
                               for cmd in cmds
                               for pos in cmd])
        ymax = np.max(all_values[..., 1])
        xmin, xmax = np.min(all_values[..., 0]), np.max(all_values[..., 0])
        xmin -= 1
        xmax += 1

        grid = Pixel.NONE * np.ones((ymax+1, xmax-xmin+1))
        for cmd in cmds:
            for k in range(len(cmd)-1):
                sx, sy = cmd[k]
                ex, ey = cmd[k+1]
                ex -= xmin
                sx -= xmin
                if sx == ex:
                    min(sy, ey)
                    grid[min(sy, ey):max(sy, ey)+1, sx] = Pixel.ROCK
                else:
                    assert sy == ey
                    grid[sy, min(sx, ex):max(sx, ex)+1] = Pixel.ROCK
        nozzle_y, nozzle_x = 0, 500-xmin
        grid[nozzle_y, nozzle_x] = Pixel.NOZZLE
        return grid, nozzle_x, nozzle_y


def _move_sand(grid: np.ndarray, i: int, j: int) -> bool:
    # Return False if sand is falling in the abyss
    if i == grid.shape[0]-1:  # Last row
        # Pixel.imshow(grid)
        return False

    for new_i, new_j in [(i+1, j), (i+1, j-1), (i+1, j+1)]:
        if grid[new_i, new_j] == Pixel.NONE:
            return _move_sand(grid, new_i, new_j)

    # Pixel.imshow(grid)
    grid[i, j] = Pixel.SAND
    return True


def part_one(path: str) -> int:
    grid, nozzle_x, nozzle_y = _read_lines(path)

    count = 0
    while _move_sand(grid, nozzle_y, nozzle_x):
        count += 1

    return count


def part_two(path: str) -> int:
    rows = _read_lines(path)

    return -1
