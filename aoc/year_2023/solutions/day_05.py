# /usr/bin/python3
"""Day 5."""
from dataclasses import dataclass
from typing import List
from typing import Tuple

from aoc.python.utils.parsing import read
from aoc.python.utils.parsing import split_in_three_ints
from aoc.python.utils.parsing import split_list_int


@dataclass
class Map:
    data: List[Tuple[int, int, int]]  # Begin, End, Dst_begin

    @staticmethod
    def from_str(block: str) -> 'Map':
        data: List[Tuple[int, int, int]] = []
        for triplet in block.split('\n'):
            dst_begin, src_begin, length = split_in_three_ints(triplet, " ")
            data.append((src_begin, src_begin+length, dst_begin))
        return Map(sorted(data))

    def eval_single_value(self, val: int) -> int:
        for src_begin, src_end, dst_begin in self.data:
            if src_begin <= val < src_end:
                return dst_begin + val - src_begin
        return val

    def eval_intervals(self, intervals: List[Tuple[int, int]]) -> List[Tuple[int, int]]:
        dst_intervals: List[Tuple[int, int]] = []

        for src_begin, src_end, dst_begin in self.data:
            tmp_intervals = []
            for i_begin, i_end in intervals:
                # Left
                if i_begin < src_begin:
                    tmp_intervals.append((i_begin, min(i_end, src_begin)))

                # Right
                if i_end > src_end:
                    tmp_intervals.append((max(i_begin, src_end), i_end))

                # Middle
                mid_begin, mid_end = max(src_begin, i_begin), min(src_end, i_end)
                if mid_begin < mid_end:
                    dst_intervals.append((mid_begin+dst_begin-src_begin,
                                          mid_end+dst_begin-src_begin))
            intervals = tmp_intervals

        # Add remaining intervals
        dst_intervals += intervals

        # Sort and merge intervals
        dst_intervals = sorted(dst_intervals)
        merged_intervals: List[Tuple[int, int]] = []
        for begin, end in dst_intervals:
            if len(merged_intervals) == 0:
                merged_intervals.append((begin, end))
            else:
                last_begin, last_end = merged_intervals[-1]
                if last_end >= begin:
                    merged_intervals[-1] = (last_begin, max(last_end, end))
                else:
                    merged_intervals.append((begin, end))

        return merged_intervals

    @staticmethod
    def iterative_eval_single_value(maps: List['Map'], val: int) -> int:
        for map in maps:
            val = map.eval_single_value(val)
        return val

    @staticmethod
    def iterative_eval_intervals(maps: List['Map'], intervals: List[Tuple[int, int]]) -> List[Tuple[int, int]]:
        for map in maps:
            intervals = map.eval_intervals(intervals)
        return intervals


def part_one(path: str) -> int:
    blocks = read(path).split("\n\n")
    blocks = [b.split(":")[-1].strip() for b in blocks]
    seeds = split_list_int(blocks[0], " ")
    maps = [Map.from_str(b) for b in blocks[1:]]
    return min(Map.iterative_eval_single_value(maps, s) for s in seeds)


def part_two(path: str) -> int:
    blocks = read(path).split("\n\n")
    blocks = [b.split(":")[-1].strip() for b in blocks]
    _seeds_ints = split_list_int(blocks[0], " ")
    seed_intervals = [(_seeds_ints[2*k], _seeds_ints[2*k]+_seeds_ints[2*k+1])
                      for k in range(len(_seeds_ints)//2)]

    maps = [Map.from_str(b) for b in blocks[1:]]
    return Map.iterative_eval_intervals(maps, seed_intervals)[0][0]
