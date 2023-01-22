# /usr/bin/python3
"""Day 3."""

from typing import List
import numpy as np


def _intersection(left: str, right: str) -> str:
    for l in left:
        if l in right:
            return l


def _read_lines(path: str) -> List[List[int]]:
    with open(path) as f:
        rows = [row.strip() for row in f.readlines()]
        return [(row[:len(row)//2], row[len(row)//2:]) for row in rows]


def part_one(path: str) -> int:
    rows = _read_lines(path)

    score = 0
    for left, right in rows:
        p = ord(_intersection(left, right))
        if p > 90:
            score += p - ord("a") + 1
        else:
            score += p - ord("A") + 27

    return score


def part_two(path: str) -> int:
    return -1
