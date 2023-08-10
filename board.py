import random
from cards import *

class Board:
    def __init__(self):
        # The numbers are set for a 2-player game according to the Dominion wiki
        self.piles = {
            # Treasure Cards
            "copper": [Copper() for _ in range(60)],
            "silver": [Silver() for _ in range(40)],
            "gold": [Gold() for _ in range(30)],
            # Victory Cards
            "estate": [Estate() for _ in range(8 + 6)],
            "duchy": [Duchy() for _ in range(8)],
            "province": [Province() for _ in range(8)],
            # Action Cards
            # "cellar": 12,
            # "moat": 12,
            # "village": 12,
            "smithy": [Smithy() for _ in range(12)],
            "remodel": [Remodel() for _ in range(12)],
            # "workshop": 12,
            "mine": [Mine() for _ in range(12)],
            # "market": 12,
            # "militia": 12,
            # "woodcutter": 12,
        }

    def is_valid_card(self, card_name):
        return card_name in self.piles.keys()

    def num_empty_piles(self):
        return sum([1 for i in self.piles.values() if len(i) == 0])

    def pick_up(self, card_name):

        if not self.is_valid_card(card_name):
            assert "Card name was not recognized"

        pile = self.piles[card_name]
        if len(pile) == 0:
            return None
        else:
            return pile.pop()
        
    def game_over(self):
        return len(self.piles["province"]) == 0 or self.num_empty_piles() == 3
