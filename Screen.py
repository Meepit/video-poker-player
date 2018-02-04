import win32api


class Screen():
    def __init__(self, number, win_api=win32api):
        self.win_api = win_api
        self.number = number
        self._setup()

    def _setup(self):
        # Sets the screen resolution and set the x_offset and y_offset
        # Which represent the midway x,y points such that we can divide the screen in 1/4 segments
        self.res = (self.win_api.GetSystemMetrics(0), self.win_api.GetSystemMetrics(1))
        self.x_offset = self.res[0] // 2
        self.y_offset = self.res[1] // 2


