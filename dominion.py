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
    def __init__(self, board):
        self.board = board
        self.discard_pile = []
        self.hand = []

        coppers = [Treasure("copper") for _ in range(7)]
        estates = [Victory("estate") for _ in range(3)]
        self.deck = coppers + estates
        random.shuffle(self.deck)

        self.draw_hand()

    def recycle(self):
        random.shuffle(self.discard_pile)
        self.deck += self.discard_pile
        self.discard_pile = []

    def draw_hand(self):
        if len(self.deck) < 5:
            self.recycle()
        self.hand = self.deck[:5]
        self.deck = self.deck[5:]
        print([c.name for c in self.hand])

    def discard_hand(self):
        self.discard_pile += self.hand
        self.draw_hand()

    def hand_value(self):
        treasure_cards = filter(lambda c: c.is_treasure(), self.hand)
        return sum(c.value for c in treasure_cards)

    def total_points(self):
        all_cards = self.deck + self.hand + self.discard_pile
        victory_cards = filter(lambda c: c.is_victory(), all_cards)
        return sum(c.points for c in victory_cards)

    def buy(self, card_name):
        if Card(card_name).price <= self.hand_value():
            card = self.board.pick_up(card_name)
            if card is None:
                return False
            else:
                self.discard_pile += [card]
                print(f"Bought {card_name}")
                return True

def big_money(player):
    treasure_total = player.hand_value()
    if treasure_total >= 8:
        player.buy("province")
    elif treasure_total >= 6:
        player.buy("gold")
    elif treasure_total >= 3:
        player.buy("silver")

def play_turn(player):
    big_money(player)
    player.discard_hand()
    return player.board.game_over()

def play_game():

    board = Board()
    player1 = Player(board)
    player2 = Player(board)

    while True:
        if play_turn(player1): break
        if play_turn(player2): break
        print("--")
    
    return player1.total_points(), player2.total_points()

if __name__ == "__main__":

    p1_points, p2_points = play_game()

    if p1_points > p2_points:
        print("P1 is the winner")
    elif p1_points < p2_points:
        print("P2 is the winner")
    else:
        print("It's a draw")


