# /usr/bin/python3
"""Main"""

import importlib
import time
from year_2022.profiling.profiler import export_profiling_events
from year_2022.solutions import EXPECTED_TOY_SOLUTIONS


def parse_args():
    import argparse
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description='Advent of Code.')

    parser.add_argument('-d', "--day", type=int, required=True, help="Day to run")
    parser.add_argument('-t', '--part-two', default=False, action='store_true', help="Part one by default")

    return parser.parse_args()


def run(day: int, part_two: bool, bis: bool = False):
    module_name = f"year_2022.solutions.day_{day:02d}"
    if bis:
        module_name += "_bis"

    try:
        day_solution = importlib.import_module(module_name)
    except ModuleNotFoundError:
        return

    if not bis:
        print(f"--- Part {1+int(part_two)} of Day {day:02d} ---")
    else:
        print("- Alternative solution -")

    try:
        solve = day_solution.part_two if part_two else day_solution.part_one
    except AttributeError as err:
        print(f"Error: {err}")
        return

    toy_answer = solve(f"year_2022/data/day_{day:02d}_toy.csv")
    good_answer = EXPECTED_TOY_SOLUTIONS[day][int(part_two)]
    assert toy_answer == good_answer, f"Expected {good_answer}, but got {toy_answer}"
    print(f"=> Correct toy answer: {toy_answer}")

    start = time.time()
    answer = solve(f"year_2022/data/day_{day:02d}.csv")
    end = time.time()
    print(f"=> Day answer: {answer}")
    print(f"Ran in {end-start} s")
    print()


def main():
    args = parse_args()

    run(args.day, args.part_two)
    run(args.day, args.part_two, bis=True)  # Run alternative solution if there is one available

    export_profiling_events("profiling/profiling.json")


main()
