# /usr/bin/python3
"""Day 22."""

from typing import List, Set, Tuple
import numpy as np


def _read_lines(path):
    with open(path) as f:
        all_rows = f.readlines()
        res = []
        for row in all_rows:
            row = row.strip()
            if row.startswith("on "):
                row = row.replace("on ", '')
                is_on = True
            else:
                row = row.replace("off ", '')
                is_on = False
            x, y, z = (tuple(int(val) for val in el[2:].split('..')) for el in row.split(','))
            res.append((is_on, x, y, z))

        return res


def part_one(path: str) -> int:
    res = _read_lines(path)
    cube_mask = np.zeros((101, 101, 101), dtype=bool)

    for is_on, (xmin, xmax), (ymin, ymax), (zmin, zmax) in res:
        if xmax < -50 or ymax < -50 or zmax < -50:
            continue
        if xmin > 50 or ymin > 50 or zmin > 50:
            continue
        xmin, xmax = tuple(50 + np.clip((xmin, xmax), -50, 50))
        ymin, ymax = tuple(50 + np.clip((ymin, ymax), -50, 50))
        zmin, zmax = tuple(50 + np.clip((zmin, zmax), -50, 50))
        cube_mask[xmin:xmax+1, ymin:ymax+1, zmin:zmax+1] = is_on

    return int(np.sum(cube_mask))


def part_two(path: str) -> int:
    #
    #
    #
    #
    #
    #
    #     TODO
    #
    #
    #
    #
    #
    #
    #
    return 0
