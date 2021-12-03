# /usr/bin/python3
"""Day 1."""

import pandas as pd

input_path = '/home/trouch/Dev/adventofcode2021/day_1a.csv'

reader = pd.read_csv(input_path, delimiter=',', chunksize=100, header=None,
                     names=['depth'], dtype={'depth': int})

last_depth = None
n_increases = 0
for chunk in reader:
    for d in chunk["depth"]:
        if last_depth is not None and d > last_depth:
            n_increases += 1
        last_depth = d

print(n_increases)
