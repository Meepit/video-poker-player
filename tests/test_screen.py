import unittest
from unittest import mock
from unittest.mock import MagicMock, patch
from screen import Screen
import win32api


class ScreenTest(unittest.TestCase):
    def setUp(self):
        win_api = MagicMock()
        screen_grabber = MagicMock()
        screen_grabber.grab.return_value = None
        self.res_return = 500
        win_api.GetSystemMetrics.return_value = self.res_return
        self.screen = Screen(1, win_api, screen_grabber)

    def test_setup_sets_resolution(self):
        self.assertEqual(self.screen.res, (self.res_return,self.res_return))

    def test_setup_sets_x_offset(self):
        self.assertEqual(self.screen.x_offset, 0)

    def test_setup_sets_y_offset(self):
        self.assertEqual(self.screen.y_offset, 0)

    def test_get_screen(self):
        self.screen.get_screen(self.screen.number)
        self.screen.image_grabber.grab.assert_called()

    def test_invalid_screen_number(self):
        with self.assertRaises(ValueError):
            self.screen.get_screen(5)

    def test_build_card_locations(self):
        with patch('screen.Screen._get_card_locations', return_value=[(0, 0, 0, 0), (0, 0, 0, 0), (0, 0, 0, 0), (0, 0, 0, 0)]):
            self.screen.build_card_locations("img")
            self.screen._get_card_locations.assert_called()

    # def random_test(self):
    #     with patch('win32api.GetSystemMetrics', return_value='meme'):
    #         res = self.screen.res
    #         prines)t(r