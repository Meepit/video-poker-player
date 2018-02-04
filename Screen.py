import win32api


class Screen():
    def __init__(self, number):
        self.number = number
        self._setup()

    def _setup(self):
        self.res = (win32api.GetSystemMetrics(0), win32api.GetSystemMetrics(1))
