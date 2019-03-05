import numpy as np

class AutoHover():

    def find_direction(self, expected, frame_size):
        frame_size = np.asanyarray(frame_size)
        expected = np.asanyarray(expected)

        #print(type(frame_size), np.shape(frame_size))

        currentX = frame_size[0]/2
        currentY = frame_size[1]/2
        Max_frame = max(frame_size[0],frame_size[1])

        #target is the currect range of the drone around the object
        X_TARGET = Max_frame/8
        Y_TARGET = Max_frame/8
        #positive is rightwards
        x_move = expected[0] - currentX
        if abs(x_move) < X_TARGET:
            x_move = 0

        #positive is backards
        y_move = expected[1] - currentY
        if abs(y_move) < Y_TARGET:
            y_move = 0
        #change cX cY (if "no object", cX=4000)
        return x_move, y_move

    def engine_power(self, x_move, y_move, frame_size):
        #forward <> back = 64 + [-1,1]*63
        #left <> right = 63 + [-1,1]*63
        frame_size = np.asanyarray(frame_size)
        ## normalize moves in interval from -0.5 to 0.5 to prevent extreme movement
        RESTRAINT = 0.3
        x_move = (x_move/(0.5*frame_size[0]))*RESTRAINT
        y_move = (y_move/(0.5*frame_size[1]))*RESTRAINT
        #64 + y_move*63, 63 + x_move*63
        return int(64 + y_move*63), int(63 + x_move*63)