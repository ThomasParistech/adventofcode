# /usr/bin/python3
"""Day 14."""

from typing import List, Set, Tuple
import numpy as np


def _read_lines(path):
    with open(path) as f:
        all_rows = f.readlines()

        polymer = all_rows[0].strip()
        transitions = [all_rows[k].strip().split(" -> ") for k in range(2, len(all_rows))]
        dict_transitions = {tr[0]: tr[1] for tr in transitions}
        return polymer, dict_transitions


def part_one(path: str) -> int:
    polymer, dict_transitions = _read_lines(path)

    for k in range(10):
        new_polymer = []
        for i in range(len(polymer)-1):
            new_polymer.append(polymer[i])
            key = polymer[i]+polymer[i+1]
            if key in dict_transitions:
                new_polymer.append(dict_transitions[key])
        new_polymer.append(polymer[-1])
        polymer = "".join(new_polymer)

    counts = {k: 0 for k in set(polymer)}
    for el in polymer:
        counts[el] += 1

    return np.max(list(counts.values())) - np.min(list(counts.values()))


def part_two(path: str) -> int:
    #
    #
    #
    #
    #
    #
    #     TODO
    #
    #
    #
    #
    #
    #
    #
    return 0
