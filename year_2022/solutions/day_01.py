# /usr/bin/python3
"""Day 1."""

from typing import List
import numpy as np


def _read_lines(path: str) -> List[List[int]]:
    with open(path) as f:
        return [[int(row.strip()) for row in rows.split("\n")] for rows in f.read().split("\n\n")]


def part_one(path: str) -> int:
    counts = _read_lines(path)
    aggregated_counts = [np.sum(c) for c in counts]
    return np.max(aggregated_counts)


def part_two(path: str) -> int:
    return -1
