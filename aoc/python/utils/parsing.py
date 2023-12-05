# /usr/bin/python3
"""Parsing."""
import csv
from typing import List
from typing import Tuple


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


def split_in_two(s: str, sep: str) -> Tuple[str, str]:
    """Split in two."""
    sep_split = s.strip().split(sep)
    assert len(sep_split) == 2, f"'{s}'"
    return sep_split[0].strip(), sep_split[1].strip()


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
    return [int(x) for x in s.split(sep)]
