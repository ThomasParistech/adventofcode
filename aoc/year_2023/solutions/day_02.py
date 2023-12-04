# /usr/bin/python3
"""Day 2."""
from dataclasses import dataclass
from typing import Dict

from aoc.python.utils.parsing import read_lines


@dataclass
class RGB:
    red: int = 0
    green: int = 0
    blue: int = 0

    @staticmethod
    def from_games(path: str) -> Dict[int, 'RGB']:
        """From list of games"""
        rgb_by_id: Dict[int, RGB] = {}
        lines = read_lines(path)
        for game in lines:
            head, content = game.split(": ")
            game_id = int(head.split(" ")[-1])

            rgb = RGB()
            for subset in content.split("; "):
                rgb |= RGB.from_subset(subset)
            rgb_by_id[game_id] = rgb
        return rgb_by_id

    @staticmethod
    def from_subset(s: str) -> 'RGB':
        """from subset string"""
        res = RGB()
        for p in s.strip().split(", "):
            val, name = p.strip().split(" ")
            setattr(res, name, int(val))

        return res

    def __or__(self, other: 'RGB') -> 'RGB':
        """Union."""
        return RGB(red=max(self.red, other.red),
                   green=max(self.green, other.green),
                   blue=max(self.blue, other.blue))

    @property
    def power(self) -> int:
        """Power"""
        return self.red * self.green * self.blue


def part_one(path: str) -> int:
    rgb_by_id = RGB.from_games(path)

    res = 0
    for game_id, rgb in rgb_by_id.items():
        if rgb.red <= 12 and rgb.green <= 13 and rgb.blue <= 14:
            res += game_id
    return res


def part_two(path: str) -> int:
    rgb_by_id = RGB.from_games(path)

    res = 0
    for rgb in rgb_by_id.values():
        res += rgb.power
    return res
