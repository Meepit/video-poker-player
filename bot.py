import requests


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

    def _build_url(self):
        ranks = '23456789tjqka'
        suits = 'hsdc'
        output = []
        url_suffix = '&game=0&payouts=1200%20239.8%20120%2018%2015%2011%205%203%202'
        for i in range(1, 5):
            prefix = str(ranks.index(self.hand.get_card_rank(i).lower()) + 13 * suits.index(self.hand.get_card_suit(i).lower()))
            output.append(prefix)
        return 'http://www.beatingbonuses.com/pick_exec.php?player=' + "%20".join(output) + url_suffix
