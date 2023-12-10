# /usr/bin/python3
"""Day 10."""
import math
from dataclasses import dataclass
from functools import reduce
from typing import Dict
from typing import List
from typing import Set, Tuple, Optional

import numpy as np

from aoc.python.utils.parsing import read_lines
from aoc.python.utils.parsing import split_in_two

from aoc.python.utils.display import plot_int_array


def init_grid(path: str) -> Tuple[List[Optional[Tuple[int, int]]], int, int, int]:
    lines = read_lines(path)
    height, width = len(lines), len(lines[0])
    flat_grid: List[Optional[Tuple[int, int]]] = [None] * (height*width)

    def ij_to_key(i: int, j: int) -> int:
        if i < 0 or j < 0 or i >= height or j >= width:
            return -1
        return i * width + j

    start_ij = None
    for i, line in enumerate(lines):
        for j, c in enumerate(line):
            crt_key = ij_to_key(i, j)

            links = None
            if c == "|":
                links = (i-1, j), (i+1, j)
            elif c == "-":
                links = (i, j-1), (i, j+1)
            elif c == "L":
                links = (i-1, j), (i, j+1)
            elif c == "J":
                links = (i-1, j), (i, j-1)
            elif c == "7":
                links = (i+1, j), (i, j-1)
            elif c == "F":
                links = (i+1, j), (i, j+1)
            elif c == "S":
                start_ij = (i, j)

            if links is not None:
                flat_grid[crt_key] = (ij_to_key(*links[0]), ij_to_key(*links[1]))

    assert start_ij is not None
    start_key = ij_to_key(*start_ij)
    linked_neighbors_key = []
    for neighbor_ij in [(start_ij[0], start_ij[1]-1),
                        (start_ij[0], start_ij[1]+1),
                        (start_ij[0]-1, start_ij[1]),
                        (start_ij[0]+1, start_ij[1])]:
        neighbor_key = ij_to_key(*neighbor_ij)
        neighbor_neighbors = flat_grid[neighbor_key]
        if neighbor_neighbors is not None and start_key in neighbor_neighbors:
            linked_neighbors_key.append(neighbor_key)
    assert len(linked_neighbors_key) == 2, f"{len(linked_neighbors_key)=}"
    flat_grid[start_key] = (linked_neighbors_key[0], linked_neighbors_key[1])
    return flat_grid, start_key, height, width


def part_one(path: str) -> int:
    flat_grid, start_key, _, _ = init_grid(path)

    start_neighbor_keys = flat_grid[start_key]
    assert start_neighbor_keys is not None
    key_path: List[int] = [start_key, start_neighbor_keys[0]]

    while len(key_path) == 2 or key_path[-1] != start_key:
        neighbors = flat_grid[key_path[-1]]
        assert neighbors is not None

        neighbor_key = neighbors[0] if neighbors[0] != key_path[-2] else neighbors[1]
        key_path.append(neighbor_key)

    return math.floor((len(key_path)-1)/2)


def key_to_ij(key: int, width: int) -> Tuple[int, int]:
    i = math.floor(key / width)
    j = key - i * width
    return i, j


def part_two(path: str) -> int:
    flat_grid, start_key, height, width = init_grid(path)

    start_neighbor_keys = flat_grid[start_key]
    assert start_neighbor_keys is not None
    key_path: List[int] = [start_key, start_neighbor_keys[0]]

    labels = np.full((height, width), fill_value=-1, dtype=int)
    while len(key_path) == 2 or key_path[-1] != start_key:
        neighbors = flat_grid[key_path[-1]]
        assert neighbors is not None

        neighbor_key = neighbors[0] if neighbors[0] != key_path[-2] else neighbors[1]
        neighbor_i, neighbor_j = key_to_ij(neighbor_key, width)
        labels[neighbor_i, neighbor_j] = 1
        key_path.append(neighbor_key)

    plot_int_array(labels)
