# /usr/bin/python3
"""Day 12."""
import copy
from typing import Dict
from typing import List
from typing import Optional

import numpy as np

from aoc.python.utils.parsing import read_lines
from aoc.python.utils.parsing import split_first
from aoc.python.utils.parsing import split_last
from aoc.python.utils.parsing import split_list_int
from aoc.python.utils.utils import last_index


def rec(sub_symbols: str, sub_numbers: List[int]) -> Optional[int]:
    if len(sub_numbers) == 0:
        return not '#' in sub_symbols

    if len(sub_symbols) == 0:
        return None

    if len(sub_symbols) < sum(sub_numbers) + len(sub_numbers)-1:
        return None

    sub_symbols = f".{sub_symbols}."

    idx_max = int(np.argmax(sub_numbers))
    val_max = sub_numbers[idx_max]
    left_sub_numbers = sub_numbers[:idx_max]
    right_sub_numbers = sub_numbers[idx_max+1:]

    total_res = 0
    for k in range(len(sub_symbols) - (val_max+2)+1):
        k_first = k
        k_last = k + val_max+1
        if '#' in (sub_symbols[k_first], sub_symbols[k_last]):
            continue
        if "." in sub_symbols[k_first+1:k_last]:
            continue

        res = 1
        left_res = rec(sub_symbols[1:k_first], left_sub_numbers)
        if left_res is None:
            continue
        res *= left_res

        right_res = rec(sub_symbols[k_last+1:-1], right_sub_numbers)
        if right_res is None:
            continue
        res *= right_res

        total_res += res

    if total_res == 0:
        return None

    return total_res


def brute_force(symbols: str, numbers: List[int]) -> int:
    """Brut force alternative to rec. Useful as ground truth to debug."""
    if "?" not in symbols:
        crt_numbers = []
        crt_size = 0
        for s in "."+symbols+".":
            if s == "#":
                crt_size += 1
            elif crt_size != 0:
                crt_numbers.append(crt_size)
                crt_size = 0

        if crt_numbers == numbers:
            # print(symbols)
            return 1
        return 0

    idx = symbols.index("?")

    res = 0
    res += brute_force(symbols[:idx]+"#"+symbols[idx+1:], numbers)
    res += brute_force(symbols[:idx]+"."+symbols[idx+1:], numbers)
    return res


def part_one(path: str) -> int:
    lines = read_lines(path)
    total_res = 0

    for line in lines:
        symbols = split_first(line, " ")
        numbers = split_list_int(split_last(line, " "), ",")

        rec_res = rec(symbols, numbers)
        assert rec_res is not None

        total_res += rec_res

    return total_res


def part_two(path: str) -> int:
    lines = read_lines(path)

    res = 0
    for line in lines:
        symbols = "?".join(5*[split_first(line, " ")])
        numbers = split_list_int(",".join(5*[split_last(line, " ")]), ",")
        res += solve(symbols, numbers)

    return res


def init_possibles(symbols: str, numbers: List[int]) -> List[np.ndarray]:
    """Store true if can start at this index"""
    assert symbols[0] == "." and symbols[-1] == "."
    can_start: Dict[int, np.ndarray] = {}
    for number in set(numbers):
        possible = np.zeros(len(symbols), dtype=bool)
        for k in range(1, len(symbols) - number):
            #   k
            #   |
            #  .##############.
            #  |              |
            # k_first       k_last
            k_first = k - 1
            k_last = k + number
            if '#' in (symbols[k_first], symbols[k_last]):
                continue
            if "." in symbols[k_first+1:k_last]:
                continue
            possible[k] = True
        can_start[number] = possible
    return [copy.deepcopy(can_start[nbr]) for nbr in numbers]


def solve(symbols: str, numbers: List[int]):
    symbols = f".{symbols}."

    possibles = init_possibles(symbols, numbers)

    all_counts = [np.zeros_like(possible, dtype=int) for possible in possibles]
    right_first_one = []
    for k in range(len(symbols)):
        try:
            right_first_one.append(k+symbols[k:].index("#"))
        except ValueError:
            right_first_one.append(-1)

    try:
        # Can't let the first '#' unused
        first_one = symbols.index("#")
        possibles[0][first_one+1:] = False
    except ValueError:
        pass

    try:
        # Can't let the last '#' unused
        last_one = last_index(symbols, "#")
        possibles[-1][:last_one - (numbers[-1]-1)] = False
    except ValueError:
        pass

    all_counts[0] = possibles[0].astype(int)
    for crt_idx in range(len(numbers)-1):
        crt_number = numbers[crt_idx]
        crt_counts = all_counts[crt_idx]

        next_possibles = possibles[crt_idx+1]
        next_counts = all_counts[crt_idx+1]

        possible_next_i = np.argwhere(next_possibles).reshape(-1)
        for crt_i in np.argwhere(crt_counts > 0).reshape(-1):
            lowerbound_possible_next_i = crt_i + crt_number+1  # First possible start
            if lowerbound_possible_next_i < len(symbols):
                upper_bound_possible_next_i = right_first_one[lowerbound_possible_next_i]  # Last possible start
                if upper_bound_possible_next_i > 0:
                    # don't let unsued '#' between segments
                    mask = np.logical_and(lowerbound_possible_next_i <= possible_next_i,
                                          possible_next_i <= upper_bound_possible_next_i)
                else:
                    mask = lowerbound_possible_next_i <= possible_next_i
                next_counts[possible_next_i[mask]] += crt_counts[crt_i]

    return int(np.sum(all_counts[-1]))
