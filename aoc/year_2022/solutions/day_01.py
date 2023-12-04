# /usr/bin/python3
"""Day 1."""

from typing import List

import numpy as np


def _read_lines(path: str) -> List[List[int]]:
    with open(path) as f:
        counts = [[int(row.strip()) for row in rows.split("\n")] for rows in f.read().split("\n\n")]
        return [np.sum(c) for c in counts]


def part_one(path: str) -> int:
    aggregated_counts = _read_lines(path)
    return np.max(aggregated_counts)


def part_two(path: str) -> int:
    aggregated_counts = _read_lines(path)
    top_three = np.argsort(aggregated_counts)[-3:]
    return np.sum(np.array(aggregated_counts)[top_three])
