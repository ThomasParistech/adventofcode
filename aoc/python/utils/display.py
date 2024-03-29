# /usr/bin/python3
"""Plot."""
import matplotlib.pyplot as plt
import numpy as np


def plot_int_array(x: np.ndarray, block: bool = True):
    plt.figure()
    plt.ioff()
    plt.pcolormesh(x.astype(int), edgecolors='k', linewidth=0.2, snap=True)
    plt.colorbar()
    plt.gca().set_aspect('equal')
    plt.gca().invert_yaxis()
    plt.show(block=block)


def print_1d_array(x: np.ndarray, sep: str = ""):
    print(sep.join([str(a) for a in x]))


def print_2d_array(x: np.ndarray, sep: str = ""):
    for row in x:
        print_1d_array(row, sep)
