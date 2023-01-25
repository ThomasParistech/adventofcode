# /usr/bin/python3
"""Day 14."""

from typing import List, Tuple, Optional
import numpy as np
from enum import IntEnum
import cv2


class Pixel(IntEnum):
    NONE = 0
    SAND = 1
    ROCK = 2
    NOZZLE = 3

    @staticmethod
    def imshow(grid: np.ndarray, wait_key: int = 0):
        img = np.zeros((*grid.shape, 3), dtype=np.uint8)
        img[grid == Pixel.NONE] = (241, 246, 227)
        img[grid == Pixel.SAND] = (51, 223, 254)
        img[grid == Pixel.ROCK] = (128, 135, 137)
        img[grid == Pixel.NOZZLE] = (166, 207, 47)
        height = 700
        img = cv2.resize(img, (int(height*float(img.shape[1])/img.shape[0]), height),
                         interpolation=cv2.INTER_NEAREST)
        cv2.imshow("Sand", img)
        cv2.waitKey(wait_key)


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
        ymax += 1

        xmin = min(xmin-1, 500-ymax)
        xmax = max(xmax+1, 500+ymax)

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


def part_one(path: str) -> int:
    grid, nozzle_x, nozzle_y = _read_lines(path)

    def _move_sand(grid: np.ndarray, i: int, j: int) -> bool:
        # Return False if sand is falling in the abyss
        if i == grid.shape[0]-1:  # Last row
            return False

        for new_i, new_j in [(i+1, j), (i+1, j-1), (i+1, j+1)]:
            if grid[new_i, new_j] == Pixel.NONE:
                return _move_sand(grid, new_i, new_j)

        # Pixel.imshow(grid)
        grid[i, j] = Pixel.SAND
        return True

    count = 0
    while _move_sand(grid, nozzle_y, nozzle_x):
        count += 1

    return count


def part_two(path: str) -> int:
    grid, nozzle_x, nozzle_y = _read_lines(path)

    def _move_sand(grid: np.ndarray, i: int, j: int) -> bool:
        # Return False if sand is stuck in the nozzle
        if i == grid.shape[0]-1:
            # Pixel.imshow(grid, wait_key=1)
            grid[i, j] = Pixel.SAND
            return True

        for new_i, new_j in [(i+1, j), (i+1, j-1), (i+1, j+1)]:
            if grid[new_i, new_j] == Pixel.NONE:
                return _move_sand(grid, new_i, new_j)

        if grid[i, j] == Pixel.NOZZLE:
            return False

        grid[i, j] = Pixel.SAND
        # Pixel.imshow(grid, wait_key=1)
        return True

    count = 0
    while _move_sand(grid, nozzle_y, nozzle_x):
        count += 1

    return count+1
