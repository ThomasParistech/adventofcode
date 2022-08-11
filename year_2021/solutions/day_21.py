# /usr/bin/python3
"""Day 21."""

from typing import Dict, List, Set, Tuple
import numpy as np


class DeterministicDice:
    def __init__(self):
        self.next_val = 1
        self.n_rolls = 0

    def next(self, n):
        sum = 0
        for _ in range(n):
            sum += self.next_val
            self.next_val = 1 + (self.next_val) % 100
        self.n_rolls += n
        return sum


class Player:
    def __init__(self, val):
        self.val = val
        self.score = 0

    def move(self, shift) -> bool:
        self.val = 1 + (self.val+shift-1) % 10
        self.score += self.val
        return self.score >= 1000


def _read_lines(path):
    with open(path) as f:
        all_rows = f.readlines()
        one, two = tuple(int(row.strip().split(": ")[-1]) for row in all_rows)
        return one, two


def part_one(path: str) -> int:
    one, two = _read_lines(path)
    player_1, player_2 = Player(one), Player(two)
    dice = DeterministicDice()

    while True:
        dice_sum = dice.next(3)
        win_1 = player_1.move(dice_sum)
        if win_1:
            return player_2.score * dice.n_rolls
        dice_sum = dice.next(3)
        win_2 = player_2.move(dice_sum)
        if win_2:
            return player_1.score * dice.n_rolls


def get_3_sums():
    counts = {k: 0 for k in range(3, 10)}
    for a in range(1, 4):
        for b in range(1, 4):
            for c in range(1, 4):
                counts[a+b+c] += 1
    return counts


COUNTS_3_SUMS = get_3_sums()  # How many universes per sum result


class DiracPlayer:
    def __init__(self, init_pos: int):
        # [pos][score] = n_univ
        self.universes: List[Dict[int, int]] = [{} for _ in range(11)]
        self.universes[init_pos][0] = 1
        self.n_wins = 0

    def next(self, other: 'DiracPlayer') -> bool:
        new_universes = [{} for _ in range(11)]
        n_winning_universes = 0
        for pos, dico in enumerate(self.universes):
            for score, n_univ in dico.items():
                for sum3, count_univ in COUNTS_3_SUMS.items():
                    new_pos = 1 + (pos+sum3-1) % 10
                    new_score = score+new_pos
                    new_n_univ = n_univ*count_univ
                    if new_score >= 21:
                        n_winning_universes += new_n_univ
                    else:
                        new_universes[new_pos][new_score] = new_universes[new_pos].get(new_score, 0) + new_n_univ
        self.universes = new_universes

        self.n_wins += n_winning_universes * other.get_n_remaining_universes()
        return self.get_n_remaining_universes() != 0

    def get_n_remaining_universes(self):
        return int(np.sum(np.sum(list(dico.values())) for dico in self.universes))


def part_two(path: str) -> int:
    one, two = _read_lines(path)
    player_1, player_2 = DiracPlayer(one), DiracPlayer(two)

    while True:
        if not player_1.next(player_2):
            break
        if not player_2.next(player_1):
            break

    return player_1.n_wins
