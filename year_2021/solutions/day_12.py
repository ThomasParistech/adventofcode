# /usr/bin/python3
# type: ignore
"""Day XXXXXX."""

from typing import Dict
from typing import List


def _read_lines(path) -> Dict[str, List[str]]:  # Cave Name -> List of available cave names
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

        return possibilities


def propagate(possibilities, path_counts: int, path: List[str], allow_small_double: bool = False) -> int:
    if path[-1] == "end":
        # print(",".join(path))
        return path_counts + 1

    next_caves = possibilities[path[-1]]
    for next_cave in next_caves:
        is_small = (next_cave.lower() == next_cave)
        is_small_seen = is_small and next_cave in path
        if is_small_seen:
            if not allow_small_double:
                continue
            allow_small_double = False

        path.append(next_cave)
        path_counts = propagate(possibilities, path_counts, path, allow_small_double)
        path.pop()
        if is_small_seen:
            allow_small_double = True

    return path_counts


def part_one(path: str) -> int:
    possibilities = _read_lines(path)

    path = ["start"]
    path_counts = propagate(possibilities, 0, path)

    return path_counts


def part_two(path: str) -> int:
    possibilities = _read_lines(path)
    for _, v in possibilities.items():
        if "start" in v:
            v.remove("start")  # Not possible to go back to "start"

    path = ["start"]
    path_counts = propagate(possibilities, 0, path, allow_small_double=True)

    return path_counts
