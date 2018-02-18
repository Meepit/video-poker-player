from hand import Hand
from screen import Screen
from bot import Bot
import unittest
from unittest import mock
from unittest.mock import MagicMock, patch


class BotTest(unittest.TestCase):
    def setUp(self):
        self.hand = MagicMock()
        self.hand.get_card_rank.return_value = "5"
        self.hand.get_card_suit.return_value = "d"
        self.request = MagicMock()
        self.req_obj = MagicMock()
        self.req_obj.text = "0.812 0.912"
        self.request.get.return_value = self.req_obj
        self.q = MagicMock()
        self.bot = Bot(self.hand, self.q, self.request)

    def test_calculate_action_3(self):
        self.assertEqual(self.bot.calculate_action(), 4)

    def test_calculate_action_4(self):
        self.req_obj.text = "0.912 0.812 "
        self.assertEqual(self.bot.calculate_action(), 4)



