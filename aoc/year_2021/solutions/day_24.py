# /usr/bin/python3
# type: ignore
"""Day 24."""

from typing import List
from typing import Optional
from typing import Tuple

import numpy as np


def _read_lines(path):
    with open(path) as f:
        all_rows = np.array([row.strip() for row in f.readlines()])
        inp_indices = [idx for idx, row in enumerate(all_rows) if len(row.split(" ")) == 2]
        alphas = [int(row.split(" ")[-1]) for row in all_rows[[idx + 4 for idx in inp_indices]]]
        betas = [int(row.split(" ")[-1]) for row in all_rows[[idx + 5 for idx in inp_indices]]]
        gammas = [int(row.split(" ")[-1]) for row in all_rows[[idx + 15 for idx in inp_indices]]]
        print(betas)
        return list(zip(alphas, betas, gammas))


def rec(read_idx: int, alphas_betas_gammas: List[Tuple[int, int, int]],
        small_first: bool, z: int = 0, nbr: str = "") -> Optional[str]:
    # Idea: When alpha=26 do //26 and when alpha=1 do *26

    if read_idx == len(alphas_betas_gammas):
        return nbr if z == 0 else None

    alpha, beta, gamma = alphas_betas_gammas[read_idx]

    if alpha == 26:
        a = z % 26 + beta
        if (1 <= a <= 9):
            return rec(read_idx+1, alphas_betas_gammas, small_first, z//26, f"{nbr}{a}")
        return None

    assert alpha == 1
    core_z = z*26+gamma
    a_range = range(1, 10) if small_first else reversed(range(1, 10))
    a_forbidden = beta + z % 26
    for a in a_range:
        if a != a_forbidden:
            result = rec(read_idx+1, alphas_betas_gammas, small_first, core_z+a, f"{nbr}{a}")
            if result is not None:
                return result


def part_one(path: str) -> int:
    abg = _read_lines(path)
    return int(rec(0, abg, small_first=False))


def part_two(path: str) -> int:
    abg = _read_lines(path)
    return int(rec(0, abg, small_first=True))
