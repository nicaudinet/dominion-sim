import unittest
import random

from player import Player
from board import Board 

class TestPlayer(unittest.TestCase):

    def setUp(self):
        self.board = Board()
        self.player = Player(self.board)

    def test_init_cards(self):
        init_cards = ["copper"] * 7 + ["estate"] * 3
        self.assertCountEqual(init_cards, self.player.all_cards())

    def test_draw_enough_cards_in_deck(self):
        """
        Test drawing cards with enough cards in the deck
        """
        cards = ["copper", "copper", "estate", "estate", "copper"]
        self.player.hand = []
        self.player.deck = cards
        self.player.draw(2)
        self.assertCountEqual(self.player.hand, ["copper", "copper"])
        self.assertCountEqual(self.player.deck, ["copper", "estate", "estate"])

    def test_draw_enough_cards(self):
        """
        Test drawing cards with not enough cards in the deck but enough total
        cards
        """
        self.player.deck = ["copper", "silver"]
        self.player.discard_pile = ["gold"]
        self.player.hand = []
        self.player.draw(3)
        self.assertCountEqual(self.player.hand, ["copper", "silver", "gold"])
        self.assertCountEqual(self.player.deck, [])

    def test_draw_not_enough_cards(self):
        """
        Test drawing cards with not enough cards total
        """
        self.player.deck = ["copper", "silver"]
        self.player.discard_pile = ["gold"]
        self.player.hand = []
        self.player.draw(5)
        self.assertCountEqual(self.player.hand, ["copper", "silver", "gold"])
        self.assertCountEqual(self.player.deck, [])

    def test_turn(self):
        """
        Play through the first couple of turns for the DoNothing strategy
        """
        random.seed(0)
        # Init player with known card order
        self.player.hand = []
        self.discard_pile = []
        self.player.deck = ["copper"] * 7 + ["estate"] * 3
        self.player.draw_hand()
        # Play first turn
        self.player.play_turn()
        self.assertCountEqual(self.player.hand, ["copper"] * 2 + ["estate"] * 3)
        self.assertCountEqual(self.player.deck, [])
        self.assertCountEqual(self.player.discard_pile, ["copper"] * 5)
        # Play second turn
        self.player.play_turn()
        self.assertCountEqual(self.player.hand, ["copper"] * 3 + ["estate"] * 2)
        self.assertCountEqual(self.player.deck, ["copper"] * 4 + ["estate"])
        self.assertCountEqual(self.player.discard_pile, [])
