# /usr/bin/python3
"""Day 21."""

from typing import List, Set, Tuple
import numpy as np


class Dice:
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
        return Player(one), Player(two)


def part_one(path: str) -> int:
    player_1, player_2 = _read_lines(path)
    dice = Dice()

    while True:
        dice_sum = dice.next(3)
        win_1 = player_1.move(dice_sum)
        if win_1:
            return player_2.score * dice.n_rolls
        dice_sum = dice.next(3)
        win_2 = player_2.move(dice_sum)
        if win_2:
            return player_1.score * dice.n_rolls

    return -1


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
