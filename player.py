import random
from board import *
from strategy import DoNothing

class Player():
    def __init__(self, board, strategy=DoNothing, debug=False, name=None):
        self.board = board
        self.strategy = strategy(self)
        self.debug = debug
        self.name = name

        self.deck = []
        self.hand = []
        self.discard_pile = []
        self.in_play = []

        for _ in range(7):
            self.gain(Copper())
        for _ in range(3):
            self.gain(Estate())
        self.draw_hand()

    def all_cards(self):
        return self.deck + self.hand + self.discard_pile + self.in_play

    def card_summary(self):
        cards = self.all_cards()
        unique_cards = set([c.name for c in cards])
        summary = {}
        for card_name in unique_cards:
            summary[card_name] = sum([1 for c in cards if c == card_name])
        return summary

    def draw(self, n):
        if len(self.deck + self.discard_pile) < n:
            self.hand += self.deck
            self.hand += self.discard_pile
            self.deck = []
            self.discard_pile = []
        elif len(self.deck) < n:
            random.shuffle(self.discard_pile)
            self.deck += self.discard_pile
            self.discard_pile = []
            self.hand += self.deck[:n]
            self.deck = self.deck[n:]
        else:
            self.hand += self.deck[:n]
            self.deck = self.deck[n:]

    def draw_hand(self):
        self.draw(5)

    def discard_hand(self):
        self.discard_pile += self.hand
        self.discard_pile += self.in_play
        self.hand = []
        self.in_play = []

    def hand_value(self):
        treasure_cards = filter(lambda c: c.is_treasure(), self.hand)
        return sum(c.value for c in treasure_cards)

    def total_points(self):
        victory_cards = filter(lambda c: c.is_victory(), self.all_cards())
        return sum(c.points for c in victory_cards)

    def trash(self, card_name):
        try:
            self.hand.remove(card_name)
        except ValueError:
            pass # Do nothing if card is not in hand

    def gain(self, card_name):
        card = self.board.pick_up(card_name) 
        if card is None:
            return False
        else:
            self.discard_pile += [card]
            return True 

    def gain_hand(self, card_name):
        card = self.board.pick_up(card_name) 
        if card is None:
            return False
        else:
            self.hand += [card]
            return True 

    def buy(self, card_name):
        if Card(card_name).price <= self.hand_value():
            if self.debug:
                if self.name is not None: print(" - ", end="")
                print("Final hand:  ", sorted(self.hand))
            success = self.gain(card_name)
            if success and self.debug:
                if self.name is not None: print(" - ", end="")
                print(f"Bought {card_name}")
            return success

    def use_card(self, card_name):
        if card_name in self.hand:
            card = self.hand.pop(self.hand.index(card_name))
            self.in_play.append(card)
            if self.debug:
                if self.name is not None: print(" - ", end="")
                print("Played", card.name)
            return card
        else:
            return None

    def play_turn(self):
        if self.debug:
            if self.name is not None:
                print(self.name + ":")
                print(" - ", end="")
            print("Initial hand:", sorted(self.hand))
        self.strategy.play()
        self.discard_hand()
        self.draw_hand()
        if self.debug: print("")
        return self.board.game_over()
