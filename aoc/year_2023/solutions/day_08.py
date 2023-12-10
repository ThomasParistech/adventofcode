# /usr/bin/python3
"""Day 8."""
import math
from dataclasses import dataclass
from functools import reduce
from typing import Dict
from typing import List
from typing import Set

import numpy as np

from aoc.python.utils.parsing import read_lines
from aoc.python.utils.parsing import split_in_two


@dataclass
class _BaseData:
    words: Dict[str, int]
    index_transformation: np.ndarray
    n_commands: int

    @staticmethod
    def from_str(path: str) -> '_BaseData':
        lines = read_lines(path)
        first_line = lines[0]
        commands_is_left = np.array([c == "L" for c in first_line])

        words = {}
        left_words: List[str] = []
        right_words: List[str] = []
        for k, line in enumerate(lines[2:]):
            word, pair = split_in_two(line, " = ")
            left, right = split_in_two(pair[1:-1], ", ")
            left_words.append(left)
            right_words.append(right)
            words[word] = k

        left_indices = np.array([words[left] for left in left_words])
        right_indices = np.array([words[right] for right in right_words])

        indices = np.arange(len(left_indices))
        for is_left in commands_is_left:
            if is_left:
                indices = left_indices[indices]
            else:
                indices = right_indices[indices]

        return _BaseData(index_transformation=indices,
                         n_commands=len(commands_is_left),
                         words=words)


@dataclass
class NormalData:
    index_transformation: np.ndarray
    n_commands: int
    start_idx: int
    end_idx: int

    @staticmethod
    def from_str(path: str) -> 'NormalData':
        data = _BaseData.from_str(path)
        return NormalData(index_transformation=data.index_transformation,
                          n_commands=data.n_commands,
                          start_idx=data.words["AAA"],
                          end_idx=data.words["ZZZ"])


def part_one(path: str) -> int:
    data = NormalData.from_str(path)

    n_steps = 0
    crt_idx = data.start_idx
    while crt_idx != data.end_idx:
        crt_idx = data.index_transformation[crt_idx]
        n_steps += data.n_commands

    return n_steps


@dataclass
class GhostEndTimes:
    first_n_steps: int
    period: int
    end_idx: int
    start_idx: int


@dataclass
class GhostData:
    index_transformation: np.ndarray
    n_commands: int
    ghost_start_indices: Set[int]
    ghost_end_indices: Set[int]

    @staticmethod
    def from_str(path: str) -> 'GhostData':
        data = _BaseData.from_str(path)
        return GhostData(index_transformation=data.index_transformation,
                         n_commands=data.n_commands,
                         ghost_start_indices=set(k for word, k in data.words.items() if word.endswith("A")),
                         ghost_end_indices=set(k for word, k in data.words.items() if word.endswith("Z")))

    def find_ghost_end_times(self) -> List[GhostEndTimes]:
        res: List[GhostEndTimes] = []

        for start_idx in self.ghost_start_indices:
            n_steps = 0
            crt_idx = start_idx
            while crt_idx not in self.ghost_end_indices:
                crt_idx = self.index_transformation[crt_idx]
                n_steps += self.n_commands

            end_idx = crt_idx
            period = 0
            while period == 0 or crt_idx not in self.ghost_end_indices:
                crt_idx = self.index_transformation[crt_idx]
                period += self.n_commands
            res.append(GhostEndTimes(start_idx=start_idx,
                                     end_idx=end_idx,
                                     first_n_steps=n_steps,
                                     period=period))  # Weird fact: first_n_steps=period
        return res


def lcm(x, y):
    return (x * y) // math.gcd(x, y) if x and y else 0


def part_two(path: str) -> int:
    data = GhostData.from_str(path)
    return reduce(lcm,  [x.first_n_steps for x in data.find_ghost_end_times()])
