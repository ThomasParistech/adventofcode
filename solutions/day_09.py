# /usr/bin/python3
"""Day 9."""

from typing import List, Set, Tuple
import numpy as np
import time


def get_neighbors(i, j, shape) -> List[Tuple[int, int]]:
    res = []
    if i > 0:
        res.append((i-1, j))
    if j > 0:
        res.append((i, j-1))
    if i+1 < shape[0]:
        res.append((i+1, j))
    if j+1 < shape[1]:
        res.append((i, j+1))
    return res


def find_basins(np_rows: np.ndarray) -> Tuple[List[Tuple[int, int]], int]:
    basins = []
    sum = 0
    for (i, j), val in np.ndenumerate(np_rows):
        neighbors = get_neighbors(i, j, np_rows.shape)
        min_neighbor_val = np.min([np_rows[k][l] for (k, l) in neighbors])
        if val < min_neighbor_val:
            basins.append((i, j))
            sum += 1 + val
    return basins, sum


def _read_lines(path) -> Tuple[List[Set[int]], List[str]]:
    with open(path) as f:
        all_rows = f.readlines()
        all_rows = [list(row.strip()) for row in all_rows]

        np_rows = np.array(all_rows, dtype=int)
        return np_rows


def propagate_basin(i, j, np_rows, basin_ids, next_basin_id):
    basin_ids[i][j] = next_basin_id
    neighbors = get_neighbors(i, j, np_rows.shape)
    neighbors = [n for n in neighbors if basin_ids[n[0]][n[1]] == 0]
    val = np_rows[i][j]
    for (i_n, j_n) in neighbors:
        val_n = np_rows[i_n][j_n]
        if val < val_n:
            propagate_basin(i_n, j_n, np_rows, basin_ids, next_basin_id)


def part_one(path: str) -> int:
    np_rows = _read_lines(path)
    _, sum = find_basins(np_rows)
    return sum


def part_two(path: str) -> int:
    np_rows = _read_lines(path)
    basin_ids = np.zeros_like(np_rows)
    basin_ids[np_rows == 9] = -1  # 9 values don't belong to any basin

    basins, _ = find_basins(np_rows)
    next_basin_id = 1
    for (i, j) in basins:
        propagate_basin(i, j, np_rows, basin_ids, next_basin_id)
        next_basin_id += 1

    basins_size = sorted([np.sum(basin_ids == k) for k in range(next_basin_id)], reverse=True)
    return basins_size[0]*basins_size[1]*basins_size[2]
