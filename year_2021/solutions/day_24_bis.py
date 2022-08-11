# /usr/bin/python3
"""Day 24."""

from typing import List, Optional
import numpy as np


def _read_lines(path):
    with open(path) as f:
        all_rows = np.array([row.strip() for row in f.readlines()])
        inp_indices = [idx for idx, row in enumerate(all_rows) if len(row.split(" ")) == 2]
        alphas = [int(row.split(" ")[-1]) for row in all_rows[[idx + 4 for idx in inp_indices]]]
        betas = [int(row.split(" ")[-1]) for row in all_rows[[idx + 5 for idx in inp_indices]]]
        gammas = [int(row.split(" ")[-1]) for row in all_rows[[idx + 15 for idx in inp_indices]]]

        return alphas, betas, gammas


class RevertNode:
    def __init__(self, z: int, depth: int):
        self.z: int = z
        self.depth: int = depth

    def find_parents(self, small_first: bool, nbr: str, alphas: List[int], betas: List[int], gammas: List[int]) -> Optional[int]:
        prev_depth = self.depth - 1
        if prev_depth == -1:
            return int(nbr)

        alpha = alphas[prev_depth]
        beta = betas[prev_depth]
        gamma = gammas[prev_depth]

        a_z_to_add = []
        if alpha == 1:
            # Failing test
            prev_z = self.z // 26
            prev_a = self.z % 26 - gamma
            if (prev_a != beta + prev_z % 26) and (1 <= prev_a <= 9):
                a_z_to_add.append((prev_a, prev_z))

            # Passing test
            prev_z = self.z
            prev_a = beta + prev_z % 26
            if 1 <= prev_a <= 9:
                a_z_to_add.append((prev_a, prev_z))

        else:  # alpha=26
            # Failing test
            prev_a = self.z % 26 - gamma
            if 1 <= prev_a <= 9:
                core_prev_z = 26*(self.z // 26)
                for mod_z in range(26):
                    prev_z = core_prev_z + mod_z
                    if (prev_a != beta + prev_z % 26):
                        a_z_to_add.append((prev_a, prev_z))
            # Passing test
            a_range = range(max(1, beta), 10) if small_first else range(9, max(0, beta-1), -1)
            for prev_a in a_range:
                prev_z = 26*self.z + prev_a - beta
                a_z_to_add.append((prev_a, prev_z))

        for prev_a, prev_z in a_z_to_add:
            parent = RevertNode(prev_z, prev_depth)
            res = parent.find_parents(small_first, f"{prev_a}{nbr}", alphas, betas, gammas)
            if res is not None:
                return res
        return None


def part_one(path: str) -> int:
    alphas, betas, gammas = _read_lines(path)
    return RevertNode(0, 14).find_parents(False, "", alphas, betas, gammas)


def part_two(path: str) -> int:
    alphas, betas, gammas = _read_lines(path)
    return RevertNode(0, 14).find_parents(True, "", alphas, betas, gammas)
