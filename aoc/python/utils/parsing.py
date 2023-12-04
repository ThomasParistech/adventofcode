# /usr/bin/python3
"""Parsing."""
import csv
from typing import List


def read_csv(path: str, delimiter: str = ',') -> List[List[str]]:
    """Read CSV file with custom delimiter."""
    with open(path, "r", encoding="utf-8", newline='') as f:
        reader = csv.reader(f, delimiter=delimiter)
        return list(reader)
