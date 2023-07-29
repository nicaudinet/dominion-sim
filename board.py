import random
import constants as const

class Card:
    def __init__(self, card_name):
        self.name = card_name
        self.price = const.price[card_name]

    def is_treasure(self):
        return hasattr(self, "value")

    def is_victory(self):
        return hasattr(self, "points")

    def is_action(self):
        return hasattr(self, "actions")

    def __eq__(self, other):
        if isinstance(other, str):
            return self.name == other
        elif isinstance(other, Card):
            return self.name == other.name
        else:
            raise Exception("Cannot compare Card to something that is not a string or a Card")

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name

class Treasure(Card):
    def __init__(self, card_name):
        super().__init__(card_name)
        self.value = const.value[card_name]

class Victory(Card):
    def __init__(self, card_name):
        super().__init__(card_name)
        self.points = const.points[card_name]

class Action(Card):
    def __init__(self, card_name):
        super().__init__(card_name)
        self.action = None # FIXME

class Board:
    def __init__(self):
        self.piles = {
            # Treasure Cards
            "copper": 20,
            "silver": 20,
            "gold": 20,
            # Victory Cards
            "estate": 20,
            "duchy": 20,
            "province": 20,
            # Action Cards
            # "cellar": 12,
            # "moat": 12,
            # "village": 12,
            "smithy": 12,
            # "remodel": 12,
            # "workshop": 12,
            "mine": 12,
            # "market": 12,
            # "militia": 12,
            # "woodcutter": 12,
        }

    def is_valid_card(self, card_name):
        return card_name in self.piles.keys()

    def is_treasure(self, card_name):
        return card_name in ["copper", "silver", "gold"]
    
    def is_victory(self, card_name):
        return card_name in ["estate", "duchy", "province"]

    def is_action(self, card_name):
        A = self.is_valid_card(card_name)
        B = self.is_treasure(card_name) or self.is_victory(card_name)
        return A and (not B)

    def num_empty_piles(self):
        return len(list(filter(lambda i: i == 0, self.piles.values())))

    def pick_up(self, card_name):

        if not self.is_valid_card(card_name):
            assert "Card name was not recognized"

        if self.piles[card_name] == 0:
            return None
        else:
            self.piles[card_name] -= 1
        
        if self.is_treasure(card_name):
            return Treasure(card_name)

        elif self.is_victory(card_name):
            return Victory(card_name)

        elif self.is_action(card_name):
            return Action(card_name)

    def game_over(self):
        return self.piles["province"] == 0 or self.num_empty_piles() == 3

