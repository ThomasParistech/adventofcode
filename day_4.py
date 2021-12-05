# /usr/bin/python3
"""Day 4."""

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

    def try_remove(self, val):
        for k in range(bingo_size):
            if val in self.rows[k]:
                self.rows[k].remove(val)
            if val in self.cols[k]:
                self.cols[k].remove(val)
        if all(len(s) != 0 for s in self.rows) and all(len(s) != 0 for s in self.cols):
            return False

        unmarked_sum = int(np.sum([np.sum(list(s)) for s in self.rows]))
        print(f"ID {self.id}, Unmarked sum {unmarked_sum} => {unmarked_sum*val}")
        return True


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


def part_one(path):
    random_draws, grids = _read_grids(path)

    for val in random_draws:
        if any(grid.try_remove(val) for grid in grids):
            break


def part_two(path):
    random_draws, grids = _read_grids(path)

    n_waiting = len(grids)
    for val in random_draws:
        success_ids = [idx for idx, grid in enumerate(grids) if grid.try_remove(val)]
        for idx in sorted(success_ids, reverse=True):
            grids.pop(idx)
        n_waiting -= len(success_ids)
        if n_waiting == 0:
            break


if __name__ == "__main__":
    input_path = '/home/trouch/Dev/adventofcode2021/day_4.csv'
    part_one(input_path)
    part_two(input_path)
