from hand import Hand
from screen import Screen
import unittest
from unittest import mock
from unittest.mock import MagicMock, patch


class HandTest(unittest.TestCase):
    def setUp(self):
        screen = MagicMock()
        self.img = MagicMock()
        screen.image_grabber.grab.return_value = self.img
        self.cards = {"card{0}".format(i): {"coord": (0, 0, 5, 5)} for i in range(1, 5)}
        screen.screen.return_value = 1
        screen.build_locations.return_value = self.cards
        self.os = MagicMock()
        self.suits = {"heart": 170, "diamond": 180, "club": 164, "spade": 160}
        self.hand = Hand(screen, self.suits, self.os)
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

    def test_determine_correct_rank(self):
        self.img.convert.return_value = True
        self.ocr.image_to_string.return_value = "5"
        self.assertEqual(self.hand.determine_rank(1, ocr=self.ocr), "5")

    def test_determine_correct_rank_10(self):
        self.img.convert.return_value = True
        self.ocr.image_to_string.return_value = "10"
        self.assertEqual(self.hand.determine_rank(1, ocr=self.ocr), "T")

    def test_determine_correct_rank_0(self):
        self.img.convert.return_value = True
        self.ocr.image_to_string.return_value = "0"
        self.assertEqual(self.hand.determine_rank(1, ocr=self.ocr), "Q")

    def test_determine_correct_suit_H(self):
        self.img.getpixel.return_value = [170, 170, 170]
        self.os.path.getsize.return_value = 175
        self.assertEqual(self.hand.determine_suit(1), "H")

    def test_determine_correct_suit_D(self):
        self.img.getpixel.return_value = [170, 170, 170]
        self.os.path.getsize.return_value = 179
        self.assertEqual(self.hand.determine_suit(1), "D")

    def test_determine_correct_suit_C(self):
        self.hand.set_card_rank(1, "5")
        self.img.getpixel.return_value = [164, 170, 170]
        self.os.path.getsize.return_value = 164
        self.assertEqual(self.hand.determine_suit(1), "C")

    def test_determine_correct_suit_S(self):
        self.hand.set_card_rank(1, "5")
        self.img.getpixel.return_value = [161, 170, 170]
        self.os.path.getsize.return_value = 161
        self.assertEqual(self.hand.determine_suit(1), "S")

    def test_card_status_false(self):
        self.img.getpixel.return_value = [161, 170, 170]
        self.assertFalse(self.hand.get_cards_status())

    def test_card_status_true(self):
        self.img.getpixel.return_value = [277, 277, 277]
        self.assertFalse(self.hand.get_cards_status())

    def test_get_hand(self):
        for i in range(1,5):
            self.hand.set_card_rank(i, "5")
            self.hand.set_card_suit(i, "h")
        self.assertEqual(self.hand.get_hand(), "5h 5h 5h 5h ")

    # @patch('hand.Hand.determine_rank')
    # @patch('hand.Hand.determine_suit')
    # def test_get_ranks_and_suits(self):
    #     self.hand.get_ranks_and_suits()
    #     self.hand.determine_rank.assert_called()