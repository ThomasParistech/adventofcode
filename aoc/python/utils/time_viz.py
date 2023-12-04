# /usr/bin/python3
"""Time Visualization"""
import os
from typing import List

import matplotlib.pyplot as plt
import numpy as np

from aoc.python import get_year_folder


def generate_times_figure(year: int, times_part_one: List[float], times_part_two: List[float]):
    """Display time taken for each day (and save figure)."""
    year_folder = get_year_folder(year, assert_exists=True)

    bar_width = 0.25
    plt.subplots(figsize=(12, 8))
    plt.yscale('log')
    # Set position of bar on X axis
    br1 = np.arange(25)
    br2 = [x + bar_width for x in br1]

    # Make the plot
    plt.bar(br1, times_part_one, color='tab:purple', width=bar_width,
            edgecolor='k', label='Part one')
    plt.bar(br2, times_part_two, color='tab:green', width=bar_width,
            edgecolor='k', label='Part two')
    plt.axhline(1.0, color="k", label="1s")

    # Adding Xticks
    plt.xlabel('Day', fontweight='bold', fontsize=15)
    plt.ylabel('Logarithmic Time', fontweight='bold', fontsize=15)
    plt.xticks([r + bar_width for r in range(25)],
               [str(r) for r in range(1, 26)])
    plt.title(f"Advent Of Code {year}")
    plt.legend()
    fig_path = os.path.join(year_folder, f'performance_{year}.png')
    plt.savefig(fig_path)
    print(f"Stats for year {year} have been saved at {fig_path}")
    plt.show()
