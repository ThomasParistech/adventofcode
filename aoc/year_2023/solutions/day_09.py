# /usr/bin/python3
"""Day 9."""
import math
from dataclasses import dataclass
from functools import reduce
from typing import Dict
from typing import List
from typing import Set

import numpy as np

from aoc.python.utils.parsing import read_lines, split_list_int
from aoc.python.utils.parsing import split_in_two


def predict_right(values: np.ndarray) -> int:
    if np.count_nonzero(values) == 0:
        return 0
    return values[-1] + predict_right(np.diff(values))


def part_one(path: str) -> int:
    lines = read_lines(path)
    res = 0
    for line in lines:
        res += predict_right(np.array(split_list_int(line, " ")))
    return res


def predict_left(values: np.ndarray) -> int:
    if np.count_nonzero(values) == 0:
        return 0
    return values[0] - predict_left(np.diff(values))


def part_two(path: str) -> int:
    lines = read_lines(path)
    res = 0
    for line in lines:
        res += predict_left(np.array(split_list_int(line, " ")))
    return res
