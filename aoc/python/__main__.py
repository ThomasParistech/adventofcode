# /usr/bin/python3
"""Main"""
import importlib
import os
import sys
import time
from types import ModuleType
from typing import List
from typing import Optional

import fire
import numpy as np
from tqdm import tqdm

from aoc.python import get_year_folder
from aoc.python.utils.profiler import export_profiling_events
from aoc.python.utils.time_viz import generate_times_figure


def get_expected_toy_solution(year: int, day: int, part_two: bool) -> Optional[str]:
    """Get expected toy solution for a given year, day and part."""
    csv_file = os.path.join(get_year_folder(year, assert_exists=True), "data/expected_toy_solutions.csv")
    assert os.path.isfile(csv_file), f"Missing toy solutions CSV file for year {year}"

    with open(csv_file, "r", encoding="utf-8") as f:
        all_rows = f.readlines()
        assert len(all_rows) == 25, f"Got only {len(all_rows)} days"
        row = all_rows[day-1].split("#")[0].strip()  # Remove comments
        val = (row.split(",")[int(part_two)]).strip()
        if val == "None":
            return None
        return val


def get_data(year: int, day: int, part_two: bool, toy: bool) -> Optional[str]:
    """Get CSV data file for a given year and day (real or toy data)"""
    year_folder = get_year_folder(year, assert_exists=True)
    base = os.path.join(year_folder, f"data/day_{day:02d}")

    if toy:
        path = base+"_toy.csv"
        if not os.path.isfile(path):
            path = base + "_toy_" + ("part_two" if part_two else "part_one") + ".csv"
    else:
        path = base+".csv"

    return path if os.path.isfile(path) else None


def get_day_module(year: int, day: int, bis: bool) -> Optional[ModuleType]:
    """Get Python module of a given day of a given year (can also be an alternative solution with bis=True)"""
    year_folder = get_year_folder(year, assert_exists=True)
    module_name = os.path.join(year_folder, "solutions", f"day_{day:02d}").replace("/", ".")
    if bis:
        module_name += "_bis"
    try:
        return importlib.import_module(module_name)
    except ModuleNotFoundError:
        return None


def run(year: int, day: int, part_two: bool, bis: bool = False) -> bool:
    """Evaluate solution for a given year, day and part."""
    day_solution = get_day_module(year, day, bis)
    if day_solution is None:
        if not bis:
            print(f"Missing day solution code for day {day} of year {year}")
        return False

    if bis:
        print("- Alternative solution -")
    else:
        print(f"--- Year {year} / Part {1+int(part_two)} of Day {day:02d} ---")

    try:
        solve = day_solution.part_two if part_two else day_solution.part_one  # type: ignore
    except AttributeError as err:
        print(f"Error: {err}")
        return False

    toy_data = get_data(year, day, part_two, toy=True)
    if toy_data is None:
        print(f"Missing toy CSV file for day {day} of year {year}")
        return False
    toy_answer = str(solve(toy_data))
    good_answer = get_expected_toy_solution(year, day, part_two)
    if good_answer is None:
        print(f"Missing toy solution for day {day} of year {year}")
        return False

    if toy_answer != good_answer:
        print(f"Expected {good_answer}, but got {toy_answer}")
        return False

    print(f"=> Correct toy answer: {toy_answer}")

    day_data = get_data(year, day, part_two, toy=False)
    if day_data is None:
        print(f"Missing CSV file for day {day} of year {year}")
        return False

    start = time.perf_counter()
    answer = str(solve(day_data))
    end = time.perf_counter()
    print(f"=> Day answer: {answer}")
    print(f"Ran in {end-start} s")
    print()
    return True


def _measure_run(y: int, d: int, t: bool) -> float:
    with open(os.devnull, 'w') as _dev_null:
        sys.stdout = _dev_null  # Block Print

        start = time.perf_counter()
        if run(y, d, t):
            end = time.perf_counter()
            measure = end-start
        else:
            measure = np.nan

    sys.stdout = sys.__stdout__  # Enable print
    return measure


def get_most_recent_year() -> int:
    for k in reversed(range(2000, 2100)):
        if os.path.isdir(get_year_folder(k)):
            return k
    raise ValueError("There's no valid year folder")


def get_most_recent_day(year: int) -> int:
    for k in reversed(range(30)):
        if get_day_module(year, k, bis=False):
            return k
    raise ValueError(f"There's no valid day for year {year}")


def main(y: Optional[int] = None,
         d: Optional[int] = None,
         all: bool = False,
         two: bool = False):
    """
    Args:
        y: Year to run. If not specified, use the latest year
        d: Day to run. If not specified, use the latest day of the input year
        all: If specified, run evaluation on all days
        two: If specified, run part two
    """
    if y is None:
        y = get_most_recent_year()

    if d is None:
        d = get_most_recent_day(y)

    if all:
        # MEASURE
        times_part_one: List[float] = []
        times_part_two: List[float] = []
        with tqdm(desc=f"AdventOfCode {y}", total=50, unit="star") as tbar:
            for day in range(1, 26):
                times_part_one.append(_measure_run(y, day, False))
                tbar.update(1)
                times_part_two.append(_measure_run(y, day, True))
                tbar.update(1)
        # DRAW
        generate_times_figure(y, times_part_one, times_part_two)
    else:
        run(y, d, two)
        run(y, d, two, bis=True)  # Run alternative solution if there is one available
        export_profiling_events(os.path.join(get_year_folder(y), "profiling/profiling.json"))


if __name__ == "__main__":
    fire.Fire(main)
