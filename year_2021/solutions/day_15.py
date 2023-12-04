# /usr/bin/python3
# type: ignore
"""Day 15."""

from typing import List
from typing import Optional
from typing import Tuple

import numpy as np


def _read_lines(path):
    with open(path) as f:
        all_rows = f.readlines()
        grid_risks = np.array([list(row.strip()) for row in all_rows], dtype=int)
        return grid_risks


def backtrack(grid_risks: np.ndarray, mask_free: np.ndarray, i: int, j: int, sum_risks: int) -> Optional[int]:
    sum_risks += grid_risks[i, j]

    if i == mask_free.shape[0]-1 and j == mask_free.shape[1]-1:
        return sum_risks

    neighbors = []
    if i > 0 and mask_free[i-1, j]:
        neighbors.append((i-1, j))
    if i+1 < mask_free.shape[0] and mask_free[i+1, j]:
        neighbors.append((i+1, j))
    if j > 0 and mask_free[i, j-1]:
        neighbors.append((i, j-1))
    if j+1 < mask_free.shape[1] and mask_free[i, j+1]:
        neighbors.append((i, j+1))

    results = []
    for n in neighbors:
        mask_free[n[0], n[1]] = False
        res = backtrack(grid_risks, mask_free, n[0], n[1], sum_risks)
        if res is not None:
            results.append(res)
        mask_free[n[0], n[1]] = True

    if len(results) == 0:
        return None

    return np.min(results)


def ij_to_hash(i, j, width):
    return i*width+j


def hash_to_ij(hash, width):
    return hash//width, hash % width


def get_4_neighbors(i, j, shape) -> List[Tuple[int, int]]:
    neighbors = []
    if i > 0:
        neighbors.append((i-1, j))
    if i+1 < shape[0]:
        neighbors.append((i+1, j))
    if j > 0:
        neighbors.append((i, j-1))
    if j+1 < shape[1]:
        neighbors.append((i, j+1))
    return neighbors


def dijkstras(grid_risks: np.ndarray) -> int:
    height, width = grid_risks.shape
    mask_unknown = np.ones_like(grid_risks, dtype=bool)

    tmp_distances_dict = {0: 0}
    while len(tmp_distances_dict) != 0:
        vertex_to_add = min(tmp_distances_dict.keys(), key=(lambda k: tmp_distances_dict[k]))
        dist = tmp_distances_dict.pop(vertex_to_add)
        i, j = hash_to_ij(vertex_to_add, width)
        # print(f"{i},{j} => {dist}")
        mask_unknown[i, j] = False

        if i == height-1 and j == width-1:
            return dist

        # Propagate
        neighbors = get_4_neighbors(i, j, grid_risks.shape)
        for i_n, j_n in neighbors:
            if mask_unknown[i_n, j_n]:
                new_dist = dist + grid_risks[i_n, j_n]
                hash_n = ij_to_hash(i_n, j_n, width)
                if hash_n in tmp_distances_dict:
                    tmp_distances_dict[hash_n] = min(new_dist, tmp_distances_dict[hash_n])
                else:
                    tmp_distances_dict[hash_n] = new_dist


def part_one(path: str) -> int:
    grid_risks = _read_lines(path)

    # mask_free = np.ones_like(grid_risks, dtype=bool)
    # sum_risks = backtrack(grid_risks, mask_free, 0, 0, 0)
    # answer = sum_risks - grid_risks[0, 0]

    return dijkstras(grid_risks)


def part_two(path: str) -> int:
    grid_risks = _read_lines(path)
    grid_risks = np.concatenate([1+np.mod(grid_risks+k-1, 9) for k in range(5)], axis=1)
    grid_risks = np.concatenate([1+np.mod(grid_risks+k-1, 9) for k in range(5)], axis=0)

    return dijkstras(grid_risks)
