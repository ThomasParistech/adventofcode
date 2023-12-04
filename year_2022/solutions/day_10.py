# /usr/bin/python3
# type: ignore
"""Day 10."""

from typing import List
from typing import Optional

import numpy as np


def _read_lines(path: str) -> List[Optional[int]]:
    with open(path) as f:
        rows = [row.strip() for row in f.readlines()]

        return [int(row.split(" ")[-1])if row != "noop" else None
                for row in rows]


def part_one(path: str) -> int:
    rows = _read_lines(path)

    x = 1
    cycles = 0
    score = 0
    next_target = 20
    for cmd in rows:
        cycles += 1 if cmd is None else 2

        if cycles >= next_target:
            score += x*next_target
            next_target += 40

        if cmd is not None:
            x += cmd

    return score


def part_two(path: str) -> int:
    rows = _read_lines(path)

    x = 1
    cycles = 0
    score = 0
    img = np.zeros((6, 40), dtype=bool)
    for cmd in rows:
        for _ in range(1 if cmd is None else 2):
            cycles += 1
            x_cycle = (cycles-1) % 40
            y_cycle = (cycles-1) // 40

            img[y_cycle, x_cycle] = abs(x - x_cycle) <= 1

        if cmd is not None:
            x += cmd

    img_txt = "\n".join(["".join(row) for row in img.astype(int).astype(str)])
    img_txt = img_txt.replace("0", ".").replace("1", "#")
    print(img_txt)
    return None
