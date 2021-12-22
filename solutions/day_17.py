# /usr/bin/python3
"""Day 17."""

from typing import List, Set, Tuple
import numpy as np


def _read_lines(path):
    with open(path) as f:
        row = f.readlines()[0].strip()
        row = row.split("target area: ")[-1]
        xmin, xmax = tuple(int(val) for val in row.split(", ")[0][2:].split(".."))
        ymin, ymax = tuple(int(val) for val in row.split(", ")[1][2:].split(".."))
        assert ymax < 0
        assert xmin > 0
        return xmin, xmax, ymin, ymax


def part_one(path: str) -> int:
    _, _, ymin, ymax = _read_lines(path)

    vy0_list = np.array(list(range(-ymin-1, 0, -1)))  # From -ymin-1 to 1
    tmp = 2 * vy0_list+1
    tmp_square = tmp**2

    n_min_list = np.ceil(0.5*(tmp + np.sqrt(tmp_square - 8*ymax)))
    n_max_list = np.floor(0.5*(tmp + np.sqrt(tmp_square - 8*ymin)))

    is_valid_list = n_min_list <= n_max_list

    for idx, is_valid in enumerate(is_valid_list):
        if is_valid:
            vy0 = vy0_list[idx]
            ymax = (vy0*(vy0+1))//2
            return ymax

    return 0


def part_two(path: str) -> int:
    xmin, xmax, ymin, ymax = _read_lines(path)

    # Y
    vy0_list = np.array(list(range(ymin, -ymin)))
    tmp = 2 * vy0_list+1
    tmp_square = tmp**2

    n_min_list = np.ceil(0.5*(tmp + np.sqrt(tmp_square - 8*ymax))).astype(int)
    n_max_list = np.floor(0.5*(tmp + np.sqrt(tmp_square - 8*ymin))).astype(int)

    is_valid_list = n_min_list <= n_max_list
    n_counts_vy0 = {}
    for idx, is_valid in enumerate(is_valid_list):
        if is_valid:
            for n in range(n_min_list[idx], n_max_list[idx]+1):
                n_counts_vy0[n] = n_counts_vy0.get(n, []) + [vy0_list[idx]]

    # print(n_counts_vy0)

    # X
    n_to_test = np.array(list(n_counts_vy0.keys()), dtype=float)
    tmp_sum = 0.5*(n_to_test-1)

    vx0_min = tmp_sum + xmin / n_to_test
    vx0_max = tmp_sum + xmax / n_to_test

    vx0_min[n_to_test > vx0_min] = 0.5*(-1 + np.sqrt(1+8*xmin))  # Has reached its constant speed for the given n
    vx0_max[n_to_test > vx0_max] = 0.5*(-1 + np.sqrt(1+8*xmax))  # Has reached its constant speed for the given n

    vx0_min_list = np.ceil(vx0_min).astype(int)
    vx0_max_list = np.floor(vx0_max).astype(int)
    is_valid_list = vx0_min_list <= vx0_max_list

    n_counts_vx0 = {}
    for idx, is_valid in enumerate(is_valid_list):
        if is_valid:
            n = int(n_to_test[idx])
            n_counts_vx0[n] = n_counts_vx0.get(n, []) + list(range(vx0_min_list[idx], vx0_max_list[idx]+1))
    # print(n_counts_vx0)

    # Merge
    set_possibilities = set()
    for n in n_counts_vy0.keys():
        for vy0 in n_counts_vy0[n]:
            for vx0 in n_counts_vx0[n]:
                set_possibilities.add((vx0, vy0))

    return len(set_possibilities)
