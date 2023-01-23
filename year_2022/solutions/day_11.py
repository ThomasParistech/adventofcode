# /usr/bin/python3
"""Day 11."""

from typing import List, Callable, Tuple, Dict
import numpy as np
from dataclasses import dataclass


@dataclass
class Monkey:
    items: List[int]
    div: int
    send_true: int
    send_false: int
    operation: Callable[[int], int]
    inspection_count: int = 0

    def process(self) -> List[Tuple[int, int]]:
        send: List[Tuple[int, int]] = []
        for x in self.items:
            x = self.operation(x)//3
            send.append((x, self.send_true if x % self.div == 0 else self.send_false))

        self.inspection_count += len(self.items)
        self.items.clear()
        return send


@dataclass
class AdvancedMonkey:
    items_modulos: List[Dict[int, int]]
    div: int
    send_true: int
    send_false: int
    operation: Callable[[int], int]
    inspection_count: int = 0

    @staticmethod
    def from_monkey(monkey: Monkey) -> 'AdvancedMonkey':
        return AdvancedMonkey(
            items_modulos=[{key: val % key for key in [2, 3, 5, 7, 11, 13, 17, 19, 23]}
                           for val in monkey.items],
            div=monkey.div,
            send_true=monkey.send_true,
            send_false=monkey.send_false,
            operation=monkey.operation,
        )

    def process(self) -> List[Tuple[Dict[int, int], int]]:
        send: List[Tuple[int, int]] = []
        for modulos in self.items_modulos:
            new_modulos = {key: self.operation(x) % key
                           for key, x in modulos.items()}

            send.append((new_modulos, self.send_true if new_modulos[self.div] == 0 else self.send_false))

        self.inspection_count += len(self.items_modulos)
        self.items_modulos.clear()
        return send


def _read_lines(path: str) -> List[Monkey]:
    with open(path) as f:
        monkeys_str = f.read().split("\n\n")
        monkeys: List[Monkey] = []
        for monkey_str in monkeys_str:
            monkey_str = monkey_str.split("\n")
            operation_str = monkey_str[2].split(" = ")[-1].replace("old", "x")

            monkeys.append(Monkey(items=list(map(int, monkey_str[1].split(": ")[-1].split(","))),
                                  operation=eval('lambda x : ' + operation_str),
                                  div=int(monkey_str[3].split(" ")[-1]),
                                  send_true=int(monkey_str[4].split(" ")[-1]),
                                  send_false=int(monkey_str[5].split(" ")[-1])))
        return monkeys


def part_one(path: str) -> int:
    monkeys = _read_lines(path)

    for _ in range(20):
        for monkey in monkeys:
            send = monkey.process()
            for val, idx in send:
                monkeys[idx].items.append(val)

    counts = sorted([monkey.inspection_count for monkey in monkeys])
    return counts[-1]*counts[-2]


def part_two(path: str) -> int:
    advanced_monkeys = [AdvancedMonkey.from_monkey(monkey) for monkey in _read_lines(path)]

    for _ in range(10000):
        for monkey in advanced_monkeys:
            send = monkey.process()
            for modulos, idx in send:
                advanced_monkeys[idx].items_modulos.append(modulos)

    counts = sorted([monkey.inspection_count for monkey in advanced_monkeys])
    return counts[-1]*counts[-2]
