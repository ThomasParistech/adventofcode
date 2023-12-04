# /usr/bin/python3
"""Day 3."""
from typing import List
from typing import Optional

import numpy as np

from aoc.python.utils.parsing import read_lines


def part_one(path: str) -> int:
    lines = read_lines(path)

    # Find special chars
    of_interest = np.zeros((len(lines), len(lines[0])), dtype=bool)
    for i, line in enumerate(lines):
        for j, c in enumerate(line):
            if not c.isdigit() and c != ".":
                for u in range(max(i-1, 0), 1+min(i+1, of_interest.shape[0]-1)):
                    for v in range(max(j-1, 0), 1+min(j+1, of_interest.shape[1]-1)):
                        of_interest[u, v] = True

    # plot_int_array(of_interest)

    # Find values near special chars
    res = 0
    for i, line in enumerate(lines):
        crt_val: Optional[int] = None
        crt_is_special: bool = False
        for j, c in enumerate(line):
            if c.isdigit():
                crt_is_special |= of_interest[i, j]
                if crt_val is None:
                    crt_val = int(c)
                else:
                    crt_val = 10*crt_val + int(c)
            else:
                if crt_val is not None:
                    if crt_is_special:
                        res += crt_val

                    crt_val = None
                    crt_is_special = False
        if crt_val is not None:
            if crt_is_special:
                res += crt_val

    return res


def part_two(path: str) -> int:
    lines = read_lines(path)

    # Find values
    next_id = 0
    value_id_mapping: List[int] = []
    value_id_grid = np.full((len(lines), len(lines[0])), fill_value=-1, dtype=int)
    for i, line in enumerate(lines):
        j_start: Optional[int] = None
        j_end: Optional[int] = None
        for j, c in enumerate(line):
            if c.isdigit():
                if j_start is None:
                    j_start = j
                j_end = j+1
            else:
                if j_start is not None:
                    value_id_grid[i, j_start:j_end] = next_id
                    value_id_mapping.append(int(line[j_start:j_end]))
                    next_id += 1
                    j_start, j_end = None, None

        if j_start is not None:
            value_id_grid[i, j_start:j_end] = next_id
            value_id_mapping.append(int(line[j_start:j_end]))
            next_id += 1
            j_start, j_end = None, None

    # print(value_id_mapping)
    # plot_int_array(value_id_grid)

    # Find gears
    res = 0
    for i, line in enumerate(lines):
        for j, c in enumerate(line):
            if c == "*":
                adjacent_ids = set(value_id_grid[u, v]
                                   for u in range(max(i-1, 0), 1+min(i+1, value_id_grid.shape[0]-1))
                                   for v in range(max(j-1, 0), 1+min(j+1, value_id_grid.shape[1]-1)))
                adjacent_ids.discard(-1)
                if len(adjacent_ids) == 2:
                    id1, id2 = tuple(adjacent_ids)
                    res += value_id_mapping[id1] * value_id_mapping[id2]
    return res
