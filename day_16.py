# /usr/bin/python3
"""Day XXXXXX."""

from typing import List, Set, Tuple
import numpy as np
import time


def _read_lines(path):
    with open(path) as f:
        all_rows = f.readlines()
        all_rows = [list(row.strip()) for row in all_rows]

        np_rows = np.array(all_rows, dtype=int)
        return np_rows


def part_one(path):
    #
    #
    #
    #
    #
    #
    #     TODO
    #
    #
    #
    #
    #
    #
    #
    pass


def part_two(path):
    #
    #
    #
    #
    #
    #
    #     TODO
    #
    #
    #
    #
    #
    #
    #
    pass


if __name__ == "__main__":
    input_path = '/home/trouch/Dev/adventofcode2021/data/day_XXXXXX.csv'
    part_one(input_path)
    start = time.time()
    part_two(input_path)
    end = time.time()
    print(f"{end-start} s")
