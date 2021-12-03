# /usr/bin/python3
"""Day 2."""

import pandas as pd


def part_one(path):
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

    print(horiz*depth)


def part_two(path):
    pass


if __name__ == "__main__":
    input_path = '/home/trouch/Dev/adventofcode2021/day_2.csv'
    part_one(input_path)
    part_two(input_path)
