import unittest
import random

from board import Board
from player import Player
from cards import *

treasure_cards = [Copper(), Silver(), Gold()]
victory_cards = [Estate(), Duchy(), Province()]
action_cards = [Smithy(), Mine()]
all_cards = treasure_cards + victory_cards + action_cards

class TestCard(unittest.TestCase):

    def test_is_treasure(self):
        card = random.choice(treasure_cards)
        self.assertTrue(card.is_treasure())
        card = random.choice(victory_cards + action_cards)
        self.assertFalse(card.is_treasure())

    def test_is_victory(self):
        card = random.choice(victory_cards)
        self.assertTrue(card.is_victory())
        card = random.choice(treasure_cards + action_cards)
        self.assertFalse(card.is_victory())

    def test_is_action(self):
        card = random.choice(action_cards)
        self.assertTrue(card.is_action())
        card = random.choice(victory_cards + treasure_cards)
        self.assertFalse(card.is_action())

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

class TestRemodel(TestActionCard):

    def test_name(self):
        self.assertEqual(Remodel().name, "remodel")
    
    def test_play(self):
        remodel = Remodel()
        old_card = random.choice(all_cards)
        self.player.discard_pile = []
        self.player.hand = [old_card]
        valid_cards = [c for c in all_cards if c.price <= old_card.price + 2]
        new_card = random.choice(valid_cards)
        remodel.play(self.player, old_card, new_card)
        self.assertListEqual(self.player.discard_pile, [new_card])
        self.assertListEqual(self.player.hand, [])