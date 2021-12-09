# /usr/bin/python3
"""Day 5."""

import numpy as np

grid_size = 1000


def _read_lines(path):
    with open(path) as f:
        row = f.readlines()[0].strip().split(',')
        return np.array(row, dtype=int)


def part_one(path):
    # Very slow and naive solution
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
    # Optimal!
    fishes = _read_lines(path)
    counts = {k: 0 for k in range(9)}
    for fish in fishes:
        counts[fish] += 1

    n_days = 256
    for _ in range(n_days):
        new_fishes = counts[0]
        for k in range(8):
            counts[k] = counts[k+1]
        counts[6] += new_fishes
        counts[8] = new_fishes
    print(np.sum([v for (k, v) in counts.items()]))


if __name__ == "__main__":
    input_path = '/home/trouch/Dev/adventofcode2021/data/day_6.csv'
    part_one(input_path)
    part_two(input_path)
