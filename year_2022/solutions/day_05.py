# /usr/bin/python3
"""Day 5."""

from typing import List, Tuple
import numpy as np
from dataclasses import dataclass


@dataclass
class Move:
    n: int
    src: int
    dst: int


def _read_lines(path: str) -> Tuple[List[List[int]], List[Move]]:
    with open(path) as f:
        begin, end = tuple(f.read().split("\n\n"))
        begin = begin.split("\n")
        end = end.split("\n")
        n_piles = int(begin.pop().strip().split(" ")[-1])

        stocks = [[] for _ in range(n_piles)]
        for k in range(len(begin)):  # From bottom to top
            row = begin[-k-1]+" "
            row = [row[i:i+4][1:-2] for i in range(0, len(row), 4)]
            for i, letter in enumerate(row):
                if letter != " ":
                    stocks[i].append(letter)

        cmds = []
        for row in end:
            row, dst = row.split(" to ")
            row, src = row.split(" from ")
            n = row.split("move ")[-1]
            cmds.append(Move(n=int(n), src=int(src)-1, dst=int(dst)-1))

        return stocks, cmds


def part_one(path: str) -> int:
    stocks, cmds = _read_lines(path)

    for cmd in cmds:
        for _ in range(cmd.n):
            val = stocks[cmd.src].pop()
            stocks[cmd.dst].append(val)

    return "".join([pile[-1] for pile in stocks])


def part_two(path: str) -> int:
    stocks, cmds = _read_lines(path)

    for cmd in cmds:
        stocks[cmd.dst].extend(stocks[cmd.src][-cmd.n:])
        stocks[cmd.src] = stocks[cmd.src][:-cmd.n]

    return "".join([pile[-1] for pile in stocks])
