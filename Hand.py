import pytesseract
from time import sleep
import os
from suits import Suits


class Hand:
    def __init__(self, screen, suits=Suits, os=os):
        self.screen = screen
        self.suits = suits
        self.cards = screen.build_locations(screen.screen)
        self.os = os

    def get_card_coord(self, card_num):
        return self.cards["card{0}".format(card_num)]["coord"]

    def set_card_rank(self, card_num, rank):
        self.cards["card{0}".format(card_num)]["rank"] = rank

    def get_card_rank(self, card_num):
        return self.cards["card{0}".format(card_num)]["rank"]

    def set_card_suit(self, card_num, suit):
        self.cards["card{0}".format(card_num)]["suit"] = suit

    def get_card_suit(self, card_num):
        return self.cards["card{0}".format(card_num)]["suit"]

    def get_hand(self):
        str = ""
        for i in range(1, 5):
            str += self.cards["card{0}".format(i)]["rank"] + self.cards["card{0}".format(i)]["suit"] + " "
        return str

    def determine_rank(self, card_num, ocr=pytesseract):
        # Rank makes up about 27% of the card, suit makes up about 25%
        x1, y1, x2, y2 = self.get_card_coord(card_num)
        rank_offset = int((y2 - y1) * 0.27)
        rank = self.screen.image_grabber.grab((x1, y1, x1 + rank_offset, y1 + rank_offset))
        rank = rank.convert("1")  # Convert to black/white for better detection.
        rank_str = ocr.image_to_string(rank, config='-psm 10000 -c tessedit_char_whitelist=0123456789JQKA')
        rank_str = self._check_possible_misdetections(rank_str)
        if len(rank_str) == 0 or len(rank_str) > 1:
            print("There was a problem detecting rank. Detected as {0}. Retrying".format(rank_str))
            sleep(1)
            return self.determine_rank(card_num)
        return rank_str

    def determine_suit(self, card_num):
        x1, y1, x2, y2 = self.get_card_coord(card_num)
        suit_offset = int((y2 - y1) * 0.25)
        suit = self.screen.image_grabber.grab((x1, y1 + suit_offset, x1 + suit_offset, y1 + (suit_offset * 2)))
        pixel_colour = suit.getpixel((suit_offset // 2, suit_offset // 2))
        suit_filesize = self._process_suit(suit, card_num)
        if pixel_colour[0] > 165:  # red suit
            abs_diff_diamond = abs(suit_filesize - self.suits["diamond"])
            abs_diff_heart = abs(suit_filesize - self.suits["heart"])
            return "D" if abs_diff_diamond < abs_diff_heart else "H"
        else:  # black suit
            abs_diff_spade = abs(suit_filesize - self.suits["spade"])
            abs_diff_club = abs(suit_filesize - self.suits["club"])
            if self.get_card_rank(card_num) == "Q":  # Bottom part of Queen clips into suit causing misdetection.
                abs_diff_spade = abs(suit_filesize - self.suits["q_spade"])
            return "C" if abs_diff_club < abs_diff_spade else "S"

    def get_ranks_and_suits(self):
        for i in range(1, 5):
            rank = self.determine_rank(i)
            self.set_card_rank(i, rank)
            suit = self.determine_suit(i)
            self.set_card_suit(i, suit)

    def get_cards_status(self):
        img = self.screen.image_grabber.grab()
        ready = False
        for i in range(1, 5):
            coord = self.get_card_coord(i)
            pixel_colour = img.getpixel((coord[0] + 55, coord[1] + 2))
            if pixel_colour[0] > 240 and pixel_colour[1] > 240 and pixel_colour[2] > 240:
                ready = True
            else:
                ready = False
        if img.getpixel((self.get_card_coord(2)[2] + 50, self.get_card_coord(2)[1] + 50))[0] > 25:
            ready = False
        return ready

    def _process_suit(self, img, card_num):
        suit = img.convert("L")
        suit = img.resize((30, 30))
        suit_filename = "screen" + str(self.screen.number) + "_card" + str(card_num) + ".png"
        suit.save("detections/" + suit_filename)
        suit_filesize = self.os.path.getsize("detections/" + suit_filename)
        return suit_filesize

    def _check_possible_misdetections(self, detection):
        result = detection
        if detection == "10":
            result = "T"
        if detection == "0":
            result = "Q"
        return result

