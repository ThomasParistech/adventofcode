# /usr/bin/python3
# type: ignore
"""Day 18."""

import copy
from dataclasses import dataclass
from typing import Optional
from typing import Tuple

import numpy as np


@dataclass
class Number:
    val: Optional[int] = None
    left: Optional['Number'] = None
    right: Optional['Number'] = None
    depth: int = 0

    def explode(self, left_neighbor: Optional['Number'], right_neighbor: Optional['Number']):
        if left_neighbor is not None:
            left_neighbor.val += self.left.val
        if right_neighbor is not None:
            right_neighbor.val += self.right.val
        self.val = 0
        self.left = None
        self.right = None

    def split(self):
        assert self.val is not None
        self.left = Number(val=int(np.floor(self.val*0.5)), depth=self.depth+1)
        self.right = Number(val=int(np.ceil(self.val*0.5)), depth=self.depth+1)
        self.val = None

    @staticmethod
    def add(a: "Number", b: 'Number') -> 'Number':
        assert a.depth == 0 and b.depth == 0
        res = Number()
        res.left = a
        res.right = b
        res.depth = 0
        res.left.increase_depth()
        res.right.increase_depth()

        res.reduce()
        return res

    def reduce(self):
        while True:
            # print(self)
            leftmost_val, node_to_explode, rightmost_val, _ = self.get_first_node_to_explode(None, None)
            if node_to_explode is not None:
                lval = leftmost_val.val if leftmost_val is not None else "X"
                rval = rightmost_val.val if rightmost_val is not None else "X"
                # print(f"Explode {node_to_explode} with {lval} and {rval}")
                node_to_explode.explode(leftmost_val, rightmost_val)
            else:
                node_to_split = self.get_first_node_to_split()
                if node_to_split is not None:
                    # print(f"Split {node_to_split}")
                    node_to_split.split()
                else:
                    break

    def get_first_node_to_explode(self,
                                  leftmost_val: Optional['Number'],
                                  node_to_explode: Optional['Number']) -> Tuple[Optional['Number'],
                                                                                Optional['Number'],
                                                                                Optional['Number'],
                                                                                bool]:
        # Val
        if self.val is not None:
            if node_to_explode is not None:
                return leftmost_val, node_to_explode, self, True  # Done
            return self, None, None, False  # Update leftmost value

        # Pair
        if node_to_explode is None and self.needs_to_explode():
            return leftmost_val, self, None, False  # Wait for next right val and skip children

        leftmost_val, node_to_explode, rightmost, success = self.left.get_first_node_to_explode(leftmost_val,
                                                                                                node_to_explode)
        if not success:
            leftmost_val, node_to_explode, rightmost, success = self.right.get_first_node_to_explode(leftmost_val,
                                                                                                     node_to_explode)
        return leftmost_val, node_to_explode, rightmost, success

    def get_first_node_to_split(self) -> Optional['Number']:
        # Val
        if self.val is not None:
            if self.needs_to_split():
                return self
            return None

        # Pair
        node_to_split = self.left.get_first_node_to_split()
        if node_to_split is None:
            node_to_split = self.right.get_first_node_to_split()
        return node_to_split

    def increase_depth(self):
        self.depth += 1
        if self.left is not None:
            self.left.increase_depth()
        if self.right is not None:
            self.right.increase_depth()

    def needs_to_explode(self) -> bool:
        if self.left is None:
            return False
        return self.depth >= 4

    def needs_to_split(self) -> bool:
        if self.val is None:
            return False
        return self.val >= 10

    def magnitude(self):
        if self.val is not None:
            return self.val

        return int(3*self.left.magnitude() + 2*self.right.magnitude())

    def __repr__(self) -> str:
        if self.val is None:
            return f"[{self.left},{self.right}]"

        return str(self.val)


def split_number(number: str) -> Tuple[str, str]:
    number = number[1:-1]
    open_brackets = 0
    for idx, c in enumerate(number):
        if c == '[':
            open_brackets += 1
        elif c == "]":
            open_brackets -= 1
        elif c == "," and open_brackets == 0:
            return number[:idx], number[idx+1:]

    raise ValueError()


def parse_number(number: str, depth: int) -> Number:
    # print(number)
    if not '[' in number:
        return Number(val=int(number),
                      depth=depth)

    left, right = split_number(number)
    new_number = Number()
    new_number.left = parse_number(left, depth+1)
    new_number.right = parse_number(right, depth+1)
    new_number.depth = depth
    return new_number


def _read_lines(path):
    with open(path) as f:
        all_rows = f.readlines()
        return [parse_number(row.strip(), 0) for row in all_rows]


def part_one(path: str) -> int:
    numbers = _read_lines(path)
    res = numbers[0]
    for k in range(1, len(numbers)):
        res = Number.add(res, numbers[k])

    # print(res)
    return res.magnitude()


def part_two(path: str) -> int:
    numbers = _read_lines(path)
    max_mag = 0
    n = len(numbers)
    for i in range(n):
        for j in range(n):
            if i != j:
                n_i = copy.deepcopy(numbers[i])
                n_j = copy.deepcopy(numbers[j])
                mag = Number.add(n_i, n_j).magnitude()
                max_mag = max(max_mag, mag)

    return max_mag
