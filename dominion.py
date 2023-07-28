from constants import prices, values, victory_points

class Card:
    def __init__(self, name):
        self.name = name
        self.price = prices[name]

class Treasure(Card):
    def __init__(self, name):
        super().__init__(name)
        self.value = values[name]

class Victory(Card):
    def __init__(self, name):
        super().__init__(name)
        self.points = victory_points[name]

class Action(Card):
    def __init__(self, name):
        super().__init__(name)
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
            "cellar": 12,
            "moat": 12,
            "village": 12,
            "smithy": 12,
            "remodel": 12,
            "workshop": 12,
            "mine": 12,
            "market": 12,
            "militia": 12,
            "woodcutter": 12,
        }

    def is_valid_card(self, card):
        return card in self.piles.keys()

    def is_treasure(self, card):
        return card in ["copper", "silver", "gold"]
    
    def is_victory(self, card):
        return card in ["estate", "duchy", "province"]

    def is_action(self, card):
        A = self.is_valid_card(card)
        B = self.is_treasure(card) or self.is_victory(card)
        return A and (not B)

    def draw(self, card):

        if not self.is_valid_card(card):
            assert "Card is not valid for this board"

        if self.piles[card] == 0:
            return None
        else:
            self.piles[card] -= 1

        if self.is_treasure(card):
            return Treasure(card)

        elif self.is_victory(card):
            return Victory(card)

        elif self.is_action(card):
            return Action(card)

if __name__ == "__main__":
    
    board = Board()
    card = board.draw("copper")
