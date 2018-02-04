import win32api
from PIL import ImageGrab


class Screen:
    def __init__(self, number, win_api=win32api, image_grabber=ImageGrab):
        self.win_api = win_api
        self.image_grabber = image_grabber
        self.number = number
        self._setup()

    def _setup(self):
        # Sets the screen resolution and set the x_offset and y_offset
        # Which represent the midway x,y points such that we can divide the screen in 1/4 segments
        self.res = (self.win_api.GetSystemMetrics(0), self.win_api.GetSystemMetrics(1))
        self.x_offset = self.res[0] // 2
        self.y_offset = self.res[1] // 2

    def get_screen(self, section):
        if 1 <= section >= 4:
            raise ValueError('Section must be between 1-4 inclusive')
        if section == 1:
            img = self.image_grabber.grab((0, 0, self.res[0] // 2, self.res[1] // 2))
        elif section == 2:
            img = self.image_grabber.grab((self.x_offset, 0, self.res[0], self.res[1] // 2))
        elif section == 3:
            img = self.image_grabber.grab((0, self.y_offset, self.res[0] // 2, self.res[1]))
        elif section == 4:
            img = self.image_grabber.grab((self.x_offset, self.y_offset, self.res[0], self.res[1]))
        return img

