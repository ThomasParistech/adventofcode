# /usr/bin/python3
"""Day 22."""


from typing import Dict, List, Tuple
import numpy as np
import bisect
from dataclasses import dataclass
from collections import defaultdict


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


def count_inside_vol(xinf, xsup, yinf, ysup, zinf, zsup, res):
    cube_mask = np.zeros((xsup-xinf, ysup-yinf, zsup-zinf), dtype=bool)

    for is_on, (xmin, xmax), (ymin, ymax), (zmin, zmax) in res:
        if xmax < xinf or ymax < yinf or zmax < zinf:
            continue
        if xmin > xsup or ymin > ysup or zmin > zsup:
            continue
        xmin, xmax = tuple(-xinf + np.clip((xmin, xmax), xinf, xsup-1))
        ymin, ymax = tuple(-yinf + np.clip((ymin, ymax), yinf, ysup-1))
        zmin, zmax = tuple(-zinf + np.clip((zmin, zmax), zinf, zsup-1))
        cube_mask[xmin:xmax+1, ymin:ymax+1, zmin:zmax+1] = is_on

    return int(np.sum(cube_mask))


def part_one(path: str) -> int:
    res = _read_lines(path)
    return count_inside_vol(-50, 51, -50, 51, -50, 51, res)


@dataclass
class Rect:
    x: int
    idx: int

    is_on: bool

    ymin: int
    ymax: int
    zmin: int
    zmax: int

    def __lt__(self, other: 'Rect'):
        return self.x < other.x


@dataclass
class Interval:
    y: int
    idx: int

    is_on: bool

    zmin: int
    zmax: int

    def __lt__(self, other: 'Interval'):
        return self.y < other.y

    @staticmethod
    def merge(intervals: List['Interval']) -> List[Tuple[int, int]]:
        merged_intervals: List[int] = []
        for active in intervals:
            idx_min = bisect.bisect_left(merged_intervals, active.zmin)
            idx_max = bisect.bisect_left(merged_intervals, active.zmax)

            if active.is_on:
                touch_left_min = idx_min != 0 and merged_intervals[idx_min-1] == active.zmin-1
                same_max = idx_max < len(merged_intervals) and merged_intervals[idx_max] == active.zmax
                touch_right_max = idx_max < len(merged_intervals) and merged_intervals[idx_max] == active.zmax+1

                n_removals = idx_max-idx_min
                for _ in range(n_removals):
                    merged_intervals.pop(idx_min)

                if idx_max % 2 == 0:  # insert ...] before [
                    if same_max or touch_right_max:
                        merged_intervals.pop(idx_max-n_removals)
                    else:
                        merged_intervals.insert(idx_max-n_removals, active.zmax)
                if idx_min % 2 == 0:  # insert [... before [
                    if touch_left_min:
                        merged_intervals.pop(idx_min-1)
                    else:
                        merged_intervals.insert(idx_min, active.zmin)
            else:
                same_max = idx_max < len(merged_intervals) and merged_intervals[idx_max] == active.zmax

                n_removals = idx_max-idx_min
                for _ in range(n_removals):
                    merged_intervals.pop(idx_min)

                if idx_max % 2 == 1:  # insert ...] before ] to make shorter
                    if same_max:
                        merged_intervals.pop(idx_max-n_removals)
                    else:
                        merged_intervals.insert(idx_max-n_removals, active.zmax+1)
                elif same_max:
                    merged_intervals[idx_max-n_removals] += 1

                if idx_min % 2 == 1:  # insert [... before ] to make shorter
                    merged_intervals.insert(idx_min, active.zmin-1)

        assert len(merged_intervals) % 2 == 0
        return list(zip(merged_intervals[::2], merged_intervals[1::2]))

    @staticmethod
    def test():
        input_intervals = [[(-30, 40), (-42, -35)],  # [ ] { }
                           [(-30, 40), (-42, -30)],  # [ ]x{ }
                           [(-30, 40), (-42, -25)],  # [ { ] }
                           [(-30, 40), (-30, -25)],  # {x[ ]  }
                           [(-30, 40), (10, 20)],    # { [] }
                           [(-30, 40), (10, 40)],    # { []x}
                           [(-30, 40), (10, 50)],    # { [ } ]
                           [(-30, 40), (40, 50)],    # { }x[ ]
                           [(-30, 40), (42, 55)]]    # { } [ ]

        # ON ON
        gt_on_on = [[(-42, -35), (-30, 40)],  # [ ] { }
                    [(-42, 40)],  # [ ]x{ }
                    [(-42, 40)],  # [ { ] }
                    [(-30, 40)],  # {x[ ]  }
                    [(-30, 40)],    # { [] }
                    [(-30, 40)],    # { []x}
                    [(-30, 50)],    # { [ } ]
                    [(-30, 50)],    # { }x[ ]
                    [(-30, 40), (42, 55)]]    # { } [ ]

        # ON OFF
        gt_on_off = [[(-30, 40)],  # [ ] { }
                     [(-29, 40)],  # [ ]x{ }
                     [(-24, 40)],  # [ { ] }
                     [(-24, 40)],  # {x[ ]  }
                     [(-30, 9), (21, 40)],    # { [] }
                     [(-30, 9)],    # { []x}
                     [(-30, 9)],    # { [ } ]
                     [(-30, 39)],    # { }x[ ]
                     [(-30, 40)]]    # { } [ ]

        for is_on, gt in zip([True, False], [gt_on_on, gt_on_off]):
            for inters_in, inters_out in zip(input_intervals, gt):
                active_intervals = [
                    Interval(y=-41, idx=5, is_on=True, zmin=inters_in[0][0], zmax=inters_in[0][1]),
                    Interval(y=-27, idx=1, is_on=is_on, zmin=inters_in[1][0], zmax=inters_in[1][1])]
                assert Interval.merge(active_intervals) == inters_out, f"Failed for {inters_in=}, {inters_out=} "


