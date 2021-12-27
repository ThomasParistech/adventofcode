# /usr/bin/python3
"""Day 19."""

from typing import List, Set, Tuple, Optional
import numpy as np
from itertools import permutations
from dataclasses import dataclass
import copy


def get_scan_pose_permutations() -> Tuple[np.ndarray, np.ndarray]:
    perms, signs = [], []

    for xyz in permutations([0, 1, 2]):
        for sign_x in [1, -1]:
            for sign_y in [1, -1]:
                sign_z = sign_x*sign_y
                if (xyz[0]+1) % 3 != xyz[1]:
                    sign_z *= -1
                perms.append(xyz)
                signs.append([sign_x, sign_y, sign_z])

    return np.array(perms, dtype=int), np.array(signs, dtype=int)


PERMS, SIGNS = get_scan_pose_permutations()
# print(np.concatenate((PERMS, SIGNS), axis=1))


@dataclass
class Pose:
    perms: np.ndarray
    signs: np.ndarray
    shift: np.ndarray

    def __init__(self, perms: np.ndarray, signs: np.ndarray, shift: np.ndarray, reverse: bool):
        if not reverse:
            self.perms = perms
            self.signs = signs
            self.shift = shift
        else:
            self.perms = np.argsort(perms)
            self.signs = signs[self.perms]
            self.shift = -1 * shift[self.perms] * self.signs

    def transform(self, xyz: np.ndarray) -> np.ndarray:
        new_xyz = xyz.T[self.perms].T
        new_xyz[:, 0] *= self.signs[0]
        new_xyz[:, 1] *= self.signs[1]
        new_xyz[:, 2] *= self.signs[2]

        new_xyz[:] += self.shift
        return new_xyz


class Scan:
    def __init__(self, idx: int, xyz: np.ndarray):  # Shape (nx3)
        assert isinstance(xyz, np.ndarray)
        self.xyz: np.ndarray = xyz
        self.neighbors: List[Tuple[Scan, Pose, np.ndarray]] = []
        self.idx = idx

    def __repr__(self):
        return "\n".join([str(pt) for pt in self.xyz])

    def add_neighbor(self, scan: 'Scan', pose: Pose):
        self.neighbors.append((scan, pose))

    def merge_with_unknown(self, unknown_scans: np.ndarray):
        unknown_scans[self.idx] = False
        for scan, pose in self.neighbors:
            if unknown_scans[scan.idx]:
                scan.merge_with_unknown(unknown_scans)
                scan.xyz = pose.transform(scan.xyz)

                # rotated_set_a = set(tuple(xyz) for xyz in self.xyz)
                # rotated_set_b = set(tuple(xyz) for xyz in scan.xyz)
                # print(rotated_set_a & rotated_set_b)

                self.xyz = np.concatenate((self.xyz, scan.xyz))
                self.xyz = np.array(list(set(tuple(xyz) for xyz in self.xyz)), dtype=int)

    def __len__(self):
        return self.xyz.shape[0]

    @staticmethod
    def align_two_scans(scan_a: 'Scan', scan_b: 'Scan') -> Optional[Pose]:
        ref_set_a = set(tuple(xyz) for xyz in scan_a.xyz)

        def add(tuple_a, tuple_b):
            return tuple(val_a + val_b for val_a, val_b in zip(tuple_a, tuple_b))

        for perms, signs in zip(PERMS, SIGNS):
            # Rotate
            rotated_xyz_b = copy.deepcopy(scan_b.xyz)
            rotated_xyz_b = (rotated_xyz_b.T[perms]).T
            rotated_xyz_b[:, 0] *= signs[0]
            rotated_xyz_b[:, 1] *= signs[1]
            rotated_xyz_b[:, 2] *= signs[2]

            rotated_set_b = set(tuple(xyz) for xyz in rotated_xyz_b)

            # Shift
            for pt_a in ref_set_a:
                for pt_b in rotated_set_b:
                    diff = tuple(val_a - val_b for val_a, val_b in zip(pt_a, pt_b))
                    new_set_b = set(add(pt, diff) for pt in rotated_set_b)
                    intersection = ref_set_a & new_set_b
                    if len(intersection) >= 12:
                        pose_ij = Pose(perms, signs, np.array(diff), reverse=True)
                        pose_ji = Pose(perms, signs, np.array(diff), reverse=False)

                        return pose_ij, pose_ji

        return None


def _read_lines(path):
    with open(path) as f:
        all_rows = f.readlines()+[""]
        starts = 1+np.array([idx for idx, row in enumerate(all_rows) if row.startswith("---")])
        ends = -2+np.roll(starts, -1)

        scans = [Scan(idx, np.array([row.strip().split(",") for row in all_rows[start:end]], dtype=int))
                 for idx, (start, end) in enumerate(zip(starts, ends))]
        return scans


def part_one(path: str) -> int:
    scans = _read_lines(path)

    # Build graph
    for i, scan_i in enumerate(scans):
        for j in range(i):
            scan_j = scans[j]
            poses = Scan.align_two_scans(scan_i, scan_j)
            if poses is not None:
                pose_ij, pose_ji = poses
                # print(i, j, pose_ij)
                # print(j, i, pose_ji)
                scan_j.add_neighbor(scan_i, pose_ij)
                scan_i.add_neighbor(scan_j, pose_ji)

    unknown_scans = np.ones(len(scans), dtype=bool)
    unknown_scans[0] = False
    scans[0].merge_with_unknown(unknown_scans)

    return len(scans[0].xyz)


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
