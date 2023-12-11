# /usr/bin/python3
"""Day 10."""
import math
from dataclasses import dataclass
from typing import List
from typing import Optional
from typing import Tuple

import numpy as np

from aoc.python.utils.parsing import read_lines


@dataclass
class PairIJ:
    i: int
    j: int

    @property
    def left(self) -> 'PairIJ':
        return PairIJ(self.i, self.j-1)

    @property
    def right(self) -> 'PairIJ':
        return PairIJ(self.i, self.j+1)

    @property
    def up(self) -> 'PairIJ':
        return PairIJ(self.i-1, self.j)

    @property
    def down(self) -> 'PairIJ':
        return PairIJ(self.i+1, self.j)

    def is_valid(self, height: int, width: int) -> bool:
        return 0 <= self.i < height and 0 <= self.j < width


@dataclass
class NeighborsGrid:
    grid: List[List[Tuple[PairIJ, ...]]]
    symbols: List[List[str]]
    start: PairIJ

    def __getitem__(self, ij: PairIJ) -> Tuple[PairIJ, ...]:
        return self.grid[ij.i][ij.j]

    def __setitem__(self, ij: PairIJ, ngbs: Tuple[PairIJ, ...]):
        self.grid[ij.i][ij.j] = ngbs

    def get_symbol(self, ij: PairIJ) -> str:
        return self.symbols[ij.i][ij.j]

    @property
    def shape(self) -> Tuple[int, int]:
        return len(self.grid), len(self.grid[0])

    @staticmethod
    def from_str(path: str) -> 'NeighborsGrid':
        lines = read_lines(path)
        height, width = len(lines), len(lines[0])

        grid: List[List[Tuple[PairIJ, ...]]] = []
        start: Optional[PairIJ] = None

        for i, line in enumerate(lines):
            grid_row: List[Tuple[PairIJ, ...]] = []
            for j, c in enumerate(line):
                ij = PairIJ(i, j)

                links = None
                if c == "|":
                    links = ij.up, ij.down
                elif c == "-":
                    links = ij.left, ij.right
                elif c == "L":
                    links = ij.up, ij.right
                elif c == "J":
                    links = ij.up, ij.left
                elif c == "7":
                    links = ij.left, ij.down
                elif c == "F":
                    links = ij.right, ij.down
                elif c == "S":
                    start = ij

                grid_row.append(tuple(linked_ij for linked_ij in links if linked_ij.is_valid(height, width))
                                if links is not None
                                else tuple())
            grid.append(grid_row)

        assert start is not None
        ngb_grid = NeighborsGrid(grid, start=start, symbols=[list(line) for line in lines])

        ngb_grid[start] = tuple(ngb
                                for ngb in [start.left, start.right, start.up, start.down]
                                if start in ngb_grid[ngb])
        assert len(ngb_grid[start]) == 2
        ngb_0, ngb_1 = ngb_grid[start]

        start_symbol = None
        if ngb_0.i == ngb_1.i:
            start_symbol = "-"
        elif ngb_0.j == ngb_1.j:
            start_symbol = "|"
        else:
            if start.i+1 in (ngb_0.i, ngb_1.i):
                if start.j+1 in (ngb_0.j, ngb_1.j):
                    start_symbol = "F"
                else:
                    start_symbol = "7"
            else:
                if start.j+1 in (ngb_0.j, ngb_1.j):
                    start_symbol = "L"
                else:
                    start_symbol = "J"

        assert start_symbol is not None
        ngb_grid.symbols[start.i][start.j] = start_symbol

        return ngb_grid


def part_one(path: str) -> int:
    grid = NeighborsGrid.from_str(path)

    mask_contour = np.zeros(grid.shape, dtype=bool)

    contour_path: List[PairIJ] = [grid.start]
    while contour_path[-1] != grid.start or len(contour_path) == 1:
        crt_ij = contour_path[-1]
        next_ij = None
        if len(contour_path) == 1:
            next_ij = grid[crt_ij][0]
        else:
            for n in grid[crt_ij]:
                if n != contour_path[-2]:
                    next_ij = n
                    break

        assert next_ij is not None
        mask_contour[crt_ij.i, crt_ij.j] = True
        contour_path.append(next_ij)

    return math.floor((len(contour_path)-1)/2)


def part_two(path: str) -> int:
    grid = NeighborsGrid.from_str(path)

    mask_contour = np.zeros(grid.shape, dtype=bool)

    contour_path: List[PairIJ] = [grid.start]
    while contour_path[-1] != grid.start or len(contour_path) == 1:
        crt_ij = contour_path[-1]
        next_ij = None
        if len(contour_path) == 1:
            next_ij = grid[crt_ij][0]
        else:
            for n in grid[crt_ij]:
                if n != contour_path[-2]:
                    next_ij = n
                    break

        assert next_ij is not None
        mask_contour[crt_ij.i, crt_ij.j] = True
        contour_path.append(next_ij)

    corner_up = set({"L",  "J"})
    corner_down = set({"7", "F"})
    border_counts = np.zeros(grid.shape, dtype=int)
    for i in range(grid.shape[0]):
        crt_border_count = 0
        last_corner = None

        for j in range(grid.shape[1]):
            ij = PairIJ(i, j)
            symbol = grid.get_symbol(ij)
            if mask_contour[i, j]:
                if symbol == "|":
                    crt_border_count += 1
                elif symbol in corner_up:
                    if last_corner is None:
                        last_corner = symbol
                    else:
                        if last_corner in corner_down:
                            crt_border_count += 1
                        last_corner = None
                elif symbol in corner_down:
                    if last_corner is None:
                        last_corner = symbol
                    else:
                        if last_corner in corner_up:
                            crt_border_count += 1
                        last_corner = None

            border_counts[i, j] = crt_border_count

    border_counts[mask_contour] = 0

    # plot_int_array(border_counts, block=False)
    # plot_int_array(mask_contour)

    mask = (border_counts % 2) == 1

    return np.count_nonzero(mask)
