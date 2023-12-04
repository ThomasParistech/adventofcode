# /usr/bin/python3
# type: ignore
"""Day 8."""

from typing import List
from typing import Set
from typing import Tuple

import numpy as np


class Solver:
    def __init__(self, list_seg: List[Set[int]]):
        self.signal_to_truth = [set(range(7)) for _ in range(7)]
        self.truth_to_signal = [set(range(7)) for _ in range(7)]

        dict_seg_by_size = {k: [] for k in [2, 3, 4, 5, 6, 7]}
        for seg in list_seg:
            dict_seg_by_size[len(seg)].append(seg)

        # Size 2 - Remove everything except cf
        self._remove_indices(dict_seg_by_size[2][0], [0, 1, 3, 4, 6])

        # Size 3 - Remove everything except acf
        self._remove_indices(dict_seg_by_size[3][0], [1, 3, 4, 6])

        # Size 4 - Remove everything except bcdf
        self._remove_indices(dict_seg_by_size[4][0], [0, 4, 6])

        # Size 5
        counts = {k: 0 for k in range(7)}
        for seg in dict_seg_by_size[5]:
            for k in seg:
                counts[k] += 1

        letters_by_counts = {k: set() for k in [1, 2, 3]}
        for l, c in counts.items():
            letters_by_counts[c].add(l)

        self._remove_indices(letters_by_counts[1], [0, 2, 3, 5, 6])  # everything Remove except be
        self._remove_indices(letters_by_counts[2], [0, 1, 3, 4, 6])  # everything Remove except cf
        self._remove_indices(letters_by_counts[3], [1, 2, 4, 5])  # everything Remove except adg

        # Size 6
        counts = {k: 0 for k in range(7)}
        for seg in dict_seg_by_size[6]:
            for k in seg:
                counts[k] += 1

        letters_by_counts = {k: set() for k in [2, 3]}
        for l, c in counts.items():
            letters_by_counts[c].add(l)

        self._remove_indices(letters_by_counts[2], [0, 1, 5, 6])  # everything Remove except cde

        # Size 7 - No information

        # Refinement
        self._refine()
        assert all(len(s) == 1 for s in self.signal_to_truth)
        assert all(len(s) == 1 for s in self.truth_to_signal)

    def _remove_indices(self, segments: Set[int], list_indices: List[int]):
        for bad in list_indices:
            for signal in segments:
                if bad in self.signal_to_truth[signal]:
                    self.signal_to_truth[signal].remove(bad)
                if signal in self.truth_to_signal[bad]:
                    self.truth_to_signal[bad].remove(signal)

    def _refine(self):
        signals_to_check = [idx for idx, s in enumerate(self.signal_to_truth) if len(s) == 1]
        truths_to_check = [idx for idx, s in enumerate(self.truth_to_signal) if len(s) == 1]

        def try_and_remove(my_set: Set[int], idx: int) -> bool:
            if not idx in my_set:
                return False
            my_set.remove(idx)
            return len(my_set) == 1

        while len(signals_to_check) != 0 or len(truths_to_check) != 0:
            tmp_sig = []
            for i_sig in signals_to_check:
                j_truth = tuple(self.signal_to_truth[i_sig])[0]
                for i in range(7):
                    if i != i_sig:
                        if try_and_remove(self.signal_to_truth[i], j_truth):
                            tmp_sig.append(i)
                        if try_and_remove(self.truth_to_signal[j_truth], i):
                            truths_to_check.append(j_truth)
            signals_to_check = tmp_sig

            tmp_truth = []
            for j_truth in truths_to_check:
                i_sig = tuple(self.truth_to_signal[j_truth])[0]
                for j in range(7):
                    if j != j_truth:
                        if try_and_remove(self.signal_to_truth[i_sig], j):
                            signals_to_check.append(i_sig)
                        if try_and_remove(self.truth_to_signal[j], i_sig):
                            tmp_truth.append(j)
            truths_to_check = tmp_truth

    def guess_4_digits_value(self, list_str: List[str]) -> int:
        assert len(list_str) == 4

        digits_dict = {"abcefg": "0",
                       "cf": "1",
                       "acdeg": "2",
                       "acdfg": "3",
                       "bcdf": "4",
                       "abdfg": "5",
                       "abdefg": "6",
                       "acf": "7",
                       "abcdefg": "8",
                       "abcdfg": "9"
                       }
        correct_segments = []
        for bad_str in list_str:
            correct_segment = ""
            for bad_c in bad_str:
                bad_idx = ord(bad_c)-ord('a')
                correct_idx = tuple(self.signal_to_truth[bad_idx])[0]
                correct_segment += chr(correct_idx+ord('a'))
            correct_segments.append("".join(sorted(correct_segment)))

        # print(f"Input: {list_str}")
        # print(f"   --> {correct_segments}")

        digits = [digits_dict[segments] for segments in correct_segments]
        val = int("".join(digits))
        # print(val)
        return val


def _read_lines(path) -> Tuple[List[Set[int]], List[str]]:
    with open(path) as f:
        all_rows = f.readlines()

        signals = []
        out_digits = []
        for row in all_rows:
            left, right = tuple(row.strip().split(' | '))
            signals.append([set(ord(c) - ord('a') for c in s) for s in left.split(' ')])
            out_digits.append(["".join(sorted(s)) for s in right.split(' ')])

        return signals, out_digits


def part_one(path: str) -> int:
    _, out_digits = _read_lines(path)

    count_uniques = 0
    for vec in out_digits:
        for s in vec:
            if len(s) in (2, 3, 4, 7):
                count_uniques += 1
    return count_uniques


def part_two(path: str) -> int:
    signals, out_digits = _read_lines(path)
    sum = np.sum([Solver(signals_vec).guess_4_digits_value(out_digits_vec)
                 for signals_vec, out_digits_vec in zip(signals, out_digits)])
    return sum
