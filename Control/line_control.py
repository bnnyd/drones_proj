#!/usr/bin/env python3
import numpy as np



def linesControl(x_dir, y_dir, line_ang, im_rows, im_cols):

    if x_dir == 0 and y_dir == 0 and line_ang == 0:
        # it's the case where the line is exactly perpendicular or when no line is found: - don't move
        return 64,63  # "zero" values for backward/forward and right/left

    min_dim = min(im_rows, im_cols)
    max_dim = max(im_rows, im_cols)
    # no-move frame (if the point on the line is in this frame the drone doesn't move perpendicularly):
    frame = max_dim / 32

    # engines power of the parallel movement


    parallel_const = min_dim/4
    x_paral = parallel_const * np.cos(np.deg2rad(line_ang))
    y_paral = parallel_const * np.sin(np.deg2rad(line_ang))


    # engines power of the perpendicular movement

    # change coordinates: the center of the image (position of the drone) will be (0,0):
    x_dir = x_dir - int(im_cols/2)
    y_dir = y_dir - int(im_rows/2)

    # if the perpendicular movemnet is too small, do nothing (use "frame")
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
    x_move = int(risun*63*(x_paral + x_perp)/(im_cols))
    y_move = int(risun*63*(y_paral + y_perp)/(im_rows))



    frw_bck = (64 - y_move)
    lft_rgt = (63 + x_move)
    if frw_bck > 255 or frw_bck < 0:
        print("ERROR: y_perp=" + str(y_perp) + " y_paral=" + str(y_paral) + " im rows=" + str(im_rows))

    return frw_bck, lft_rgt