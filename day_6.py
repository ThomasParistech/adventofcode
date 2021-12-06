# /usr/bin/python3
"""Day 5."""

import numpy as np

grid_size = 1000


def _read_lines(path):
    with open(path) as f:
        row = f.readlines()[0].strip().split(',')
        return np.array(row, dtype=int)


def part_one(path):
    fishes = _read_lines(path)
    n_days = 80

    for k in range(n_days):
        fishes -= 1
        new_parents = (fishes == -1)
        fishes[new_parents] = 6
        fishes = np.concatenate((fishes, 8*np.ones_like(fishes[new_parents], dtype=int)))
        # print(fishes)
    print(len(fishes))


def part_two(path):
    pass


if __name__ == "__main__":
    input_path = '/home/trouch/Dev/adventofcode2021/data/day_6.csv'
    part_one(input_path)
    part_two(input_path)
