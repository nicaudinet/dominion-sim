from player import *

class Strategy:
    def __init__(self, player):
        self.player = player

    def _action_phase(self):
        assert False, "Not implemented"
    
    def _buy_phase(self):
        assert False, "Not implemented"

    def play(self):
        self._action_phase()
        self._buy_phase()

class DoNothing(Strategy):
    def __init__(self, player):
        super().__init__(player)

    def _action_phase(self):
        pass

    def _buy_phase(self):
        pass

class BigMoney(Strategy):
    """
    The simplest Big Money strategy: when you can, buy a province, if not buy a
    gold, if not buy a silver, otherwise buy nothing
    """
    def __init__(self, player):
        super().__init__(player)

    def _action_phase(self):
        pass
    
    def _buy_phase(self):
        treasure_total = self.player.hand_value()
        if treasure_total >= 8:
            self.player.buy(Province())
        elif treasure_total >= 6:
            self.player.buy(Gold())
        elif treasure_total >= 3:
            self.player.buy(Silver())

class SmithyBigMoney(Strategy):
    """
    A classic variation on Big Money, where the player buys a single Smithy as
    soon as possible and then plays standard Big Money for the rest of the game
    """
    def __init__(self, player):
        super().__init__(player)
        self.has_smithy = False

    def _action_phase(self):
        smithy = self.player.use_card(Smithy())
        if smithy is not None:
            smithy.play(self.player)

    def _buy_phase(self):
        treasure_total = self.player.hand_value()
        if not self.has_smithy:
            if treasure_total >= 8:
                self.player.buy(Province())
            elif treasure_total >= 6:
                self.player.buy(Gold())
            elif treasure_total >= 4:
                self.player.buy(Smithy())
                self.has_smithy = True
            elif treasure_total >= 3:
                self.player.buy(Silver())
        else:
            if treasure_total >= 8:
                self.player.buy(Province())
            elif treasure_total >= 6:
                self.player.buy(Gold())
            elif treasure_total >= 3:
                self.player.buy(Silver())

class DoubleSmithy(Strategy):
    """
    Another variation on Big Money, where the player buys two Smithy cards as
    soon as possible and then plays standard Big Money for the rest of the game
    """
    def __init__(self, player):
        super().__init__(player)
        self.n_smithy = 0

    def _action_phase(self):
        smithy = self.player.use_card(Smithy())
        if smithy is not None:
            smithy.play(self.player)

    def _buy_phase(self):
        treasure_total = self.player.hand_value()
        if self.n_smithy < 2:
            if treasure_total >= 8:
                self.player.buy(Province())
            elif treasure_total >= 6:
                self.player.buy(Gold())
            elif treasure_total >= 4:
                self.player.buy(Smithy())
                self.n_smithy += 1
            elif treasure_total >= 3:
                self.player.buy(Silver())
        else:
            if treasure_total >= 8:
                self.player.buy(Province())
            elif treasure_total >= 6:
                self.player.buy(Gold())
            elif treasure_total >= 3:
                self.player.buy(Silver())

class MineBigMoney(Strategy):
    """
    A classic variation on Big Money, where the player buys a single Smithy as
    soon as possible and then plays standard Big Money for the rest of the game
    """
    def __init__(self, player):
        self.player = player
        self.has_mine = False

    def _action_phase(self):
        mine = self.player.use_card(Mine())
        if mine is None:
            pass
        else:
            if Silver() in self.player.hand:
                mine.play(self.player, Silver())
            elif Copper() in self.player.hand:
                mine.play(self.player, Copper())
            else:
                pass

    def _buy_phase(self):
        treasure_total = self.player.hand_value()
        if not self.has_mine:
            if treasure_total >= 5:
                self.player.buy(Mine())
                self.has_mine = True
            elif treasure_total >= 3:
                self.player.buy(Silver())
        else:
            if treasure_total >= 8:
                self.player.buy(Province())
            elif treasure_total >= 6:
                self.player.buy(Gold())
            elif treasure_total >= 3:
                self.player.buy(Silver())
