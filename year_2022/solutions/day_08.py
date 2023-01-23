# /usr/bin/python3
"""Day 8."""

from typing import List, Tuple
import numpy as np


def _read_lines(path: str) -> np.ndarray:
    with open(path) as f:
        return np.array([list(row.strip()) for row in f.readlines()]).astype(int)


def part_one(path: str) -> int:
    heights = _read_lines(path)

    size = heights.shape[0]
    visible = np.zeros((size, size, 4), dtype=bool)

    def update(idx0, idx1, channel):
        h = heights[idx0, idx1]
        if h > maxima[channel]:
            visible[idx0, idx1, channel] = True
            maxima[channel] = h

    for i in range(size):
        maxima = [-1, -1, -1, -1]
        for j in range(size):
            update(i, j, 0)  # -> Right
            update(i, size-1-j, 1)  # <- Left
            update(j, i, 2)  # v Down
            update(size-1-j, i, 3)  # ^ Up

    return np.count_nonzero(np.max(visible, axis=-1))


def part_two(path: str) -> int:
    heights = _read_lines(path)
    size = heights.shape[0]

    def right(idx0, idx1) -> int:
        if idx0+1 == size:
            return 0
        h = heights[idx0, idx1]
        for k in range(idx0+1, size):
            if heights[k, idx1] >= h:
                return k - idx0
        return size-1 - idx0

    def left(idx0, idx1) -> int:
        if idx0 == 0:
            return 0
        h = heights[idx0, idx1]
        for k in range(idx0-1, -1, -1):
            if heights[k, idx1] >= h:
                return idx0 - k
        return idx0

    def down(idx0, idx1) -> int:
        if idx1+1 == size:
            return 0
        h = heights[idx0, idx1]
        for k in range(idx1+1, size):
            if heights[idx0, k] >= h:
                return k - idx1
        return size-1 - idx1

    def up(idx0, idx1) -> int:
        if idx1 == 0:
            return 0
        h = heights[idx0, idx1]
        for k in range(idx1-1, -1, -1):
            if heights[idx0, k] >= h:
                return idx1 - k
        return idx1

    scores = np.zeros((size, size), dtype=int)
    for i in range(size):
        for j in range(size):
            scores[i, j] = right(i, j)*left(i, j)*down(i, j)*up(i, j)

    return np.max(scores)
