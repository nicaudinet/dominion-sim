from copy import copy
import constants as const

class Card:
    def __init__(self, card_name):
        self.card_name = card_name
        self.price = const.price[card_name]

    def is_treasure(self):
        return hasattr(self, "value")

    def is_victory(self):
        return hasattr(self, "points")

    def is_action(self):
        return hasattr(self, "actions")

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

    def pick_up(self, card_name):

        if not self.is_valid_card(card_name):
            assert "Card is not valid for this board"

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

class Player():
    def __init__(self, board):
        self.board = board
        coppers = [Treasure("copper") for _ in range(7)]
        estates = [Victory("estate") for _ in range(3)]
        self.deck = set(coppers + estates)
        self.discard_pile = set([])
        self.hand = None
        self.draw_hand()

    def shuffle(self):
        self.deck = copy(self.discard_pile)
        self.discard_pile = set()

    def draw_hand(self):
        deck = list(self.deck)
        self.hand = set(deck[:5])
        self.deck = deck[5:]

    def discard_hand(self):
        self.discard_pile.update(self.hand)
        self.draw_hand()

    def hand_value(self):
        treasure_cards = filter(lambda c: c.is_treasure(), self.hand)
        return sum(c.value for c in treasure_cards)

    def buy(self, card_name):
        if Card(card_name).price <= self.hand_value():
            card = self.board.pick_up(card_name)
            self.discard_pile.add(card)

def big_money(player):
    treasure_total = player.hand_value()
    if treasure_total >= 8:
        player.buy("province")
    elif treasure_total >= 6:
        player.buy("gold")
    elif treasure_total >= 4:
        player.buy("silver")
    player.discard_hand()

if __name__ == "__main__":
    
    board = Board()

    player1 = Player(board)
    player2 = Player(board)

    big_money(player1)
    big_money(player2)
