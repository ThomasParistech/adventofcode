# /usr/bin/python3
# type: ignore
"""Day XXXXXX."""

from typing import List
from typing import Tuple

import numpy as np


class Grid:
    def __init__(self, grid: np.ndarray):
        self.data = grid
        self.count = 0

    def next(self) -> bool:
        self.data += 1

        first_flashes = [(i, j) for (i, j), val in np.ndenumerate(self.data) if val > 9]

        for (i, j) in first_flashes:
            self._propagate_flash(i, j)

        all_simultaneous_flashes = np.all(self.data > 9)
        self.data[self.data > 9] = 0
        return all_simultaneous_flashes

    def _propagate_flash(self, i, j):
        self.count += 1
        neighbors = self._get_neighbors(i, j)
        for (i_n, j_n) in neighbors:
            if self.data[i_n][j_n] > 9:
                continue

            self.data[i_n][j_n] += 1
            if self.data[i_n][j_n] > 9:
                self._propagate_flash(i_n, j_n)

    def _get_neighbors(self, i, j) -> List[Tuple[int, int]]:
        res = []
        for k in [-1, 0, 1]:
            for l in [-1, 0, 1]:
                i2 = i+k
                j2 = j+l
                if i2 >= 0 and j2 >= 0 and i2 < self.data.shape[0] and j2 < self.data.shape[1]:
                    res.append((i2, j2))
        return res


def _read_lines(path):
    with open(path) as f:
        all_rows = f.readlines()
        all_rows = [list(row.strip()) for row in all_rows]

        np_rows = np.array(all_rows, dtype=int)
        return np_rows


def part_one(path: str) -> int:
    np_rows = _read_lines(path)
    grid = Grid(np_rows)
    for k in range(100):
        grid.next()
        # print(grid.data)

    return grid.count


def part_two(path: str) -> int:
    np_rows = _read_lines(path)
    grid = Grid(np_rows)
    k = 1
    while True:
        if grid.next():
            return k
        k += 1

    return 0
