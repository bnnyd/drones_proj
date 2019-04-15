#!/usr/bin/env python3
import numpy as np


def linesControl(x_dir, y_dir, line_ang, im_rows, im_cols):

    # engines power of the parallel movement
    parallel_const = 70
    x_paral = int(parallel_const * np.cos(np.deg2rad(line_ang)))
    # assuming always positive
    y_paral = int(parallel_const * np.sin(np.deg2rad(line_ang)))

    # engines power of the perpendicular movement
    # no-move frame:
    max_dim = max(im_rows, im_cols)
    frame = max_dim/8

    # center the movement around the center of the image
    x_dir = x_dir - int(im_cols/2)
    y_dir = y_dir - int(im_rows/2)

    if abs(x_dir) < frame:
        x_perp = 0
    else:
        x_perp = int(x_dir)
    if abs(y_dir) < frame:
        y_perp = 0
    else:
        # positive y_dir is downwards
        y_perp = - int(y_dir)

    x_move = x_paral + x_perp
    y_move = y_paral + y_perp
    #(64 + y_move * 63), (63 + x_move * 63)

    return x_move, y_move