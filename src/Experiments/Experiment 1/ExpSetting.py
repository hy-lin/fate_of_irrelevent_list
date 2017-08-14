
class ExpSetting(object):
    def __init__(self):
        # setsize related
        self.n_practice = 5
        self.n_trials = 240

        # stimulus related
        self.font_size_unscaled = 24
        self.font_size = 24

        # stimulus positions
        self.stimulus_positions_unscaled = [
            (640.0, 360.0), # probe
            (640.0, 240.0), # top, middle
            (300.0, 240.0), # top, left
            (980.0, 240.0), # top, right
            (640.0, 480.0), # bottom, middle
            (300.0, 480.0), # bottom, left
            (980.0, 480.0), # bottom, right
        ]

        # cue related
        self.cue_frame_height_unscaled = 200
        self.cue_frame_width_unscaled = 1000
        self.cue_top_y_unscale = 240
        self.cue_bottom_y_unscale = 480

        # time related
        self.inter_trial_interval = 500
        self.stimulus_onset_duration = 5000

        # keyboard related
        self.response_keys = ['right', 'left']
        self.escape_key = [b'D']
        
    def updateDisplayScale(self, display):
        x, y = display.window.size
        x_scale = x / 1280.0
        y_scale = y / 720.0
        
        print('x:y = ', x, y)
        print('x:y scale = ', x_scale, y_scale)
        
        self.window_center = (x/2, y/2)
        self.scale = min(x_scale, y_scale)
        self.window_size = (1280 * self.scale, 720 * self.scale)
        
        self.stimulus_positions = []
        for position in self.stimulus_positions_unscaled:
            self.stimulus_positions.append((
                (position[0] - 1280/2) * self.scale + self.window_center[0],
                (position[1] - 720/2) * self.scale + self.window_center[1]
            ))

        self.cue_frame_height = self.cue_frame_height_unscaled * self.scale
        self.cue_frame_width = self.cue_frame_width_unscaled * self.scale
        self.cue_top_y = (self.cue_top_y_unscale - 720/2) * self.scale + self.window_center[1]
        self.cue_bottom_y = (self.cue_bottom_y_unscale - 720/2) * self.scale + self.window_center[1]

        self.font_size = self.font_size_unscaled * self.scale