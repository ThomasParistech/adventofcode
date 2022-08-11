# /usr/bin/python3
"""Day 14."""

from typing import List, Set, Tuple
import numpy as np


def _read_lines(path):
    with open(path) as f:
        all_rows = f.readlines()

        polymer = all_rows[0].strip()
        transitions = [all_rows[k].strip().split(" -> ") for k in range(2, len(all_rows))]
        dict_transitions = {tr[0].strip(): tr[1].strip() for tr in transitions}
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
    polymer, dict_transitions = _read_lines(path)

    # Init
    all_letters = set(polymer+"".join(list(dict_transitions.values())))
    counts = {k: 0 for k in all_letters}
    counts_pairs = {p: 0 for p in dict_transitions.keys()}
    for i in range(len(polymer)-1):
        counts[polymer[i]] += 1
        key = polymer[i]+polymer[i+1]
        if key in counts_pairs:
            counts_pairs[key] += 1
    counts[polymer[-1]] += 1

    # Run
    for k in range(40):
        new_counts_pairs = {p: 0 for p in dict_transitions.keys()}
        for p, count in counts_pairs.items():
            new_el = dict_transitions[p]
            counts[new_el] += count

            p_left = p[0]+new_el
            p_right = new_el+p[1]

            if p_left in counts_pairs:
                new_counts_pairs[p_left] += count

            if p_right in counts_pairs:
                new_counts_pairs[p_right] += count
        counts_pairs = new_counts_pairs

    print(counts)
    return np.max(list(counts.values())) - np.min(list(counts.values()))
