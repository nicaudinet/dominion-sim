import unittest
import random

from cards import *
from player import Player
from board import Board 

class TestPlayer(unittest.TestCase):

    def setUp(self):
        self.board = Board()
        self.player = Player(self.board)

    def test_init_cards(self):
        init_cards = [Copper()] * 7 + [Estate()] * 3
        self.assertCountEqual(init_cards, self.player.all_cards())

    def test_draw_enough_cards_in_deck(self):
        """
        Test drawing cards with enough cards in the deck
        """
        cards = [Copper(), Copper(), Estate(), Estate(), Copper()]
        self.player.hand = []
        self.player.deck = cards
        self.player.draw(2)
        self.assertCountEqual(self.player.hand, [Copper(), Copper()])
        self.assertCountEqual(self.player.deck, [Copper(), Estate(), Estate()])

    def test_draw_enough_cards(self):
        """
        Test drawing cards with not enough cards in the deck but enough total
        cards
        """
        self.player.deck = [Copper(), Silver()]
        self.player.discard_pile = [Gold()]
        self.player.hand = []
        self.player.draw(3)
        self.assertCountEqual(self.player.hand, [Copper(), Silver(), Gold()])
        self.assertCountEqual(self.player.deck, [])

    def test_draw_not_enough_cards(self):
        """
        Test drawing cards with not enough cards total
        """
        self.player.deck = [Copper(), Silver()]
        self.player.discard_pile = [Gold()]
        self.player.hand = []
        self.player.draw(5)
        self.assertCountEqual(self.player.hand, [Copper(), Silver(), Gold()])
        self.assertCountEqual(self.player.deck, [])

    def test_turn(self):
        """
        Play through the first couple of turns for the DoNothing strategy
        """
        random.seed(0)
        # Init player with known card order
        self.player.hand = []
        self.discard_pile = []
        self.player.deck = [Copper()] * 7 + [Estate()] * 3
        self.player.draw_hand()
        # Play first turn
        self.player.play_turn()
        self.assertCountEqual(self.player.hand, [Copper()] * 2 + [Estate()] * 3)
        self.assertCountEqual(self.player.deck, [])
        self.assertCountEqual(self.player.discard_pile, [Copper()] * 5)
        # Play second turn
        self.player.play_turn()
        self.assertCountEqual(self.player.hand, [Copper()] * 3 + [Estate()] * 2)
        self.assertCountEqual(self.player.deck, [Copper()] * 4 + [Estate()])
        self.assertCountEqual(self.player.discard_pile, [])
