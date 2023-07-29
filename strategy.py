from player import *

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

class SmithyBigMoney:
    """
    A classic variation on Big Money, where the player buys a single Smithy as
    soon as possible and then plays standard Big Money for the rest of the game
    """
    def __init__(self, player):
        self.player = player
        self.has_smithy = False

    def _action_phase(self):
        if "smithy" in self.player.hand:
            self.player.draw(3)

    def _buy_phase(self):
        treasure_total = self.player.hand_value()
        if not self.has_smithy:
            if treasure_total >= 8:
                self.player.buy("province")
            elif treasure_total >= 6:
                self.player.buy("gold")
            elif treasure_total >= 4:
                self.player.buy("smithy")
                self.has_smithy = True
            elif treasure_total >= 3:
                self.player.buy("silver")
        else:
            if treasure_total >= 8:
                self.player.buy("province")
            elif treasure_total >= 6:
                self.player.buy("gold")
            elif treasure_total >= 3:
                self.player.buy("silver")

    def play(self):
        self._action_phase()
        self._buy_phase()

class DoubleSmithy:
    """
    Another variation on Big Money, where the player buys two Smithy cards as
    soon as possible and then plays standard Big Money for the rest of the game
    """
    def __init__(self, player):
        self.player = player
        self.n_smithy = 0

    def _action_phase(self):
        if "smithy" in self.player.hand:
            self.player.draw(3)

    def _buy_phase(self):
        treasure_total = self.player.hand_value()
        if self.n_smithy < 2:
            if treasure_total >= 8:
                self.player.buy("province")
            elif treasure_total >= 6:
                self.player.buy("gold")
            elif treasure_total >= 4:
                self.player.buy("smithy")
                self.has_smithy = True
            elif treasure_total >= 3:
                self.player.buy("silver")
        else:
            if treasure_total >= 8:
                self.player.buy("province")
            elif treasure_total >= 6:
                self.player.buy("gold")
            elif treasure_total >= 3:
                self.player.buy("silver")

    def play(self):
        self._action_phase()
        self._buy_phase()

