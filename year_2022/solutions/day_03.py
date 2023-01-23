# /usr/bin/python3
"""Day 3."""

from typing import List
import numpy as np


def _intersection(left: str, right: str) -> str:
    return list(set(left) & set(right))[0]


def _letter_to_priority(letter: str) -> int:
    p = ord(letter)
    if p > 90:
        return p - ord("a") + 1
    return p - ord("A") + 27


def _read_lines(path: str) -> List[List[int]]:
    with open(path) as f:
        return [row.strip() for row in f.readlines()]


def part_one(path: str) -> int:
    rows = _read_lines(path)

    score = 0
    for row in rows:
        p_char = _intersection(row[:len(row)//2], row[len(row)//2:])
        score += _letter_to_priority(p_char)

    return score


def part_two(path: str) -> int:
    rows = _read_lines(path)
    rows = np.array(rows).reshape(-1, 3)
    score = 0
    for group in rows:
        badge = set(group[0]) & set(group[1]) & set(group[2])
        score += _letter_to_priority(list(badge)[0])
    return score
