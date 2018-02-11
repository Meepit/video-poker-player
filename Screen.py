import cv2
import numpy as np
import win32api
from PIL import ImageGrab


class Screen:
    def __init__(self, number, win_api=win32api, image_grabber=ImageGrab):
        self.win_api = win_api
        self.image_grabber = image_grabber
        self.number = number
        self.x_offset = 0
        self.y_offset = 0
        self._setup()

    def _setup(self):
        # Sets the screen resolution and set the x_offset and y_offset
        # Which represent the midway x,y points such that we can divide the screen in 1/4 segments
        self.res = (self.win_api.GetSystemMetrics(0), self.win_api.GetSystemMetrics(1))
        if self.number == 2:
            self.x_offset = self.res[0] // 2
        if self.number == 3:
            self._y_offset = self.res[1] // 2
        if self.number == 4:
            self._x_offset = self.res[0] // 2
            self._y_offset = self.res[1] // 2

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

    def build_locations(self, img):
        card_boxes = self._get_card_locations(img)
        coords = self._build_coord_dict(card_boxes)
        self._get_deal_button(coords)
        return coords

    def _build_coord_dict(self, card_boxes):
        coords = dict()
        for i in range(4):
            coords["card{0}".format(i+1)] = {"coord":
                                      (self.x_offset + card_boxes[i][0],
                                       self.y_offset + card_boxes[i][1],
                                       self.x_offset + card_boxes[i][0] + card_boxes[i][2],
                                       self.y_offset + card_boxes[i][1] + card_boxes[i][3]
                                       )}
        return coords

    def _get_card_locations(self, img):
        # img: PIL image object
        # Convert to cv2 image, using image contour detection to find coordinates of 4 largest cards
        print("Getting locations")
        im = np.array(img)
        imgray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
        ret, thresh = cv2.threshold(imgray, 127, 255, 0)
        image, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        card_boxes = []
        for i in contours:
            if cv2.contourArea(i) > 8000:
                card_boxes.append([cv2.contourArea(i), cv2.boundingRect(i)])
                x, y, w, h = cv2.boundingRect(i)
                cv2.rectangle(im, (x, y), (x + w, y + h), (0, 255, 0), 2)
        # Card boxes should be the 4 smallest boxes by area, sort by area first then sort by x1 coord
        # Giving coordinates of cards in order.
        card_boxes = sorted(card_boxes)[:4]
        return sorted([i[1] for i in card_boxes])

    def _get_deal_button(self, coords):
        coord = coords["card3"]["coord"]
        self.deal_button = (coord[0], coord[3] + ((coord[3] - coord[1]) // 3))