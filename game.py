from board import *
from player import *
from strategy import *

def print_deck(player):
    for name, num in sorted(player.card_summary().items()):
        print(f" - {name}: {num}")

def play_game(debug=False):

    board = Board()
    player1 = Player(board, BigMoney, debug=False, name="Player1")
    player2 = Player(board, MineBigMoney, debug=debug, name="Player2")

    while True:
        if player1.play_turn(): break
        if player2.play_turn(): break

    if debug:
        print("Player 1 cards:")
        print_deck(player1)
        print("")
        print("Player 2 cards:")
        print_deck(player2)
        print("")
    
    return player1.total_points(), player2.total_points()

if __name__ == "__main__":

    debug = True

    p1_wins = 0
    p2_wins = 0
    ties = 0

    for i in range(1):
        print(f"Game {i}")
        if debug: print("---------")
        p1, p2 = play_game(debug)
        if p1 > p2:
            p1_wins += 1
        elif p1 < p2:
            p2_wins += 1
        else:
            ties += 1

    print("P1 wins:", p1_wins)
    print("P2 wins:", p2_wins)
    print("Ties:", ties)
