import unittest
from unittest import mock
from unittest.mock import MagicMock
from screen import Screen
import win32api


class ScreenTest(unittest.TestCase):
    def setUp(self):
        self.screen = Screen(1)

    def test_screen_setup(self):
        res = (win32api.GetSystemMetrics(0), win32api.GetSystemMetrics(1))
        self.assertEqual(self.screen.res, res)