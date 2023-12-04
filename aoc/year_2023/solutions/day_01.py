# /usr/bin/python3
"""Day 1."""

from aoc.python.utils.parsing import read_lines


def part_one(path: str) -> int:
    lines = read_lines(path)
    res = 0
    for l in lines:
        digits = [int(c)
                  for c in l
                  if c.isdigit()]
        res += digits[0]*10+digits[-1]
    return res


def part_two(path: str) -> int:
    lines = read_lines(path)
    res = 0
    for l in lines:
        for val_str, val in [("one", "1"),
                             ("two", "2"),
                             ("three", "3"),
                             ("four", "4"),
                             ("five", "5"),
                             ("six", "6"),
                             ("seven", "7"),
                             ("eight", "8"),
                             ("nine", "9")]:
            l = l.replace(val_str, val_str+str(val)+val_str)
        print(l)
        digits = [int(c)
                  for c in l
                  if c.isdigit()]
        res += digits[0]*10+digits[-1]
    return res
