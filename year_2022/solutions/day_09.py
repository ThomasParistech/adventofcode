# /usr/bin/python3
"""Day 9."""

from dataclasses import dataclass
from dataclasses import field
from typing import Dict
from typing import List
from typing import Optional
from typing import Tuple


@dataclass
class Rope:
    h_x: int = 0
    h_y: int = 0
    t_x: int = 0
    t_y: int = 0
    history: List[Tuple[int, int]] = field(default_factory=list)

    def __post_init__(self) -> None:
        self.history.append((self.t_x, self.t_y))

    def move(self, cmd: str):
        change = False
        old_h = (self.h_x, self.h_y)
        if cmd == "R":
            change = self.t_x == self.h_x-1
            self.h_x += 1
        elif cmd == "L":
            change = self.t_x == self.h_x+1
            self.h_x -= 1
        elif cmd == "U":
            change = self.t_y == self.h_y+1
            self.h_y -= 1
        else:  # D
            change = self.t_y == self.h_y-1
            self.h_y += 1

        if change:
            self.t_x, self.t_y = old_h
            self.history.append((self.t_x, self.t_y))


@dataclass
class RopeWithKnots:
    x: int = 0
    y: int = 0
    tail: Optional['RopeWithKnots'] = None

    def move(self, target_dx: int, target_dy: int):
        if self.tail is not None:
            t_dx = target_dx + self.x - self.tail.x
            t_dy = target_dy + self.y - self.tail.y
            if max(abs(t_dx), abs(t_dy)) > 1:
                dx = 1 if t_dx > 0 else -1
                dy = 1 if t_dy > 0 else -1
                if t_dx == 0:
                    dx = 0
                if t_dy == 0:
                    dy = 0

                self.tail.move(dx, dy)

        self.x += target_dx
        self.y += target_dy


def _read_lines(path: str) -> List[Tuple[str, int]]:
    with open(path) as f:
        rows = [row.strip().split(" ") for row in f.readlines()]
        return [(row[0], int(row[1])) for row in rows]


def part_one(path: str) -> int:
    rows = _read_lines(path)

    rope = Rope()
    for cmd, n in rows:
        for _ in range(n):
            rope.move(cmd)

    return len(set(rope.history))


STEPS_XY: Dict[str, Tuple[int, int]] = {
    "R": (1, 0),
    "L": (-1, 0),
    "D": (0, 1),
    "U": (0, -1)
}


def part_two(path: str) -> int:
    rows = _read_lines(path)

    knots: List[RopeWithKnots] = []
    for k in range(10):
        knots.append(RopeWithKnots(tail=knots[-1] if k != 0 else None))

    history: List[Tuple[int, int]] = []
    for cmd, n in rows:
        dx, dy = STEPS_XY[cmd]
        for _ in range(n):
            knots[-1].move(dx, dy)
            history.append((knots[0].x, knots[0].y))

    return len(set(history))
