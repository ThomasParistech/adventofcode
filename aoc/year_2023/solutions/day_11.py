# /usr/bin/python3
"""Day 11."""

import numpy as np

from aoc.python.utils.parsing import read_lines


def _answer(path: str, new_size: int) -> int:
    lines = read_lines(path)

    is_galaxy = np.array([list(l) for l in lines]) == "#"
    list_galaxy = np.argwhere(is_galaxy).tolist()
    n_galaxies = len(list_galaxy)

    list_empty_row = np.argwhere(~np.any(is_galaxy, axis=1)).squeeze().tolist()
    list_empty_col = np.argwhere(~np.any(is_galaxy, axis=0)).squeeze().tolist()

    grid_base = np.zeros((n_galaxies, n_galaxies), dtype=int)
    grid_n_empty = np.zeros((n_galaxies, n_galaxies), dtype=int)
    for i in range(n_galaxies):
        yi, xi = list_galaxy[i]
        for j in range(i):

            yj, xj = list_galaxy[j]

            grid_base[i, j] = abs(xi-xj) + abs(yi-yj)
            grid_n_empty[i, j] = (sum(1 for y_row in list_empty_row if (yi-y_row) * (yj-y_row) < 0)
                                  + sum(1 for x_col in list_empty_col if (xi-x_col) * (xj-x_col) < 0))

    return np.sum(grid_base + (new_size-1)*grid_n_empty)


def part_one(path: str) -> int:
    return _answer(path, 2)


def part_two(path: str) -> int:
    return _answer(path, 1000000)
