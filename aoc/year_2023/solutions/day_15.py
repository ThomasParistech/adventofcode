# /usr/bin/python3
"""Day 15."""
from typing import Dict
from typing import List

from aoc.python.utils.parsing import read
from aoc.python.utils.parsing import split_first
from aoc.python.utils.parsing import split_last


def hash_step(s: str) -> int:
    ascii_codes = [ord(c) for c in s]

    crt_val = 0
    for code in ascii_codes:
        crt_val += code
        crt_val *= 17
        crt_val %= 256

    return crt_val


def part_one(path: str) -> int:
    steps = read(path).split(",")
    return sum(hash_step(s) for s in steps)


def part_two(path: str) -> int:
    steps = read(path).split(",")

    boxes: List[Dict[str, int]] = [{} for _ in range(256)]

    for s in steps:
        if s[-1] == "-":
            label = s[:-1]
            box = boxes[hash_step(label)]
            box.pop(label, None)
        else:
            label = split_first(s, "=")
            focal = int(split_last(s, "="))
            box = boxes[hash_step(label)]
            box[label] = focal

    return sum([(i+1) * (j+1) * focal
                for i, box in enumerate(boxes)
                for j, focal in enumerate(box.values())])