def line_sweep(intervals_sorted_by_y: Dict[int, List[Interval]]) -> int:
    area = 0

    last_y = 0
    last_length = 0
    active_intervals: List[Interval] = []
    for y, inters in intervals_sorted_by_y.items():
        area += last_length*(y-last_y)
        # Remove closing intervals
        for new_inter in inters:
            inter_to_close = [pos for pos, inter in enumerate(active_intervals)
                              if inter.idx == new_inter.idx]
            if len(inter_to_close) != 0:
                active_intervals.pop(inter_to_close[0])
            else:
                active_intervals.append(new_inter)
        active_intervals.sort(key=lambda seg: seg.idx)  # Start by old info and overwrite it with newer info

        # Merge active open intervals
        merged_intervals = np.array(Interval.merge(active_intervals), dtype=int)

        # Compute length
        if len(merged_intervals) == 0:
            last_length = 0
        else:
            last_length = np.sum(merged_intervals[:, 1] - merged_intervals[:, 0] + 1)
        last_y = y

    return area


def part_two(path: str) -> int:
    # Interval.test()
    # exit()

    res = _read_lines(path)

    # Sort by X
    rects: List[Rect] = []
    for idx, (is_on, (xmin, xmax), (ymin, ymax), (zmin, zmax)) in enumerate(res):
        for x in [xmin, xmax+1]:
            rects.append(Rect(idx=idx,
                              x=x,
                              is_on=is_on,
                              ymin=ymin,
                              ymax=ymax,
                              zmin=zmin,
                              zmax=zmax))

    rects.sort()
    rects_sorted_by_x = defaultdict(list)
    for rect in rects:
        rects_sorted_by_x[rect.x].append(rect)

    # Plane sweep
    volume = 0

    last_x = 0
    last_area = 0
    active_rects: List[Rect] = []
    for x, rects in rects_sorted_by_x.items():
        volume += last_area*(x-last_x)

        # Remove closing rects
        for new_rect in rects:
            rects_to_close = [pos for pos, rect in enumerate(active_rects)
                              if rect.idx == new_rect.idx]
            if len(rects_to_close) != 0:
                active_rects.pop(rects_to_close[0])
            else:
                active_rects.append(new_rect)
        active_rects.sort(key=lambda box: box.idx)  # Start by old info and overwrite it with newer info

        ########

        intervals = []
        for rect in active_rects:
            for y in [rect.ymin, rect.ymax+1]:
                intervals.append(Interval(y=y,
                                          idx=rect.idx,
                                          is_on=rect.is_on,
                                          zmin=rect.zmin,
                                          zmax=rect.zmax))
        intervals.sort()
        intervals_sorted_by_y = defaultdict(list)
        for inter in intervals:
            intervals_sorted_by_y[inter.y].append(inter)

        last_area = line_sweep(intervals_sorted_by_y)
        last_x = x

    return volume
