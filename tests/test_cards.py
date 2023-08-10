import unittest

from board import Board
from player import Player
from cards import *

class TestActionCard(unittest.TestCase):

    def setUp(self):
        self.board = Board()
        self.player = Player(self.board)

class TestSmithy(TestActionCard):

    def test_name(self):
        self.assertEqual(Smithy().name, "smithy")

    def test_play(self):
        smithy = Smithy()
        smithy.play(self.player)
        self.assertEqual(len(self.player.hand), 8)

class TestMine(TestActionCard):

    def test_name(self):
        self.assertEqual(Mine().name, "mine")

    def test_play(self):
        mine = Mine()
        self.player.hand = ["copper"]
        mine.play(self.player, "copper")
        self.assertTrue("silver" in self.player.hand)
        self.player.hand = ["silver"]
        mine.play(self.player, "silver")
        self.assertTrue("gold" in self.player.hand)
        hand = ["estate", "gold"]
        self.player.hand = hand
        mine.play(self.player, "gold")
        self.assertEqual(self.player.hand, hand)