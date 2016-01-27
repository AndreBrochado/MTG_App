# -*- coding: utf-8 -*-

from mkmsdk.mkm import mkm
import os
from urllib.parse import quote_plus

""" Card JSON Example:

card1 = {
    name = "Lightning Bolt",
    expansion = "Magic 2010",
    normal_quantity = 42
    foil_quantity = 42
}


"""

#os.environ['MKM_APP_TOKEN'] =
#os.environ['MKM_APP_SECRET'] =
#os.environ['MKM_ACCESS_TOKEN'] =
#os.environ['MKM_ACCESS_TOKEN_SECRET'] =

class EditionError(Exception):
    def __init__(self, card):
        self.card = card
    def log_error(self):
        file = open("error_log.txt", "a")
        file.write("Card: " + self.card['name'] + " Expansion: " + self.card['expansion'] + " - Not Found")
        file.close()

def get_card_price(mkm_cards_list, card, foil=False, price_guide="LOW"):
    for test_card in mkm_cards_list:
        if (test_card['expansion'] == card['expansion']):
            if (foil):
                return card['priceGuide']['LOWFOIL']
            else:
                return card['priceGuide'][price_guide]
    raise EditionError(card)

def sum_cards_price(cards_list):
    sum = 0
    for card in cards_list:
        response = mkm.market_place.products(name=quote_plus(card['name']), game=1, language=1, match=True)
        try:
            normal_price = get_card_price(response.json()['product'], card['expansion'])
            foil_price = get_card_price(response.json()['product'], card['expansion'], True)
            sum = sum + normal_price * card['normal_quantity'] + foil_price * card['foil_quantity']
        except EditionError(card) as e:
            e.log_error()
    return sum

# Main

cards_list = []# insert card parser here -> return json as in example
total = sum_cards_price(cards_list)
print(total)