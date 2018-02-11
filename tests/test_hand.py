from hand import Hand
import unittest
from unittest import mock
from unittest.mock import MagicMock


class HandTest(unittest.TestCase):
    def setUp(self):
        screen = MagicMock()
        self.cards = {"card1": {"coord": (0, 0, 0, 0)}}
        screen.screen.return_value = 1
        screen.build_locations.return_value = self.cards
        self.hand = Hand(screen)

    def test_get_card_coord(self):
        self.assertEqual(self.hand.get_card_coord(1), self.cards["card1"]["coord"])

    def test_set_card_rank(self):
        self.hand.set_card_rank(1, "5")
        self.assertEqual(self.hand.cards["card1"]["rank"], "5")

    def test_get_card_rank(self):
        self.hand.set_card_rank(1, "5")
        self.assertEqual(self.hand.get_card_rank(1), "5")

