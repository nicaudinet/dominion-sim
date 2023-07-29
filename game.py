from board import *
from player import *
from strategy import *

def play_game():

    board = Board()
    player1 = Player(board, MineBigMoney)
    player2 = Player(board, SmithyBigMoney)

    while True:
        if player1.play(): break
        if player2.play(): break
    
    return player1.total_points(), player2.total_points()

if __name__ == "__main__":

    p1_wins = 0
    p2_wins = 0
    ties = 0

    for i in range(1000):
        print(f"Game {i}")
        p1, p2 = play_game()
        if p1 > p2:
            p1_wins += 1
        elif p1 < p2:
            p2_wins += 1
        else:
            ties += 1

    print("P1 wins:", p1_wins)
    print("P2 wins:", p2_wins)
    print("Ties:", ties)
