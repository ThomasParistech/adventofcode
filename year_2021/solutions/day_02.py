# /usr/bin/python3
"""Day 2."""

import pandas as pd


def part_one(path: str) -> int:
    reader = pd.read_csv(path, delimiter=' ', chunksize=100, header=None,
                         names=['cmd', 'val'], dtype={'cmd': str, 'val': int})

    horiz = 0
    depth = 0
    for chunk in reader:
        for index, row in chunk.iterrows():
            cmd = row["cmd"]
            val = row["val"]
            if cmd == "forward":
                horiz += val
            elif cmd == "down":
                depth += val
            elif cmd == "up":
                depth -= val

    return horiz*depth


def part_two(path: str) -> int:
    reader = pd.read_csv(path, delimiter=' ', chunksize=100, header=None,
                         names=['cmd', 'val'], dtype={'cmd': str, 'val': int})

    horiz = 0
    depth = 0
    aim = 0
    for chunk in reader:
        for index, row in chunk.iterrows():
            cmd = row["cmd"]
            val = row["val"]
            if cmd == "forward":
                horiz += val
                depth += aim * val
            elif cmd == "down":
                aim += val
            elif cmd == "up":
                aim -= val

    return horiz*depth
