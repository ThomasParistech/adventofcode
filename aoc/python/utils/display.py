# /usr/bin/python3
"""Plot."""
import matplotlib.pyplot as plt
import numpy as np


def plot_int_array(x: np.ndarray):
    plt.ioff()
    plt.pcolormesh(x.astype(int), edgecolors='k', linewidth=0.2, snap=True)
    plt.colorbar()
    plt.gca().set_aspect('equal')
    plt.gca().invert_yaxis()
    plt.show()
