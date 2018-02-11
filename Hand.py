class Hand:
    def __init__(self, screen):
        self.screen = screen
        self.cards = screen.build_locations(screen.screen)

    def get_card_coord(self, card_num):
        return self.cards["card{0}".format(card_num)]["coord"]