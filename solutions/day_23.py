# /usr/bin/python3
"""Day 23."""

from typing import Dict, List, Optional, Tuple
import numpy as np


HALLWAY_CELLS = np.array([0, 10, 30, 50, 70, 90, 100])

# 0 10 20 30 40 50 60 70 80 90 100
#      21    41    61    81
#      22    42    62    82
#      -     -     -     -
#      23    43    63    83
#      24    44    64    84


def idx_to_family(idx: int, depth: int) -> int:
    return 2*(idx//depth + 1)  # Family 2,4,6,8


def _read_lines(path, depth: int) -> Tuple[List[int], List[bool]]:
    assert depth in (2, 4)
    with open(path) as f:
        all_rows = f.readlines()

        dico: Dict[str, List[int]] = {fam: [] for fam in ['A', 'B', 'C', 'D']}

        row = all_rows[2].strip().replace('#', '')
        for idx, fam in enumerate(row):
            dico[fam].append(2*(idx+1)*10 + 1)
        row = all_rows[3].strip().replace('#', '')
        for idx, fam in enumerate(row):
            dico[fam].append(2*(idx+1)*10 + depth)

        if depth == 4:
            dico['A'] += [63, 82]
            dico['B'] += [62, 43]
            dico['C'] += [42, 83]
            dico['D'] += [22, 23]

        a_values = sorted(dico['A'], reverse=True)
        b_values = sorted(dico['B'], reverse=True)
        c_values = sorted(dico['C'], reverse=True)
        d_values = sorted(dico['D'], reverse=True)
        amphis: List[int] = a_values+b_values+c_values+d_values
        finished: List[bool] = [False for _ in range(4*depth)]

        for idx, pos in enumerate(amphis):
            family = idx_to_family(idx, depth)
            if pos == family*10+depth:
                finished[idx] = True
            for k in range(depth-1, 0):
                if pos == family*10+k and idx % depth == k and finished[idx-1]:
                    finished[idx] = True
                    break
        return amphis, finished

# A A A A B B B B C C C C D D D D


def hash_amphis(amphis: List[int], depth: int) -> int:
    return int("".join(["".join([f"{val:03d}"
                                 for val in sorted(amphis[depth*k:depth*(k+1)], reverse=True)])
                        for k in range(4)]))


def get_cost(idx: int, old_pos: int, new_pos: int, depth: int):
    number_moves = old_pos % 10 + new_pos % 10 + abs(old_pos//10 - new_pos//10)
    return number_moves * 10**(idx_to_family(idx, depth)//2 - 1)


def get_available_positions(idx: int, amphis: List[int], depth: int) -> List[int]:
    self_pos = amphis[idx]
    other_pos = [pos for k, pos in enumerate(amphis) if k != idx]
    hallway = np.array([pos for pos in other_pos if pos % 10 == 0])
    hallway_left = hallway[hallway < self_pos]
    hallway_right = hallway[hallway > self_pos]
    hallway_left = np.max(hallway_left) if hallway_left.size != 0 else -np.inf
    hallway_right = np.min(hallway_right) if hallway_right.size != 0 else np.inf

    # Stay in the room
    if self_pos % 10 > 1 and (self_pos-1) in other_pos:
        return []

    # Go in the family room if available
    self_family = idx_to_family(idx, depth)
    family_cell = self_family*10
    if hallway_left < family_cell < hallway_right:
        cells_in_family = [idx_to_family(j, depth) for j, pos in enumerate(amphis)
                           if family_cell < pos < family_cell+10]
        n_fams = len(set(cells_in_family))
        if n_fams == 0:
            return [family_cell + depth]
        elif n_fams == 1 and cells_in_family[0] == self_family:
            return [family_cell + depth - len(cells_in_family)]

    # Stay in the hallway
    if self_pos % 10 == 0:
        return []

    # Go in the hallway
    mask = np.logical_and(HALLWAY_CELLS > hallway_left, HALLWAY_CELLS < hallway_right)
    return list(HALLWAY_CELLS[mask])


def propagate(amphipods: List[int], finished: List[bool],
              dp: Dict[int, int], path: List[str], depth: int) -> Optional[int]:
    hash_amphi = hash_amphis(amphipods, depth)
    if hash_amphi in dp:
        return dp[hash_amphi]

    if all(finished):
        print(f"{','.join(path)}")
        dp[hash_amphi] = 0
        return 0

    min_cost = None
    for idx in range(4*depth):
        if not finished[idx]:
            family = idx_to_family(idx, depth)
            new_positions = get_available_positions(idx, amphipods, depth)
            for new_pos in new_positions:
                old_amphi_pos = amphipods[idx]
                additional_cost = get_cost(idx, old_amphi_pos, new_pos, depth)

                amphipods[idx] = new_pos
                if family*10 < new_pos < (family+1)*10:
                    finished[idx] = True

                path.append(f"{old_amphi_pos}->{new_pos}")
                cost = propagate(amphipods, finished, dp, path, depth)
                path.pop()
                amphipods[idx] = old_amphi_pos
                finished[idx] = False

                if cost is not None:
                    cost += additional_cost
                    min_cost = min(min_cost, cost) if min_cost is not None else cost

    dp[hash_amphi] = min_cost
    return min_cost


def solve(amphis: List[int], finished: List[bool], depth: int) -> int:
    assert len(amphis) == len(finished) == 4*depth
    dp = {}
    return propagate(amphis, finished, dp, [], depth)


def part_one(path: str) -> int:
    depth = 2
    amphis, finished = _read_lines(path, depth)
    return solve(amphis, finished, depth)


def part_two(path: str) -> int:
    depth = 4
    amphis, finished = _read_lines(path, depth)
    return solve(amphis, finished, depth)
