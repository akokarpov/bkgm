
from itertools import groupby


class Board:

    def __init__(self) -> None:
        """The board is split into 2 parts.
        The parts are rotated when player changes."""
        self.board_whites = [
            [0, 12, None, "w", "w", "w", "w", "w", "w", "w",
             "w", "w", "w", "w", "w", "w", "w", "w"],
            [1, 13, None],
            [2, 14, None],
            [3, 15, None],
            [4, 16, None],
            [5, 17, None],
            [6, 18, None],
            [7, 19, None],
            [8, 20, None],
            [9, 21, None],
            [10, 22, None],
            [11, 23, None],
        ]
        self.board_blacks = [
            [12, 0, None, "b", "b", "b", "b", "b", "b", "b",
                "b", "b", "b", "b", "b", "b", "b", "b"],
            [13, 1, None],
            [14, 2, None],
            [15, 3, None],
            [16, 4, None],
            [17, 5, None],
            [18, 6, None],
            [19, 7, None],
            [20, 8, None],
            [21, 9, None],
            [22, 10, None],
            [23, 11, None],
        ]
        self.board = None
        self.player = None
        self.moves = None
        self.head_played = False

    def rotate_board(self, player_color):
        """Rotates the board according to player's turn."""
        if player_color == "w":
            self.board = self.board_whites + self.board_blacks
        else:
            self.board = self.board_blacks + self.board_whites

    def is_point_color(self, board_index):
        """Returns True if player's checker is at the point.
        When bearing off also returns True if out of index."""
        try:
            return self.board[board_index][-1] == self.player.color
        except IndexError:
            return self.player.bear_off == True

    def is_point_open(self, board_index):
        """Returns True if point is empty.
        When bearing off also returns True if out of index."""
        try:
            return self.board[board_index][-1] == None
        except IndexError:
            return self.player.bear_off == True

    def get_indexes(self, dices, player):
        """Checks and adds valid target indexes to a list for player's choice."""

        self.rotate_board(player.color)
        self.player = player
        self.moves = []

        # Check if player is allowed to start bearing off
        if sum([self.board[index].count(self.player.color) for index in range(0, 18)]) == 0:
            player.bear_off = True

        # Can play head a 2nd time if dice is doubled on first roll
        if self.board[0].count(self.player.color) == 14 and len(dices) == 3:
            self.head_played = False

        for start_index, _ in enumerate(self.board):
            if self.head_played and start_index == 0:
                continue
            for dice in dices:
                target_index = start_index + dice
                if not self.is_point_open(start_index) and self.is_point_color(start_index):
                    if self.is_point_open(target_index) or self.is_point_color(target_index):
                        if self.check_prime(start_index, target_index):
                            self.moves.append(
                                (start_index, target_index, dice))
        if self.moves == []:
            self.head_played = False
            return False
        else:
            return True

    def check_prime(self, start_index, target_index):
        """Checks and returns True if player's allowed to build a prime."""
        is_prime_legal = True
        if self.player.bear_off == True:
            return is_prime_legal
        self.move_checker(start_index, target_index)
        self.rotate_board(self.player.opponent_color)
        groups = groupby([point[-1] for point in self.board])
        result = [(point, sum(1 for _ in group))
                  for point, group in groups if point == self.player.color][0][1]
        if result > 5:
            if max(index for index, point in enumerate(
                self.board) if point[-1] == self.player.color) > \
                max(index for index, point in enumerate(
                    self.board) if point[-1] == self.player.opponent_color):
                is_prime_legal = False
        self.rotate_board(self.player.color)
        self.move_checker(target_index, start_index)
        return is_prime_legal

    def move_checker(self, start_index, target_index):
        """Moves the checker from start to target point."""
        moved_checker = self.board[start_index].pop(-1)
        if self.player.bear_off == False or \
                self.player.bear_off == True and \
                target_index < len(self.board):
            self.board[target_index].append(moved_checker)
        else:
            self.check_winner()

    def play_move(self, move):
        """Executes move according to player's choice."""
        if move[0] == 0:
            self.head_played = True
        self.move_checker(move[0], move[1])

    def check_winner(self):
        """Checks if all checkers are born off."""
        if sum([self.board[index].count(self.player.color) for index in range(len(self.board))]) == 0:
            self.player.winner = True
