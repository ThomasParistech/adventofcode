# /usr/bin/python3
"""Brute force variant of Day 8."""

from typing import List, Set, Tuple
import numpy as np
from itertools import permutations
import copy
import time


def sort_str(s) -> str:
    return "".join(sorted(s))


def try_and_translate(list_str: List[str], word_code: str):
    tmp_list = copy.deepcopy(list_str)
    assert len(word_code) == 7
    for idx, s in enumerate(list_str):
        for old, new in zip("abcdefg", word_code):
            s = s.replace(old, new.upper())
        tmp_list[idx] = sort_str(s.lower())

    return tmp_list


def check_list(list_str: List[str]) -> bool:
    return "|".join(sorted(list_str)) == "abcdefg|abcdfg|abcefg|abdefg|abdfg|acdeg|acdfg|acf|bcdf|cf"


def eval_4_digts(list_str: List[str]) -> int:
    assert len(list_str) == 4

    digits_dict = {"abcefg": "0",
                   "cf": "1",
                   "acdeg": "2",
                   "acdfg": "3",
                   "bcdf": "4",
                   "abdfg": "5",
                   "abdefg": "6",
                   "acf": "7",
                   "abcdefg": "8",
                   "abcdfg": "9"
                   }
    digits = [digits_dict[segments] for segments in list_str]
    return int("".join(digits))


def _read_lines(path) -> Tuple[List[Set[int]], List[str]]:
    with open(path) as f:
        all_rows = f.readlines()

        signals, out_digits = [], []
        for row in all_rows:
            left, right = tuple(row.strip().split(' | '))
            signals.append([sort_str(s) for s in left.split(' ')])
            out_digits.append([sort_str(s) for s in right.split(' ')])

        return signals, out_digits


def part_one(path: str) -> int:
    _, out_digits = _read_lines(path)

    count_uniques = 0
    for vec in out_digits:
        for s in vec:
            if len(s) in (2, 3, 4, 7):
                count_uniques += 1
    return count_uniques


def part_two(path: str) -> int:
    signals, out_digits = _read_lines(path)
    sum = 0
    for signals_vec, out_digits_vec in zip(signals, out_digits):
        for word_code in permutations('abcdefg'):
            word_code = ''.join(word_code)
            translation = try_and_translate(signals_vec, word_code)
            if check_list(translation):
                good_digits = try_and_translate(out_digits_vec, word_code)
                sum += eval_4_digts(good_digits)
                break
    return sum
