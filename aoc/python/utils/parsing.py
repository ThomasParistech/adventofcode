# /usr/bin/python3
"""Parsing."""
import csv
from typing import Dict
from typing import List
from typing import Optional
from typing import Tuple

import numpy as np


def read_csv(path: str, delimiter: str = ',') -> List[List[str]]:
    """Read CSV file with custom delimiter."""
    with open(path, "r", encoding="utf-8") as f:
        reader = csv.reader(f, delimiter=delimiter)
        return list(reader)


def read(path: str) -> str:
    """Read lines"""
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def read_lines(path: str) -> List[str]:
    """Read lines"""
    with open(path, "r", encoding="utf-8") as f:
        return [l.strip() for l in f.readlines()]


def read_blocks(path: str, sep: str) -> List[List[str]]:
    """Read lines"""
    with open(path, "r", encoding="utf-8") as f:
        blocks = f.read().strip().split(sep)
        return [[line.strip() for line in b.strip().split("\n")]
                for b in blocks]


def block_as_np_str_grid(lines: List[str]) -> np.ndarray:
    """Read 2D binary grid from symbols"""
    return np.array([list(line) for line in lines])


def block_as_np_binary_grid(lines: List[str], true_symbol: str) -> np.ndarray:
    """Read 2D binary grid from symbols"""
    return block_as_np_str_grid(lines) == true_symbol


def block_as_np_int_grid(lines: List[str], mapping: Dict[str, int], default: Optional[int] = None) -> np.ndarray:
    """Read 2D int grid from symbols"""
    str_np = block_as_np_str_grid(lines)

    if default is None:
        fill_value = max(mapping.values())+1
    else:
        fill_value = default
    grid = np.full_like(str_np, fill_value=fill_value, dtype=int)
    for s, val in mapping.items():
        grid[str_np == s] = val

    if default is None:
        assert not np.any(grid == fill_value)
    return grid


def split_in_two(s: str, sep: str) -> Tuple[str, str]:
    """Split in two."""
    sep_split = s.strip().split(sep)
    assert len(sep_split) == 2, f"'{s}'"
    return sep_split[0].strip(), sep_split[1].strip()


def split_last(s: str, sep: str) -> str:
    """Split and take last."""
    return s.strip().split(sep)[-1]


def split_first(s: str, sep: str) -> str:
    """Split and take first."""
    return s.strip().split(sep)[0]


def split_in_three(s: str, sep: str) -> Tuple[str, str, str]:
    """Split in three."""
    sep_split = s.strip().split(sep)
    assert len(sep_split) == 3, f"'{s}'"
    return sep_split[0].strip(), sep_split[1].strip(), sep_split[2].strip()


def split_in_two_ints(s: str, sep: str) -> Tuple[int, int]:
    """Split in two."""
    a, b = split_in_two(s, sep)
    return int(a), int(b)


def split_in_three_ints(s: str, sep: str) -> Tuple[int, int, int]:
    """Split in three."""
    a, b, c = split_in_three(s, sep)
    return int(a), int(b), int(c)


def split_list_int(s: str, sep: str) -> List[int]:
    """Split into list of ints."""
    return [int(x) for x in s.strip().split(sep)]


def squeeze_symbol(s: str, symbol: str) -> str:
    """Squeeze consecutive occurences of a symbol."""
    done = False
    while not done:
        new_s = s.replace(symbol*2, symbol)
        done = new_s == s
        s = new_s
    return s
