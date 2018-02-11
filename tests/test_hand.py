from hand import Hand
from screen import Screen
import unittest
from unittest import mock
from unittest.mock import MagicMock, patch


class HandTest(unittest.TestCase):
    def setUp(self):
        screen = MagicMock()
        self.img = MagicMock()
        screen.screen_grabber.grab.return_value = self.img
        self.cards = {"card1": {"coord": (0, 0, 5, 5)}}
        screen.screen.return_value = 1
        screen.build_locations.return_value = self.cards
        self.hand = Hand(screen)
        self.ocr = MagicMock()

    def test_get_card_coord(self):
        self.assertEqual(self.hand.get_card_coord(1), self.cards["card1"]["coord"])

    def test_set_card_rank(self):
        self.hand.set_card_rank(1, "5")
        self.assertEqual(self.hand.cards["card1"]["rank"], "5")

    def test_get_card_rank(self):
        self.hand.set_card_rank(1, "5")
        self.assertEqual(self.hand.get_card_rank(1), "5")

    def test_set_card_suit(self):
        self.hand.set_card_rank(1, "H")
        self.assertEqual(self.hand.cards["card1"]["rank"], "H")

    def test_get_card_suit(self):
        self.hand.set_card_rank(1, "H")
        self.assertEqual(self.hand.get_card_rank(1), "H")

    def test_determine_rank(self):
        self.img.convert.return_value = True
        self.ocr.image_to_string.return_value = "5"
        self.assertEqual(self.hand.determine_rank(1, ocr=self.ocr), "5")

