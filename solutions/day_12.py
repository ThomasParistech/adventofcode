# /usr/bin/python3
"""Day XXXXXX."""

from typing import List, Set, Tuple
import numpy as np


def _read_lines(path):
    with open(path) as f:
        all_rows = f.readlines()
        paths = [tuple(row.strip().split('-')) for row in all_rows]

        possibilities = {}

        for (a, b) in paths:
            if a in possibilities:
                possibilities[a].append(b)
            else:
                possibilities[a] = [b]

            if b in possibilities:
                possibilities[b].append(a)
            else:
                possibilities[b] = [a]

        return possibilities  # Cave Name -> List of available cave names


def propagate(possibilities, path_counts: int, path: List[str]) -> int:
    if path[-1] == "end":
        print(",".join(path))
        return path_counts + 1

    next_caves = possibilities[path[-1]]
    for next_cave in next_caves:
        if (next_cave.lower() == next_cave) and next_cave in path:
            continue

        path.append(next_cave)
        path_counts = propagate(possibilities, path_counts, path)
        path.pop()

    return path_counts


def part_one(path: str) -> int:
    possibilities = _read_lines(path)

    path = ["start"]
    path_counts = propagate(possibilities, 0, path)

    return path_counts


def part_two(path: str) -> int:
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
