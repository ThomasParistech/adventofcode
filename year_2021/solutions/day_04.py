# /usr/bin/python3
# type: ignore
"""Day 4."""

from typing import Optional

import numpy as np

bingo_size = 5


class Grid:
    def __init__(self, id, np_grid):
        self.id = id
        self.rows = [set() for _ in range(bingo_size)]
        self.cols = [set() for _ in range(bingo_size)]
        for (i, j), val in np.ndenumerate(np_grid):
            self.rows[i].add(val)
            self.cols[j].add(val)

    def try_remove(self, val) -> Optional[int]:
        for k in range(bingo_size):
            if val in self.rows[k]:
                self.rows[k].remove(val)
            if val in self.cols[k]:
                self.cols[k].remove(val)
        if all(len(s) != 0 for s in self.rows) and all(len(s) != 0 for s in self.cols):
            return None

        unmarked_sum = int(np.sum([np.sum(list(s)) for s in self.rows]))
        # print(f"ID {self.id}, Unmarked sum {unmarked_sum} => {unmarked_sum*val}")
        return unmarked_sum*val


def _read_grids(path):
    with open(path) as f:
        all_lines = f.readlines()
        random_draws = np.array(all_lines[0].strip().split(","), dtype=int)
        grids = []
        idx = 2
        while idx < len(all_lines):
            grid_lines = [all_lines[k].strip().replace("  ", " ").split(" ")
                          for k in range(idx, idx+bingo_size)]
            grids.append(Grid(len(grids), np.array(grid_lines, dtype=int)))
            idx += bingo_size+1  # blank line

        return random_draws, grids


def part_one(path: str) -> int:
    random_draws, grids = _read_grids(path)

    for val in random_draws:
        for grid in grids:
            answer = grid.try_remove(val)
            if answer is not None:
                return answer


def part_two(path: str) -> int:
    random_draws, grids = _read_grids(path)

    n_waiting = len(grids)
    for val in random_draws:
        answers = [grid.try_remove(val) for grid in grids]
        success_ids = [idx for idx, answer in enumerate(answers) if answer is not None]

        for idx in sorted(success_ids, reverse=True):
            grids.pop(idx)
        n_waiting -= len(success_ids)
        if n_waiting == 0:
            return answers[0]
