# /usr/bin/python3
"""Day 25."""

from typing import List, Set, Tuple
import numpy as np


def show(mask_east, mask_south):
    tmp = np.zeros_like(mask_east, dtype=int)
    tmp[mask_east] = 1
    tmp[mask_south] = 2
    dico = {0: ".", 1: ">", 2: "v"}
    print("\n-----------")
    print("\n".join(["".join([dico[x] for x in row])for row in tmp]))


def _read_lines(path):
    with open(path) as f:
        all_rows = f.readlines()
        east = [[c == ">" for c in row.strip()] for row in all_rows]
        south = [[c == "v" for c in row.strip()] for row in all_rows]
        return np.array(east, dtype=bool), np.array(south, dtype=bool)


def part_one(path: str) -> int:
    east, south = _read_lines(path)

    n_steps = 0
    while True:
        n_steps += 1
        rolled_east = np.roll(east, 1, axis=1) & ~(east | south)
        east[np.roll(rolled_east, -1, axis=1)] = False
        east[rolled_east] = True

        rolled_south = np.roll(south, 1, axis=0) & ~(east | south)
        south[np.roll(rolled_south, -1, axis=0)] = False
        south[rolled_south] = True

        if not np.any(rolled_east) and not np.any(rolled_south):
            return n_steps


def part_two(path: str) -> int:
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
    return 0
