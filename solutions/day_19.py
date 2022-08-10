# /usr/bin/python3
"""Day 19 Optimized!"""

from typing import List, Tuple, Optional
import numpy as np
from itertools import permutations
import copy


def _read_lines(path):
    with open(path) as f:
        all_rows = f.readlines()+[""]
        starts = 1 + np.array([idx for idx, row in enumerate(all_rows)
                               if row.startswith("---")])
        ends = -2+np.roll(starts, -1)

        scans = [Scan(np.array([row.strip().split(",") for row in all_rows[start:end]], dtype=int))
                 for start, end in zip(starts, ends)]
        return scans


def get_best_diff(a: np.ndarray, b: np.ndarray) -> Tuple[int, np.int16]:
    diff = b[:, None, :] - a[None, :, :]  # Shape (lenB, lenA, 3)
    diff = diff.reshape(-1, 3)
    diff = np.c_[np.zeros(diff.shape[0]), diff].astype(np.int16)
    diff = np.asarray(diff, order='C')  # Require diff.data.c_contiguous set to True
    diff = diff.view(np.uint64)  # hash

    unique, counts = np.unique(diff, return_counts=True)
    best_idx = np.argmax(counts)
    best_count = counts[best_idx]
    best_vec3 = unique[[best_idx]].view(np.int16)[1:]

    return best_count, best_vec3


def test_all_comparisons(a: np.ndarray, b: np.ndarray) -> Optional[Tuple[np.ndarray, np.ndarray]]:
    """Return version of a that is aligned with b"""
    for xyz in permutations([0, 1, 2]):
        for sign_x in [1, -1]:
            for sign_y in [1, -1]:
                sign_z = sign_x*sign_y
                if (xyz[0]+1) % 3 != xyz[1]:
                    sign_z *= -1
                c = copy.deepcopy(a[:, xyz])
                c[:, 0] *= sign_x
                c[:, 1] *= sign_y
                c[:, 2] *= sign_z
                best_count, best_vec3 = get_best_diff(c, b)
                if best_count >= 12:  # Need at least 12 points in common
                    return c + best_vec3, best_vec3
    return None


class Scan:
    def __init__(self, pts: np.ndarray) -> None:
        self.points = pts
        self.origin = np.zeros(3, dtype=np.int16)

    def try_align(self, other: 'Scan') -> bool:
        res = test_all_comparisons(self.points, other.points)
        if res is None:
            return False

        self.points, self.origin = res
        return True

    def try_align_with_all(self, self_id: int, test_ids: List[int], scans: List['Scan'],
                           scans_ij_done: np.ndarray) -> bool:
        for known_id in test_ids:
            if not scans_ij_done[self_id, known_id]:
                scans_ij_done[self_id, known_id] = True
                scans_ij_done[known_id, self_id] = True

                if self.try_align(scans[known_id]):
                    return True
        return False

    @staticmethod
    def align_scans_inplace(scans: List['Scan']):
        aligned_ids = [0]
        waiting_ids = list(range(1, len(scans)))

        scans_ij_done = np.zeros((len(scans), len(scans)), dtype=bool)
        while len(waiting_ids) != 0:
            # print(aligned_ids, waiting_ids)
            for new_id in waiting_ids:
                success = scans[new_id].try_align_with_all(new_id, aligned_ids, scans, scans_ij_done)
                if success:
                    waiting_ids.remove(new_id)
                    aligned_ids.append(new_id)

    @staticmethod
    def count_points(scans: List['Scan']) -> int:
        all_pts = np.concatenate([scan.points for scan in scans])
        all_pts = np.c_[np.zeros(all_pts.shape[0]), all_pts].astype(np.int16)
        # diff = np.asarray(diff, order='C')  # Require diff.data.c_contiguous set to True
        all_pts = all_pts.view(np.uint64)  # hash
        return np.unique(all_pts).shape[0]

    @staticmethod
    def max_l1(scans: List['Scan']) -> int:
        origins = np.stack([scan.origin for scan in scans])
        diff = origins[:, None, :] - origins[None, :, :]
        return np.max(np.sum(np.abs(diff), axis=-1))


def part_one(path: str) -> int:
    scans = _read_lines(path)
    Scan.align_scans_inplace(scans)
    return Scan.count_points(scans)


def part_two(path: str) -> int:
    scans = _read_lines(path)
    Scan.align_scans_inplace(scans)
    return Scan.max_l1(scans)
