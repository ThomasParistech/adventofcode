# /usr/bin/python3
"""Day 4."""

from typing import List
import numpy as np


def _read_lines(path: str) -> List[List[int]]:
    with open(path) as f:
        return [[tuple(map(int, a.split("-")))
                 for a in row.strip().split(",")]
                for row in f.readlines()]


def part_one(path: str) -> int:
    rows = _read_lines(path)

    count = 0
    for task_a, task_b in rows:
        if task_a[0] <= task_b[0] and task_b[1] <= task_a[1]:
            count += 1
        elif task_b[0] <= task_a[0] and task_a[1] <= task_b[1]:
            count += 1

    return count


def part_two(path: str) -> int:
    rows = _read_lines(path)

    count = 0
    for task_a, task_b in rows:
        if task_a[1] >= task_b[0] and task_a[0] <= task_b[1]:
            count += 1

    return count
