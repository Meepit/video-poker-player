import pytesseract


class Hand:
    def __init__(self, screen):
        self.screen = screen
        self.cards = screen.build_locations(screen.screen)

    def get_card_coord(self, card_num):
        return self.cards["card{0}".format(card_num)]["coord"]

    def set_card_rank(self, card_num, rank):
        self.cards["card{0}".format(card_num)]["rank"] = rank

    def get_card_rank(self, card_num):
        return self.cards["card{0}".format(card_num)]["rank"]

    def set_card_suit(self, card_num, suit):
        self.cards["card{0}".format(card_num)]["rank"] = suit

    def get_card_suit(self, card_num):
        return self.cards["card{0}".format(card_num)]["suit"]

    def determine_rank(self, card_num, ocr=pytesseract):
        # Rank makes up about 27% of the card, suit makes up about 25%
        x1, y1, x2, y2 = self.get_card_coord(card_num)
        rank_offset = int((y2 - y1) * 0.27)
        rank = self.screen.image_grabber.grab((x1, y1, x1 + rank_offset, y1 + rank_offset))
        rank = rank.convert("1")  # Convert to black/white for better detection.
        rank_str = ocr.image_to_string(rank, config='-psm 10000 -c tessedit_char_whitelist=0123456789JQKA')
        if rank_str == "10":
            rank_str = "T"
        if rank_str == "0":
            rank_str = "Q"
        if len(rank_str) == 0 or len(rank_str) > 1:
            print("There was a problem detecting rank. Detected as {0}. Retrying".format(rank_str))
            #time.sleep(1)
            return self.determine_rank(card_num)
        return rank_str