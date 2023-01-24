# /usr/bin/python3
"""Day 12."""

from typing import List, Tuple, Dict
import numpy as np


def _read_lines(path: str) -> Tuple[np.ndarray, Tuple[int, int], Tuple[int, int]]:
    with open(path) as f:
        hmap = np.array([list(map(ord, row.strip())) for row in f.readlines()]).astype(int)
        e_ij = tuple(map(int, np.unravel_index(np.argmin(hmap), hmap.shape)))
        hmap[e_ij[0], e_ij[1]] = ord("z")
        s_ij = tuple(map(int, np.unravel_index(np.argmin(hmap), hmap.shape)))
        hmap[s_ij[0], s_ij[1]] = ord("a")

        hmap -= ord("a")
        return hmap, s_ij, e_ij


def _get_4_neighbors(i: int, j: int, shape: Tuple[int, ...]) -> List[Tuple[int, int]]:
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


def part_one(path: str) -> int:
    hmap, s_ij, e_ij = _read_lines(path)
    mask_unknown = np.ones(hmap.shape, dtype=bool)
    distmap = np.zeros(hmap.shape, dtype=int)

    djikstra_set: Dict[Tuple[int, int], int] = {s_ij: 0}  # 2D index -> Distance

    while len(djikstra_set) != 0:
        vertex_to_add = min(djikstra_set.keys(), key=(lambda k: djikstra_set[k]))
        dist = djikstra_set.pop(vertex_to_add)
        i, j = vertex_to_add
        mask_unknown[i, j] = False
        distmap[i, j] = dist

        if vertex_to_add == e_ij:
            # import matplotlib.pyplot as plt
            # plt.ioff()
            # plt.matshow(hmap)
            # plt.matshow(distmap)
            # plt.show()
            return dist

        # Propagate
        href = hmap[i, j]
        neighbors = _get_4_neighbors(i, j, hmap.shape)
        neighbors = [(i, j) for i, j in neighbors if hmap[i, j] <= href+1]
        for ij_n in neighbors:
            i_n, j_n = ij_n
            if mask_unknown[i_n, j_n]:
                new_dist = dist + 1
                if ij_n in djikstra_set:
                    djikstra_set[ij_n] = min(new_dist, djikstra_set[ij_n])
                else:
                    djikstra_set[ij_n] = new_dist

    return -1


def part_two(path: str) -> int:
    hmap, _, e_ij = _read_lines(path)
    mask_unknown = np.ones(hmap.shape, dtype=bool)
    distmap = np.zeros(hmap.shape, dtype=int)
    mask_a = hmap == 0

    # Start from end instead
    djikstra_set: Dict[Tuple[int, int], int] = {e_ij: 0}  # 2D index -> Distance

    while len(djikstra_set) != 0:
        vertex_to_add = min(djikstra_set.keys(), key=(lambda k: djikstra_set[k]))
        dist = djikstra_set.pop(vertex_to_add)
        i, j = vertex_to_add
        mask_unknown[i, j] = False
        distmap[i, j] = dist

        if mask_a[i, j]:
            # import matplotlib.pyplot as plt
            # plt.ioff()
            # plt.matshow(hmap)
            # plt.matshow(mask_a)
            # plt.matshow(distmap)
            # plt.show()
            return dist

        # Propagate
        href = hmap[i, j]
        neighbors = _get_4_neighbors(i, j, hmap.shape)
        neighbors = [(i, j) for i, j in neighbors if hmap[i, j] >= href-1]
        for ij_n in neighbors:
            i_n, j_n = ij_n
            if mask_unknown[i_n, j_n]:
                new_dist = dist + 1
                if ij_n in djikstra_set:
                    djikstra_set[ij_n] = min(new_dist, djikstra_set[ij_n])
                else:
                    djikstra_set[ij_n] = new_dist

    return -1
