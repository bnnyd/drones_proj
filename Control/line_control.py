#!/usr/bin/env python3
import numpy as np

def linesControl(x_dir,y_dir, m):
    # engines power of the parallel movement
    parallel_const = 30
    x_paral = int(np.sign(m)*np.sqrt(1/(1 + m**2)))
    # assuming always positive
    y_paral = int(sqrt(1 -x_paral**2))

    # engines power of the perpendicular movement

    #int(64 + y_move * 63), int(63 + x_move * 63)

    return x_paral, y_paral