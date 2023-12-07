# /usr/bin/python3
"""Day 7."""
from collections import Counter
from dataclasses import dataclass
from functools import total_ordering
from typing import Dict
from typing import List
from typing import Tuple

from aoc.python.utils.parsing import read_lines
from aoc.python.utils.parsing import split_first
from aoc.python.utils.parsing import split_last

MAPPING_VALUES: Dict[str, int] = {**{"T": 10, "J": 11, "Q": 12, "K": 13, "A": 14},
                                  **{str(k): k for k in range(1, 10)}}
MAPPING_TYPES: Dict[Tuple[int, ...], int] = {(1, 1, 1, 1, 1): 0,
                                             (1, 1, 1, 2): 1,
                                             (1, 2, 2): 2,
                                             (1, 1, 3): 3,
                                             (2, 3): 4,
                                             (1, 4): 5,
                                             (5,): 6}


def get_hand_type(values: List[int]) -> int:
    return MAPPING_TYPES[tuple(sorted(Counter(values).values()))]


@total_ordering
@dataclass
class Hand:
    values: Tuple[int, int, int, int, int]
    hand_type: int

    @staticmethod
    def from_str(s: str, use_joker: bool) -> 'Hand':
        if use_joker:
            joker_mask = [c == "J" for c in s]
            s = s.replace("J", "1")  # Make it weak
            _list = [MAPPING_VALUES[c] for c in s]
            if all(joker_mask):
                hand_type = max(MAPPING_TYPES.values())
            else:
                most_common_card, _ = Counter([v
                                               for v, is_joker in zip(_list, joker_mask)
                                               if not is_joker]).most_common(1)[0]
                _list_for_handing_type = [most_common_card if is_joker else v
                                          for v, is_joker in zip(_list, joker_mask)]
                hand_type = get_hand_type(_list_for_handing_type)
        else:
            _list = [MAPPING_VALUES[c] for c in s]
            hand_type = get_hand_type(_list)

        values = (_list[0], _list[1], _list[2], _list[3], _list[4])
        return Hand(values, hand_type)

    def __eq__(self, other) -> bool:
        assert isinstance(other, Hand)
        return self.values == other.values

    def __lt__(self, other) -> bool:
        assert isinstance(other, Hand)

        if self.hand_type == other.hand_type:
            for self_val, other_val in zip(self.values, other.values):
                if self_val != other_val:
                    return self_val < other_val
            raise ValueError

        return self.hand_type < other.hand_type


def _part(path: str, use_joker: bool) -> int:
    lines = read_lines(path)

    hands = [Hand.from_str(split_first(line, " "), use_joker) for line in lines]
    bids = [int(split_last(line, " ")) for line in lines]

    sorted_indices = sorted(range(len(hands)), key=lambda k: hands[k])

    return sum((k+1) * bids[sorted_idx]
               for k, sorted_idx in enumerate(sorted_indices))


def part_one(path: str) -> int:
    return _part(path, use_joker=False)


def part_two(path: str) -> int:
    return _part(path, use_joker=True)
