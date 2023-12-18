# /usr/bin/python3
"""Day 13."""
from typing import List
from typing import Optional
from typing import Tuple

import numpy as np

from aoc.python.utils.parsing import block_as_np_binary_grid
from aoc.python.utils.parsing import read_blocks


def find_mirror(block: np.ndarray, vertical: bool, n_smudges: int) -> Optional[int]:
    if not vertical:
        block = block.T

    candidates: List[Tuple[int, int, int]] = [(k,                           # k (end_left and begin_right)
                                               max(0, 2*k-block.shape[1]),  # begin_left
                                               min(block.shape[1], 2*k))    # end_right
                                              for k in range(1, block.shape[1])]

    # Iterate over rows
    for k, begin_left, end_right in candidates:
        if np.count_nonzero(block[:, begin_left:k] != block[:, k:end_right][:, ::-1]) == n_smudges:
            return k

    return None


def solve(path: str, n_smudges: int):
    # '#': True
    # '.': False
    blocks = [block_as_np_binary_grid(lines, '#')
              for lines in read_blocks(path, "\n\n")]

    n_left_vertical = 0
    n_up_horizontal = 0
    for b in blocks:
        n_left = find_mirror(b, vertical=True, n_smudges=n_smudges)
        if n_left is not None:
            n_left_vertical += n_left
        else:
            n_left = find_mirror(b, vertical=False, n_smudges=n_smudges)
            assert n_left is not None
            n_up_horizontal += n_left

    return n_up_horizontal*100 + n_left_vertical


def part_one(path: str) -> int:
    return solve(path, n_smudges=0)


def part_two(path: str) -> int:
    return solve(path, n_smudges=1)
