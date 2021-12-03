# /usr/bin/python3
"""Day 2."""

import pandas as pd
import numpy as np


def part_one(path):
    reader = pd.read_csv(path, chunksize=100, header=None,
                         names=["bin"], dtype=str)
    n_rows = 0
    bit_counts = np.zeros(12)
    for chunk in reader:
        n_rows += len(chunk)
        for b in chunk["bin"]:
            for idx, c in enumerate(b):
                if c == '1':
                    bit_counts[idx] += 1

    gamma_rate = bit_counts > n_rows/2
    event_rate = np.logical_not(gamma_rate)

    gamma_rate_val = sum(v << i for i, v in enumerate(gamma_rate[::-1]))
    event_rate_val = sum(v << i for i, v in enumerate(event_rate[::-1]))

    print(gamma_rate_val*event_rate_val)


def part_two(path):
    pass


if __name__ == "__main__":
    input_path = '/home/trouch/Dev/adventofcode2021/day_3.csv'
    part_one(input_path)
    part_two(input_path)
