# /usr/bin/python3
"""Day 4."""
from aoc.python.utils.parsing import read_lines
from aoc.python.utils.parsing import split_in_two


def part_one(path: str) -> int:
    lines = read_lines(path)
    res = 0
    for row in lines:
        _, content = split_in_two(row, ":")
        content = content.replace("  ", " ")
        winning_numbers, played_numbers = split_in_two(content, "|")

        num_wins = len(set(winning_numbers.split(" ")) & set(played_numbers.split(" ")))
        if num_wins != 0:
            res += 2**(num_wins-1)
    return res


def part_two(path: str) -> int:
    lines = read_lines(path)

    number_cards = [1]*len(lines)
    for k, row in enumerate(lines):
        _, content = split_in_two(row, ":")
        content = content.replace("  ", " ")
        winning_numbers, played_numbers = split_in_two(content, "|")

        num_wins = len(set(winning_numbers.split(" ")) & set(played_numbers.split(" ")))
        for i in range(k+1, min(len(lines), k+1+num_wins)):
            number_cards[i] += number_cards[k]

    return sum(number_cards)
