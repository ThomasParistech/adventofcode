# /usr/bin/python3
"""Day 14."""
from dataclasses import dataclass
from typing import Dict

import numpy as np

from aoc.python.utils.parsing import block_as_np_str_grid
from aoc.python.utils.parsing import read_lines


def part_one(path: str) -> int:
    platform = Platform.from_str(path)
    platform.roll_north()
    return platform.score_north()


@dataclass
class Platform:
    grid: np.ndarray

    @staticmethod
    def from_str(path: str) -> 'Platform':
        return Platform(grid=block_as_np_str_grid(read_lines(path)))

    def __hash__(self) -> int:
        return hash(self.grid.tobytes())

    def score_north(self) -> int:
        count_by_rows = np.count_nonzero(self.grid == "O", axis=1)
        return np.dot(count_by_rows, 1+np.arange(len(count_by_rows))[::-1])

    def cycle(self):
        self.roll_north()
        self.roll_west()
        self.roll_south()
        self.roll_east()

    def roll_west(self):
        for row in self.grid:
            last_available_idx = None
            for j, c in enumerate(row):
                if c == "O":
                    if last_available_idx is not None:
                        row[last_available_idx] = "O"
                        row[j] = "."
                        last_available_idx += 1
                elif c == "#":
                    last_available_idx = None
                elif last_available_idx is None:
                    last_available_idx = j

    def roll_north(self):
        self._roll_west_rotated(k=1)

    def roll_east(self):
        self._roll_west_rotated(k=2)

    def roll_south(self):
        self._roll_west_rotated(k=-1)

    def _roll_west_rotated(self, k: int):
        self.grid = np.rot90(self.grid, k=k)
        self.roll_west()
        self.grid = np.rot90(self.grid, k=-k)


def part_two(path: str) -> int:
    platform = Platform.from_str(path)

    hash_to_n_cycles: Dict[int, int] = {}  # hash -> n_cycles
    n_cycles_to_score: Dict[int, int] = {}  # n_cycles -> score
    n_total_cycles = 1000000000
    for n_cycles in range(1, n_total_cycles+1):
        platform.cycle()

        hash_val = hash(platform)

        previous_n_cycles = hash_to_n_cycles.get(hash_val, None)
        if previous_n_cycles is not None:
            pattern_size = n_cycles - previous_n_cycles
            remainder = (n_total_cycles-previous_n_cycles) % pattern_size
            return n_cycles_to_score[previous_n_cycles+remainder]

        hash_to_n_cycles[hash_val] = n_cycles
        n_cycles_to_score[n_cycles] = platform.score_north()

    return -1
