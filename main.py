
from dice import Dice
from board import Board
from player import Player

dices = Dice()
player1 = Player("w")
player2 = Player("b")
board = Board()

roll_player1 = roll_player2 = None
while roll_player1 == roll_player2:
    roll_player1 = sum(dices.roll_dices())
    roll_player2 = sum(dices.roll_dices())
player = player1 if roll_player1 > roll_player2 else player2
print(f"Player {player.color} starts first...")

dices.roll_dices()
while not player.winner:

    if board.get_indexes(dices.rolled_dices, player):
        print(f"Board: {board.board}")
        player.select_move(board.moves)
        board.play_move(player.choice)
        dices.rolled_dices.remove(player.choice[2])
    else:
        player = player2 if player == player1 else player1
        dices.roll_dices()

print(f"Player {player.color} won the game.")
