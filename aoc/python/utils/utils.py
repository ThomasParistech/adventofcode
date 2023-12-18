# /usr/bin/python3
"""Utils."""
import numpy as np


def last_index(s: str, c: str) -> int:
    return len(s) - 1 - s[::-1].index(c)


def last_np_max(x: np.ndarray) -> int:
    return len(x) - 1 - int(np.argmax(x[::-1]))
