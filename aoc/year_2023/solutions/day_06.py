# /usr/bin/python3
"""Day 6."""
import math
from dataclasses import dataclass
from typing import Tuple

from aoc.python.utils.parsing import read
from aoc.python.utils.parsing import split_in_two
from aoc.python.utils.parsing import split_last
from aoc.python.utils.parsing import split_list_int
from aoc.python.utils.parsing import squeeze_symbol


@dataclass
class Race:
    time: int
    distance: int

    def get_winning_interval(self) -> Tuple[int, int]:
        delta = self.time**2 - 4*(self.distance+1)  # +1 to beat the record
        assert delta >= 0
        delta_sqrt = math.sqrt(delta)

        c_min = math.ceil(0.5*(self.time - delta_sqrt))
        c_max = math.floor(0.5*(self.time + delta_sqrt))

        return c_min, c_max


def part_one(path: str) -> int:
    s = squeeze_symbol(read(path), " ")
    times_str, distances_str = split_in_two(s, "\n")
    times = split_list_int(split_last(times_str, ":"), " ")
    distances = split_list_int(split_last(distances_str, ":"), " ")

    res = 1
    for time, distance in zip(times, distances):
        race = Race(time=time, distance=distance)
        c_min, c_max = race.get_winning_interval()
        res *= c_max-c_min+1
    return res


def part_two(path: str) -> int:
    s = squeeze_symbol(read(path), " ")
    times_str, distances_str = split_in_two(s, "\n")
    race = Race(time=int(split_last(times_str, ":").replace(" ", "")),
                distance=int(split_last(distances_str, ":").replace(" ", "")))
    c_min, c_max = race.get_winning_interval()
    return c_max-c_min+1
