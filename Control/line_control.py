#!/usr/bin/env python3
import numpy as np


def linesControl(x_dir, y_dir, line_ang, im_rows, im_cols):

    min_dim = min(im_rows, im_cols)
    max_dim = max(im_rows, im_cols)
    # no-move frame:
    frame = max_dim / 8

    # engines power of the parallel movement
    parallel_const = min_dim/2
    x_paral = parallel_const * np.cos(np.deg2rad(line_ang))
    # assuming always positive
    y_paral = parallel_const * np.sin(np.deg2rad(line_ang))

    # engines power of the perpendicular movement


    # center the movement around the center of the image
    x_dir = x_dir - int(im_cols/2)
    y_dir = y_dir - int(im_rows/2)

    if abs(x_dir) < frame:
        x_perp = 0
    else:
        x_perp = x_dir
    if abs(y_dir) < frame:
        y_perp = 0
    else:
        # positive y_dir is downwards
        y_perp = - y_dir

    risun = 0.3
    # normalization: both x_par and x_perp have values [0, min_dim/2],...
    # x and y move are in cartesian coordinates and not image coord.
    x_move = int(risun*63*(x_paral + x_perp)/(im_rows))
    y_move = int(risun*63*(y_paral + y_perp)/(im_cols))



    frw_bck = (64 - y_move)
    lft_rgt = (63 + x_move)
    return frw_bck, lft_rgt