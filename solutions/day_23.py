# /usr/bin/python3
"""Day 23."""

from typing import Dict, List, Optional, Tuple
import numpy as np


HALLWAY_CELLS = np.array([0, 10, 30, 50, 70, 90, 100])

# 0 10 20 30 40 50 60 70 80 90 100
#      21    41    61    81
#      22    42    62    82


def _read_lines(path):
    with open(path) as f:
        all_rows = f.readlines()

        dico: Dict[str, List[int]] = {fam: [] for fam in ['A', 'B', 'C', 'D']}

        row = all_rows[2].strip().replace('#', '')
        for idx, fam in enumerate(row):
            dico[fam].append(2*(idx+1)*10 + 1)
        row = all_rows[3].strip().replace('#', '')
        for idx, fam in enumerate(row):
            dico[fam].append(2*(idx+1)*10 + 2)

        return dico['A'], dico['B'], dico['C'], dico['D']


def part_one(path: str) -> int:

    def hash_amphis(amphis: List[int]) -> int:
        res = ""
        for k in range(4):
            pair = (amphis[2*k], amphis[2*k+1])
            res += "{0:03d}{1:03d}".format(min(pair), max(pair))
        return int(res)

    def idx_to_family(idx: int) -> int:
        return 2*(idx//2 + 1)  # Family 2,4,6,8

    def get_available_positions(idx: int, amphis: List[int]) -> List[int]:
        self_pos = amphis[idx]
        other_pos = [pos for k, pos in enumerate(amphis) if k != idx]
        hallway = np.array([pos for pos in other_pos if pos % 10 == 0])
        hallway_left = hallway[hallway < self_pos]
        hallway_right = hallway[hallway > self_pos]
        hallway_left = np.max(hallway_left) if hallway_left.size != 0 else -np.inf
        hallway_right = np.min(hallway_right) if hallway_right.size != 0 else np.inf

        # Stay in the room
        if self_pos % 10 == 2 and (self_pos-1) in other_pos:
            return []

        # Go in the family room if available
        self_family = idx_to_family(idx)
        family_cell = self_family*10
        if hallway_left < family_cell < hallway_right:
            if not family_cell+1 in other_pos:
                if not family_cell+2 in other_pos:
                    return [family_cell+2]

                fam = [idx_to_family(j) for j, pos in enumerate(amphis) if pos == family_cell+2][0]
                if fam == self_family:
                    return [family_cell+1]

        # Stay in the hallway
        if self_pos % 10 == 0:
            return []

        # Go in the hallway
        mask = np.logical_and(HALLWAY_CELLS > hallway_left, HALLWAY_CELLS < hallway_right)
        return list(HALLWAY_CELLS[mask])

    def get_cost(idx: int, old_pos: int, new_pos: int):
        number_moves = old_pos % 10 + new_pos % 10 + abs(old_pos//10 - new_pos//10)
        return number_moves * 10**(idx_to_family(idx)//2 - 1)

    def propagate(amphipods: List[int], finished: List[bool], dp: Dict[int, int], path: List[str]) -> Optional[int]:
        hash_amphi = hash_amphis(amphipods)
        if hash_amphi in dp:
            return dp[hash_amphi]

        if all(finished):
            # print(f"{','.join(path)}")
            dp[hash_amphi] = 0
            return 0

        min_cost = None
        for idx in range(8):
            if not finished[idx]:
                family = idx_to_family(idx)
                new_positions = get_available_positions(idx, amphipods)
                for new_pos in new_positions:
                    old_amphi_pos = amphipods[idx]
                    additional_cost = get_cost(idx, old_amphi_pos, new_pos)

                    amphipods[idx] = new_pos
                    if new_pos in (family*10+1, family*10+2):
                        finished[idx] = True

                    path.append(f"{old_amphi_pos}->{new_pos}")
                    cost = propagate(amphipods, finished, dp, path)
                    path.pop()
                    amphipods[idx] = old_amphi_pos
                    finished[idx] = False

                    if cost is not None:
                        cost += additional_cost
                        min_cost = min(min_cost, cost) if min_cost is not None else cost

        dp[hash_amphi] = min_cost
        return min_cost

    ###### Run ######

    aa, bb, cc, dd = _read_lines(path)

    amphis: List[int] = [max(aa), min(aa), max(bb), min(bb), max(cc), min(cc), max(dd), min(dd)]
    finished: List[bool] = [False for _ in range(8)]

    for idx, pos in enumerate(amphis):
        family = idx_to_family(idx)
        if pos == family*10+2:
            finished[idx] = True
        elif pos == family*10+1 and idx % 2 == 1 and finished[idx-1]:
            finished[idx] = True

    dp = {}
    return propagate(amphis, finished, dp, [])


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
