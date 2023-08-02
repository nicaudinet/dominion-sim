import constants as const

###################
# Base Card Class #
###################

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

    def __eq__(self, other):
        if isinstance(other, str):
            return self.name == other
        elif isinstance(other, Card):
            return self.name == other.name
        else:
            raise Exception("Can only compare Card to a string or a Card")

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name

##################
# Treasure Cards #
##################

class Treasure(Card):
    def __init__(self, card_name, value):
        super().__init__(card_name)
        self.value = value

class Copper(Treasure):
    def __init__(self):
        super().__init__("copper", 1)

class Silver(Treasure):
    def __init__(self):
        super().__init__("silver", 2)

class Gold(Treasure):
    def __init__(self):
        super().__init__("gold", 3)

#################
# Victory Cards #
#################

class Victory(Card):
    def __init__(self, card_name, points):
        super().__init__(card_name)
        self.points = points

class Estate(Victory):
    def __init__(self):
        super().__init__("estate", 2)

class Duchy(Victory):
    def __init__(self):
        super().__init__("duchy", 5)

class Province(Victory):
    def __init__(self):
        super().__init__("province", 8)

################
# Action Cards #
################

class Action(Card):
    def __init__(self, card_name):
        super().__init__(card_name)

    def play(self):
        assert False, "Not Implemented"

class Smithy(Action):
    def __init__(self):
        super().__init__("smithy")

    def play(self, player):
        player.draw(3)

class Mine(Action):
    def __init__(self):
        super().__init__("mine")

    def play(self, player):
        if "silver" in player.hand:
            player.trash("silver")
            player.gain_hand("gold")
        elif "copper" in player.hand:
            player.trash("copper")
            player.gain_hand("silver")

