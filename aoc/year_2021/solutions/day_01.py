# /usr/bin/python3
"""Day 1."""

import pandas as pd


def part_one(path: str) -> int:
    reader = pd.read_csv(path, delimiter=',', chunksize=100, header=None,
                         names=['depth'], dtype={'depth': int})

    last_depth = None
    n_increases = 0
    for chunk in reader:
        for d in chunk["depth"]:
            if last_depth is not None and d > last_depth:
                n_increases += 1
            last_depth = d

    return n_increases


def part_two(path: str) -> int:
    reader = pd.read_csv(path, delimiter=',', chunksize=100, header=None,
                         names=['depth'], dtype={'depth': int})

    last_depth = None
    last_last_depth = None
    last_sum = None
    n_increases = 0
    for chunk in reader:
        for d in chunk["depth"]:
            if last_last_depth is not None and last_depth is not None:
                sum = d + last_depth + last_last_depth
                if last_sum is not None and sum > last_sum:
                    n_increases += 1
                last_sum = sum

            last_last_depth = last_depth
            last_depth = d

    return n_increases
