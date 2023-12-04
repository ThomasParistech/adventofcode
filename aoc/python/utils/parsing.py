# /usr/bin/python3
"""Parsing."""
import csv
from typing import List


def read_csv(path: str, delimiter: str = ',') -> List[List[str]]:
    """Read CSV file with custom delimiter."""
    with open(path, "r", encoding="utf-8") as f:
        reader = csv.reader(f, delimiter=delimiter)
        return list(reader)


def read_lines(path: str) -> List[str]:
    """Read lines"""
    with open(path, "r", encoding="utf-8") as f:
        return [l.strip() for l in f.readlines()]
