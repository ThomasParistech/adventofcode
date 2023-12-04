# /usr/bin/python3
# type: ignore
"""Day 5."""

import numpy as np

grid_size = 1000


class Line2d:
    def __init__(self, pt1, pt2):
        x1, y1 = tuple(pt1)
        x2, y2 = tuple(pt2)

        # Bounding box
        self.xmin = min(x1, x2)
        self.xmax = max(x1, x2)
        self.ymin = min(y1, y2)
        self.ymax = max(y1, y2)

        # Slope
        self.increasing = (x1 < x2) == (y1 < y2)

    def add_points(self, counts, use_diagonal):
        if self.xmin == self.xmax:  # Vertical
            for y in range(self.ymin, self.ymax+1):
                counts[y][self.xmin] += 1
        elif self.ymin == self.ymax:  # Horizontal
            for x in range(self.xmin, self.xmax+1):
                counts[self.ymin][x] += 1
        elif use_diagonal:
            diff = self.ymax - self.ymin
            if self.increasing:
                for k in range(diff+1):
                    counts[self.ymin+k][self.xmin+k] += 1
            else:
                for k in range(diff+1):
                    counts[self.ymax-k][self.xmin+k] += 1


def _read_lines(path):
    with open(path) as f:
        all_rows = f.readlines()

        lines_2d = []
        for row in all_rows:
            row = row.strip().split(' -> ')
            pts = [np.array(row[k].split(','), dtype=int) for k in [0, 1]]
            lines_2d.append(Line2d(pts[0], pts[1]))
        return lines_2d


def part_one(path: str) -> int:
    lines_2d = _read_lines(path)
    counts = np.zeros((grid_size, grid_size), dtype=int)
    for line in lines_2d:
        line.add_points(counts, False)

    return np.sum(counts >= 2)


def part_two(path: str) -> int:
    lines_2d = _read_lines(path)
    counts = np.zeros((grid_size, grid_size), dtype=int)
    for line in lines_2d:
        line.add_points(counts, True)

    return np.sum(counts >= 2)
