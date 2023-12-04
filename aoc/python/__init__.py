# /usr/bin/python3
"""Init"""
import os


def get_year_folder(year: int, assert_exists: bool = False) -> str:
    """Get Year main folder."""
    year_folder = os.path.join("aoc", f"year_{year}")
    if assert_exists:
        assert os.path.isdir(year_folder), f"Missing folder for year {year}"
    return year_folder
