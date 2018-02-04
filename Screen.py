import win32api


class Screen():
    def __init__(self, number):
        self.number = number
        self._setup()

    def _setup(self):
        self.res = (win32api.GetSystemMetrics(0), win32api.GetSystemMetrics(1))
        self.x_offset = self.res[0] // 2
        self.y_offset = self.res[1] // 2