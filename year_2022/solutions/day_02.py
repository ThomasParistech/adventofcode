# /usr/bin/python3
"""Day 2."""

from typing import List
import numpy as np


def _read_lines(path: str) -> List[List[int]]:
    with open(path) as f:
        return [row.strip() for row in f.readlines()]


def part_one(path: str) -> int:
    rows = _read_lines(path)

    possibilities = {}
    for k, todo in enumerate(["X", "Y", "Z"]):
        for opponent, win_score in zip(["A", "B", "C"], np.roll([3, 0, 6], k)):
            key = opponent+" "+todo
            possibilities[key] = k+1 + win_score

    scores = [possibilities[key] for key in rows]
    return np.sum(scores)


def part_two(path: str) -> int:
    rows = _read_lines(path)

    possibilities = {}
    for k, todo in enumerate(["X", "Y", "Z"]):
        for opponent, rock_score in zip(["A", "B", "C"], np.roll([3, 1, 2], -k)):
            key = opponent+" "+todo
            possibilities[key] = 3*k + rock_score

    scores = [possibilities[key] for key in rows]
    return np.sum(scores)
