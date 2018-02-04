import unittest
from unittest import mock
from unittest.mock import MagicMock, patch
from screen import Screen
import win32api


class ScreenTest(unittest.TestCase):
    def setUp(self):
        win_api = MagicMock()
        self.res_return = 500
        win_api.GetSystemMetrics.return_value = self.res_return
        self.screen = Screen(1, win_api)

    def test_setup_sets_resolution(self):
        self.assertEqual(self.screen.res, (self.res_return,self.res_return))

    def test_setup_sets_x_offset(self):
        self.assertEqual(self.screen.x_offset, self.res_return // 2)

    def test_setup_sets_y_offset(self):
        self.assertEqual(self.screen.y_offset, self.res_return // 2)

    # def random_test(self):
    #     with patch('win32api.GetSystemMetrics', return_value='meme'):
    #         res = self.screen.res
    #         print(res)