

class auto_hover():

    def stabilizer(self, current, expected):
        max_x = 40
        max_y = 40
        x_frame_size = 360
        y_frame_size = 180

        x_move = expected(0) - current(0)
        y_move = expected(1) - current(1)

        max_x = 40
        max_y = 40
        x_frame_size = 360
        y_frame_size = 180


        #forword <> back = 64 + [-1,1]*63
        #left <> right = 63 + [-1,1]*63