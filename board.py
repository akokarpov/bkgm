
import os
import pygame
from random import choice


class Board:
    """Engine of the game. The 2 board parts contain points.
    The board parts are rotated on each player change."""

    def __init__(self, bkgm) -> None:
        self.screen = bkgm.screen
        self.settings = bkgm.settings
        self.background = pygame.image.load(
            os.path.join("data", "board.jpg")).convert()
        self.back_width = self.background.get_size()[0]
        self.back_height = self.background.get_size()[1]
        self.points_w = bkgm.points[0:12]
        self.points_b = bkgm.points[12:24]
        self.endpoint_w = bkgm.points[24:25]
        self.endpoint_b = bkgm.points[25:26]
        self.board = None
        self.player = None
        self.doubles = False
        self.head_forced = False
        self.head_played = False
        self.moves = None
        self.moving_checker = None
    
    def combine(self, rolls):

        if len(rolls) == 1:
            combination = rolls
        if len(rolls) == 2:
            combination = [rolls[0], rolls[1], rolls[0] + rolls[1]]
        if len(rolls) >= 3:
            self.doubles = True
            combination = [roll + roll * i for i, roll in enumerate(rolls)]
            if len(self.board[0].stack) >= 14:
                self.head_played = False
                if rolls[0] >= 3:
                    self.head_forced = True
                    combination = [rolls[0]]
            
        if self.head_forced and len(self.board[0].stack) == 13:
            self.head_forced = False
            self.head_played = True
            combination = [rolls[0], rolls[0] + rolls[0]]               
        
        return combination


    def get_moves(self, rolls, player):
        """Gets available moves."""

        if rolls == []:
            self.reset()
            return False

        self.moves = {}
        self.player = player
        self.rotate(self.player.color)
        
        rolls = self.combine(rolls)

        if self.count_points(s_index=0, t_index=18) == 0:
            self.player.bear_off = True
            self.rotate(self.player.color)

        for s_index, _ in enumerate(self.board):
            endpoint = len(self.board) - 1
            if self.head_forced:
                s_index = 0
            if s_index == 0 and self.head_played:
                continue
            if s_index == endpoint and player.bear_off:
                break
            for roll in rolls:
                t_index = s_index + roll
                if self.color_check(s_index):
                    if not self.player.bear_off:
                        if self.point_empty(t_index) or self.color_check(t_index):
                            if self.check_prime(s_index, t_index):
                                if rolls.index(roll) == 2 and self.moves == {}:
                                    break
                                self.add_moves(s_index, t_index)
                        else:
                            if self.doubles:
                                break
                    else:
                        if self.point_empty(t_index) or \
                                self.color_check(t_index) or \
                                t_index == endpoint or \
                                t_index > endpoint and not self.doubles and \
                                self.count_points(6, s_index) == 0 and rolls.index(roll) < 2 or \
                                t_index > endpoint and self.doubles and \
                                self.count_points(6, s_index) == 0 and rolls.index(roll) == 0 or \
                                self.doubles and roll == 3 and s_index == 6 and t_index == roll * 2 or \
                                self.doubles and roll == 2 and s_index == 6 and t_index == roll * 3 or \
                                self.doubles and roll == 2 and s_index == 8 and t_index == roll * 2 or \
                                self.doubles and roll == 1 and s_index <= 8 and t_index == roll * 4 or \
                                self.doubles and roll == 1 and s_index <= 9 and t_index == roll * 3 or \
                                self.doubles and roll == 1 and s_index <= 10 and t_index == roll * 2:
                            self.add_moves(s_index, t_index)
                            self.one_move_to_play()
        if self.check_winner():
            return True
        elif self.moves == {}:
            self.reset()
            return False
        else:
            return True

    def reset(self):
        """Sets head_played and doubles flags to False values."""
        self.head_played = False
        self.doubles = False
        self.head_forced = False

    def rotate(self, player_color):
        """Rotates the board according to player's turn."""
        if player_color == "w":
            if self.player.bear_off:
                self.board = self.points_b + self.endpoint_w
            else:
                self.board = self.points_w + self.points_b
        else:
            if self.player.bear_off:
                self.board = self.points_w + self.endpoint_b
            else:
                self.board = self.points_b + self.points_w

    def color_check(self, index):
        """Returns True if player's checker is at the point."""
        try:
            return self.board[index].stack[-1].color == self.player.color
        except IndexError:
            return False

    def point_empty(self, index):
        """Returns True if board point is empty."""
        try:
            return self.board[index].stack == []
        except IndexError:
            return False

    def count_points(self, s_index, t_index):
        """Returns sum of points occupied by a player between 2 indexes."""
        return sum([point.stack[-1].color.count(self.player.color)
                    for point in self.board[s_index:t_index] if point.stack != []])

    def add_moves(self, s_index, t_index):
        """Adds moves to a dictionary."""
        if s_index not in self.moves:
            self.moves[s_index] = [t_index]
        else:
            if t_index not in self.moves[s_index]:
                self.moves[s_index].append(t_index)

    def one_move_to_play(self):
        """Removes a possible move with lowest roll if player cannot play both rolls."""
        if len(self.moves) == 1 and len(next(iter(self.moves.values()))) == 2:
            next(iter(self.moves.values())).remove(
                min(next(iter(self.moves.values()))))

    def check_prime(self, s_index, t_index):
        """Returns True if player is allowed to build a prime."""
        prime = False
        is_prime_legal = True
        count_player = 0
        max_index_player = 0
        max_index_opponent = 0

        self.move_checker(s_index, t_index)
        self.rotate(self.player.opponent_color)

        for index, _ in enumerate(self.board):
            if self.color_check(index):
                count_player += 1
                if count_player > 5:
                    prime = True
                    max_index_player = index
            else:
                count_player = 0
            if not self.color_check(index) and not self.point_empty(index):
                max_index_opponent = index

        if prime and max_index_player > max_index_opponent:
            is_prime_legal = False

        self.rotate(self.player.color)
        self.move_checker(t_index, s_index)
        return is_prime_legal

    def check_endpoint(self, t_index):
        """Sets out of index beared off checkers to endpoint."""
        if t_index >= len(self.board):
            return len(self.board) - 1
        else:
            return t_index

    def move_checker(self, s_index, t_index):
        """Moves the checker from start to target point."""
        t_index = self.check_endpoint(t_index)
        moved_checker = self.board[s_index].stack.pop()
        self.board[t_index].stack.append(moved_checker)
        self.board[s_index].align_checkers()
        self.board[t_index].align_checkers()

    def lit_points(self, s_index, mode):
        """Shows possible move destinations."""
        for t_index in self.moves[s_index]:
            t_index = self.check_endpoint(t_index)
            self.board[t_index].backlit(mode)

    def take_checker(self, mouse_coords):
        """Returns True if player took a checker from the point."""
        for s_index in self.moves.keys():
            if self.board[s_index].rect.collidepoint(mouse_coords):
                self.moving_checker = self.board[s_index].stack[-1]
                self.lit_points(s_index, "on")
                self.s_index = s_index
                return True

    def player_move(self, mouse_coords):
        """Makes a move if player's move was legal."""
        played_indexes = None
        for t_index in self.moves[self.s_index]:
            returned_t_index = t_index
            t_index = self.check_endpoint(t_index)
            if self.board[t_index].rect.collidepoint(mouse_coords):
                if self.s_index == 0:
                    self.head_played = True
                played_indexes = self.s_index, returned_t_index
                self.move_checker(self.s_index, t_index)
                break
        self.lit_points(self.s_index, "off")
        self.board[t_index].align_checkers()
        self.board[self.s_index].align_checkers()
        return played_indexes

    def cpu_move(self):
        """Makes random moves if player is CPU."""
        if self.moves == {}:
            return None
        s_index = choice(list(self.moves.keys()))
        t_index = choice(self.moves[s_index])
        if s_index == 0:
            self.head_played = True
        if self.player.bear_off:
            t_index = max(self.moves[s_index])
        self.move_checker(s_index, t_index)
        return s_index, t_index

    def check_winner(self):
        """Return True if player beared off all checkers."""
        if self.player.bear_off and len(self.board[-1].stack) == 15:
            self.player.winner = True
            self.settings.game_over = True
            return True
    
    def blitme(self):
        """Draws background with board image on the screen."""
        self.screen.blit(self.background, (
            (self.settings.WIDTH - self.back_width) / 2,
            self.settings.HEIGHT - self.back_height)
        )
