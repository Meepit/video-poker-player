import requests
import time


class Bot:
    def __init__(self, hand, q, request = requests):
        self.hand = hand
        self.queue = q
        self.request = requests

    def calculate_action(self):
        url = self._build_url()
        try:
            r = self.request.get(url)
        except(requests.ConnectionError, requests.Timeout):
            print("Connection issue, retrying.")
            return self.calculate_action()
        evs = r.text.split(" ")
        return 3 if float(evs[0]) > float(evs[1]) else 4

    def add_to_queue(self, card=0, coord=()):
        if coord:
            self.queue.put(coord)
            return
        if card == 3:
            location = self.hand.get_card_coord(3)
            self.queue.put((location[0] + 20, location[1] + 20))
        elif card == 4:
            location = self.hand.get_card_coord(4)
            self.queue.put((location[0] + 20, location[1] + 20))

    def start(self):
        while True:
            print("Waiting for cards")
            while not self.hand.get_cards_status():
                pass
            time.sleep(0.5)  # failsafe
            # get card ranks and suits
            self.hand.get_ranks_and_suits()
            # Temporary fix to get around the issue of pickem poker client slowing down causing early detection#
            if self.hand.get_card_rank(1).lower() == "K":
                print("Retrying to be safe.")
                self.hand.get_ranks_and_suits()
            # End temp fix #
            print(self.hand.get_hand())
            action = self.calculate_action()
            self.add_to_queue(card=action)
            print("Choosing {0}".format(action))
            # Get deal button
            deal_button_xy = self.hand.screen.deal_button
            deal_button = self.hand.screen.image_grabber.grab((deal_button_xy[0], deal_button_xy[1], deal_button_xy[0] + 3, deal_button_xy[1] +3))
            deal_button_pixel_colour = deal_button.getpixel((2, 2))[0]
            if deal_button_pixel_colour <= 250:
                print("\tWaiting for deal button..")
            while not deal_button.getpixel((2, 2))[0] >= 200:  # Deal button not ready
                deal_button = self.hand.screen.image_grabber.grab((deal_button_xy[0], deal_button_xy[1], deal_button_xy[0] + 3, deal_button_xy[1] + 3))
            self.add_to_queue(coord=self.hand.screen.deal_button)
            # end deal button section

    def _build_url(self):
        ranks = '23456789tjqka'
        suits = 'hsdc'
        output = []
        url_suffix = '&game=0&payouts=1200%20239.8%20120%2018%2015%2011%205%203%202'
        for i in range(1, 5):
            prefix = str(ranks.index(self.hand.get_card_rank(i).lower()) + 13 * suits.index(self.hand.get_card_suit(i).lower()))
            output.append(prefix)
        return 'http://www.beatingbonuses.com/pick_exec.php?player=' + "%20".join(output) + url_suffix
