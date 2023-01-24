# /usr/bin/python3
"""Day 13."""

from functools import cmp_to_key
from typing import List
import numpy as np

from enum import Enum


class Comparison(Enum):
    LOWER = -1
    EQUAL = 0
    GREATER = 1


def _read_lines(path: str) -> List[List[int]]:
    with open(path) as f:
        rows = [row.strip() for row in f.readlines()]
        n_pairs = (len(rows)+1)//3
        pairs = [(eval(rows[3*k]), eval(rows[3*k+1]))
                 for k in range(n_pairs)]
        return pairs


def compare(a, b) -> Comparison:
    if isinstance(a, list) and isinstance(b, list):
        k = 0
        while k < min(len(a), len(b)):
            if compare(a[k], b[k]) == Comparison.GREATER:
                return Comparison.GREATER
            if compare(a[k], b[k]) == Comparison.LOWER:
                return Comparison.LOWER
            k += 1

        if len(a) == len(b):
            return Comparison.EQUAL

        return Comparison.LOWER if len(a) < len(b) else Comparison.GREATER

    if not isinstance(a, list) and not isinstance(b, list):
        if a == b:
            return Comparison.EQUAL

        return Comparison.LOWER if a < b else Comparison.GREATER

    if not isinstance(a, list):
        return compare([a], b)

    return compare(a, [b])


def part_one(path: str) -> int:
    pairs = _read_lines(path)

    score = 0
    for k, (a, b) in enumerate(pairs):
        if compare(a, b) != Comparison.GREATER:
            score += k + 1

    return score


def part_two(path: str) -> int:
    all_paquets = [p
                   for pair in _read_lines(path)
                   for p in pair]
    all_paquets += [[[2]], [[6]]]

    all_paquets = sorted(all_paquets,
                         key=cmp_to_key(lambda a, b: int(compare(a, b).value)))

    idx2 = all_paquets.index([[2]])
    idx6 = all_paquets.index([[6]])

    return (idx2+1) * (idx6+1)
