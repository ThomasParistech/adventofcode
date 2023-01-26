# /usr/bin/python3
"""Day 15."""

import matplotlib.pyplot as plt
from typing import List, Tuple
import numpy as np

from dataclasses import dataclass


@dataclass
class Sensor:
    x: int
    y: int
    beacon_x: int
    beacon_y: int
    beacon_dist: int = 0

    def __post_init__(self) -> None:
        self.beacon_dist = abs(self.beacon_x-self.x) + abs(self.beacon_y-self.y)


def _read_lines(path: str) -> Tuple[int,  List[Sensor]]:
    with open(path) as f:
        y_row = int(f.readline().strip().split("=")[-1])
        sensors: List[Sensor] = []
        for row in f.readlines():
            scan, beacon = row.strip().split(': closest beacon is at x=')
            x, y = tuple(map(int, scan.split("Sensor at x=")[-1].split(", y=")))
            beacon_x, beacon_y = tuple(map(int, beacon.split(", y=")))
            sensors.append(Sensor(x=x,
                                  y=y,
                                  beacon_x=beacon_x,
                                  beacon_y=beacon_y))
        return y_row, sensors


def _is_overlapping(a: Tuple[int, int], b: Tuple[int, int]) -> bool:
    return a[1] >= b[0] and b[1] >= a[0]


def _merge_intervals(intervals: List[Tuple[int, int]]) -> List[Tuple[int, int]]:
    final_intervals = []
    while len(intervals) != 0:
        inter_ref = intervals[-1]

        tmp_intervals, overlapping = [], []
        for inter in intervals:
            if _is_overlapping(inter, inter_ref):
                overlapping.append(inter)
            else:
                tmp_intervals.append(inter)

        if len(overlapping) == 1:
            final_intervals.append(intervals.pop())
        else:
            xmin = np.min([inter[0] for inter in overlapping])
            xmax = np.max([inter[1] for inter in overlapping])
            tmp_intervals.append((xmin, xmax))
            intervals = tmp_intervals
    return final_intervals


def part_one(path: str) -> int:
    y_row, sensors = _read_lines(path)

    # Find intervals
    intervals = []
    for s in sensors:
        dx = s.beacon_dist - abs(s.y - y_row)
        if dx >= 0:
            intervals.append((s.x-dx, s.x+dx))

    # Merge intervals
    final_intervals = _merge_intervals(intervals)
    count = np.sum([inter[1]-inter[0]+1 for inter in final_intervals])

    # Remove Beacons
    x_beacons = set([s.beacon_x for s in sensors if s.beacon_y == y_row])
    count -= np.count_nonzero([inter[0] <= x <= inter[1]
                               for inter in final_intervals
                               for x in x_beacons])

    return count


def part_two(path: str) -> int:
    y_row, sensors = _read_lines(path)
    mini, maxi = 0, 2*y_row

    for k in range(y_row):
        for y in [y_row - k, y_row + k]:
            # Find intervals
            intervals = []
            for s in sensors:
                dx = s.beacon_dist - abs(s.y - y)
                if dx >= 0:
                    if s.x+dx >= mini and s.x-dx <= maxi:
                        start = max(mini, s.x-dx)
                        end = min(maxi, s.x+dx)
                        intervals.append((start, end))
            merged = _merge_intervals(intervals)
            if len(merged) > 1:
                assert len(merged) == 2, merged
                x = merged[0][1]+1 if merged[0][0] < merged[1][0] else merged[0][0]-1
                return y + 4000000*x

    return -1
