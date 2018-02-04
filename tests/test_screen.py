import unittest
from unittest import mock
from unittest.mock import MagicMock
from screen import Screen
import win32api


class ScreenTest(unittest.TestCase):
    def setUp(self):
        self.screen = Screen(1)

    def test_setup_sets_resolution(self):
        res = (win32api.GetSystemMetrics(0), win32api.GetSystemMetrics(1))
        self.assertEqual(self.screen.res, res)

    def test_setup_sets_x_offset(self):
        x_offset = win32api.GetSystemMetrics(0) // 2
        self.assertEqual(self.screen.x_offset, x_offset)

    def test_setup_sets_y_offset(self):
        y_offset = win32api.GetSystemMetrics(1) // 2
        self.assertEqual(self.screen.y_offset, y_offset)