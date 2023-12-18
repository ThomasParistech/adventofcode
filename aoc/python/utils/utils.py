# /usr/bin/python3
"""Utils."""
import numpy as np

from typing import Any


def last_index(s: str, c: str) -> int:
    return len(s) - 1 - s[::-1].index(c)


def last_np_max(x: np.ndarray) -> int:
    return len(x) - 1 - int(np.argmax(x[::-1]))


def last_np_index(x: np.ndarray, val: Any) -> int:
    return last_np_max(x == val)
