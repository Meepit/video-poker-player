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

