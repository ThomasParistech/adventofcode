# /usr/bin/python3
"""Day XXXXXX."""

from typing import List, Optional, Set, Tuple
import numpy as np

values_errors_dict = {
    ")": 3,
    "]": 57,
    "}": 1197,
    ">": 25137
}

values_complete_dict = {
    "(": 1,
    "[": 2,
    "{": 3,
    "<": 4
}

symbol_pairs = {"}": "{", "]": "[", ")": "(", ">": "<"}


def _read_lines(path):
    with open(path) as f:
        all_rows = f.readlines()
        return [row.strip() for row in all_rows]


def process(symbols: str) -> Tuple[Optional[str], List[int]]:
    stack = []
    for c in symbols:
        if c in ("(", "{", "[", "<"):
            stack.append(c)
        else:
            if len(stack) == 0 or symbol_pairs[c] != stack.pop():
                return c, stack

    return None, stack


def part_one(path: str) -> int:
    symbols_list = _read_lines(path)
    error_sum = 0
    for symbols in symbols_list:
        first_error_char, _ = process(symbols)
        if first_error_char is not None:
            error_sum += values_errors_dict[first_error_char]
    return error_sum


def part_two(path: str) -> int:
    symbols_list = _read_lines(path)
    scores = []
    for symbols in symbols_list:
        first_error_char, remaining_stack = process(symbols)
        if first_error_char is None:
            score = 0
            for c in remaining_stack[::-1]:  # Reverse
                score *= 5
                score += values_complete_dict[c]
            scores.append(score)
    scores.sort()
    return scores[int(len(scores)/2)]
