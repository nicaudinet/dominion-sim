import time
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
            # "smithy": 12,
            # "remodel": 12,
            # "workshop": 12,
            # "mine": 12,
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

class Player():
    def __init__(self, board, strategy, debug=False):
        self.board = board
        self.strategy = strategy(self)
        self.debug = debug

        coppers = [Treasure("copper") for _ in range(7)]
        estates = [Victory("estate") for _ in range(3)]
        self.deck = coppers + estates
        random.shuffle(self.deck)
        self.hand = []
        self.discard_pile = []

        self.draw_hand()

    def all_cards(self):
        return self.deck + self.hand + self.discard_pile

    def recycle(self):
        random.shuffle(self.discard_pile)
        self.deck += self.discard_pile
        self.discard_pile = []

    def draw(self, n):
        if len(self.deck) < n:
            self.recycle()
        self.hand += self.deck[:n]
        self.deck = self.deck[n:]

    def draw_hand(self):
        self.hand = []
        self.draw(5)
        if self.debug: print(sorted([c.name for c in self.hand]))

    def discard_hand(self):
        self.discard_pile += self.hand
        self.draw_hand()

    def hand_value(self):
        treasure_cards = filter(lambda c: c.is_treasure(), self.hand)
        return sum(c.value for c in treasure_cards)

    def total_points(self):
        victory_cards = filter(lambda c: c.is_victory(), self.all_cards())
        return sum(c.points for c in victory_cards)

    def buy(self, card_name):
        if Card(card_name).price <= self.hand_value():
            card = self.board.pick_up(card_name)
            if card is None:
                return False
            else:
                self.discard_pile += [card]
                if self.debug: print(f"Bought {card_name}")
                return True

    def play(self):
        self.strategy.play()
        self.discard_hand()
        return self.board.game_over()

class BigMoney:
    """
    The simplest Big Money strategy: when you can, buy a province, if not buy a
    gold, if not buy a silver, otherwise buy nothing
    """
    def __init__(self, player):
        self.player = player

    def play(self):
        treasure_total = self.player.hand_value()
        if treasure_total >= 8:
            self.player.buy("province")
        elif treasure_total >= 6:
            self.player.buy("gold")
        elif treasure_total >= 3:
            self.player.buy("silver")

def play_game():

    board = Board()
    player1 = Player(board, BigMoney)
    player2 = Player(board, BigMoney)

    while True:
        if player1.play(): break
        if player2.play(): break
    
    return player1.total_points(), player2.total_points()

if __name__ == "__main__":

    p1_wins = 0
    p2_wins = 0
    ties = 0

    for i in range(1000):
        print(f"Game {i}")
        p1, p2 = play_game()
        if p1 > p2:
            p1_wins += 1
        elif p1 < p2:
            p2_wins += 1
        else:
            ties += 1

    print("P1 wins:", p1_wins)
    print("P2 wins:", p2_wins)
    print("Ties:", ties)
