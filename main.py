

import os
import pygame
from random import randint, choice

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0, 100)
BEIGE = (244, 234, 195)
TRANSPARENT = (0, 0, 0, 0)
SCREEN_SIZE = WIDTH, HEIGHT = 1024, 768

pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption("Russian Long Backgammon")
back = pygame.image.load(os.path.join("data", "board.jpg")).convert()
back_width = back.get_size()[0]
back_height = back.get_size()[1]
font = pygame.font.Font('freesansbold.ttf', 40)


class Dices:
    """Class of dices to return rand numbers and corresponding images."""

    def __init__(self) -> None:
        self.rolls = []
        self.roll_p1 = None
        self.roll_p2 = None
        self.sprites = pygame.sprite.Group()
        self.sound = pygame.mixer.Sound(os.path.join("data", "dices.mp3"))

    def kill(self):
        """Removes played dices from board."""
        for sprite in self.sprites:
            sprite.kill()

    def update(self):
        """Places new dices sprites on board."""
        offset_x = 0
        for number in self.rolls:
            sprite = pygame.sprite.Sprite()
            sprite.image = pygame.image.load(
                os.path.join("data", f"dice{number}.png")).convert()
            sprite.image.set_colorkey(WHITE)
            sprite.rect = sprite.image.get_rect()
            sprite.rect.x = WIDTH - (back_width / 2) + offset_x
            sprite.rect.y = HEIGHT - (back_height / 2) - 25
            sprite.add(self.sprites)
            offset_x += 60

    def roll(self) -> list:
        """Returns a list of 2 or 4 rand numbers between 1-6."""
        self.rolls = []
        self.sound.play()
        for _ in range(2):
            number = randint(1, 6)
            if number in self.rolls:
                self.rolls = [number, number, number, number]
            else:
                self.rolls.append(number)
        self.kill()
        self.update()
        return self.rolls

    def kick_off(self, player1, player2) -> object:
        """Returns the player who starts the game first."""
        while self.roll_p1 == self.roll_p2:
            self.roll_p1 = sum(self.roll())
            self.roll_p2 = sum(self.roll())
        return player1 if self.roll_p1 > self.roll_p2 else player2

    def remove(self, indexes):
        """Discards rolls played by the player."""
        s_index = indexes[0]
        t_index = indexes[1]
        if len(self.rolls) == 1 or sum(self.rolls) == (t_index - s_index):
            self.rolls.clear()
        elif len(self.rolls) == 2:
            self.rolls.remove(t_index - s_index)
        else:
            if len(self.rolls) == 3:
                if sum(self.rolls) - (t_index - s_index) == self.rolls[0] * 2:
                    rolls_to_remove = 1
                else:
                    rolls_to_remove = 2
            else:
                if sum(self.rolls) - (t_index - s_index) == self.rolls[0]:
                    rolls_to_remove = 3
                elif sum(self.rolls) - (t_index - s_index) == self.rolls[0] * 2:
                    rolls_to_remove = 2
                else:
                    rolls_to_remove = 1
            for _ in range(rolls_to_remove):
                self.rolls.remove(self.rolls[0])


class Checker(pygame.sprite.Sprite):
    """Class of chechers: either white or black."""

    def __init__(self, color):
        pygame.sprite.Sprite.__init__(self)
        self.color = color
        if self.color == "w":
            file = "w_checker.png"
        else:
            file = "b_checker.png"
        self.image = pygame.image.load(os.path.join("data", file)).convert()
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0


class Point(pygame.sprite.Sprite):
    """Points contain checkers and are interated by the Board class."""

    def __init__(self, number):
        pygame.sprite.Sprite.__init__(self)
        self.stack = []
        self.number = number
        self.point_coords = {
            0: (835, 73),
            1: (777, 73),
            2: (717, 73),
            3: (657, 73),
            4: (597, 73),
            5: (537, 73),
            6: (437, 73),
            7: (377, 73),
            8: (317, 73),
            9: (257, 73),
            10: (197, 73),
            11: (137, 73),
            12: (137, 445),
            13: (197, 445),
            14: (257, 445),
            15: (317, 445),
            16: (377, 445),
            17: (437, 445),
            18: (537, 445),
            19: (597, 445),
            20: (657, 445),
            21: (717, 445),
            22: (777, 445),
            23: (835, 445),
            24: (925, 445),  # endpoint coords for white checkers
            25: (50, 73),  # endpoint coords for black checkers
        }
        self.image = pygame.Surface((50, 300), pygame.SRCALPHA)
        self.rect = self.image.get_rect()
        self.rect.x = self.point_coords[self.number][0]
        self.rect.y = self.point_coords[self.number][1]

    def backlit(self, mode="off"):
        """Fills point will color if mode is set to 'on'."""
        if self.number < 12 or self.number == 25:
            points = [(0, 0), (50, 0), (25, 280)]
        else:
            points = [(0, 300), (50, 300), (25, 0)]
        if mode == "on":
            color = GREEN
        else:
            color = TRANSPARENT
        pygame.draw.polygon(self.image, color, points)

    def align_checkers(self):
        """Aligns checkers in the point."""
        step_y = 0
        offset_y = 0
        for checker in self.stack:
            checker.rect.x = self.rect.x
            if self.number < 12 or self.number == 25:
                checker.rect.y = self.rect.y + offset_y + step_y
            else:
                checker.rect.y = HEIGHT - 72 - offset_y - step_y
            if checker in self.stack[:5]:
                offset_y = 0
            elif checker in self.stack[5:10]:
                offset_y = -275
            elif checker in self.stack[10:]:
                offset_y = -525
            step_y += 50


class Player:
    """Player class which represents a human or CPU."""

    def __init__(self, color: str) -> None:
        if color == "w":
            self.color = color
            self.opponent_color = "b"
        else:
            self.color = "b"
            self.opponent_color = "w"
        self.bear_off = False
        self.winner = False
        self.cpu = False

    def get_label(self):
        """Return a text label to blit on screen."""
        name = "CPU" if self.cpu else "Player"
        if self.bear_off:
            label = f"{name} '{self.color.upper()}' is bearing off..."
        else:
            label = f"{name} '{self.color.upper()}' is making a move..."
        if self.winner:
            label = f"{name} '{self.color.upper()}' has won the game."
        return font.render(label, True, BLACK)


class Board:
    """Engine of the game. The 2 board parts contain points.
    The board parts are rotated on each player change."""

    def __init__(self, *points) -> None:
        self.points_w = points[0:12]
        self.points_b = points[12:24]
        self.endpoint_w = points[24:25]
        self.endpoint_b = points[25:26]
        self.board = None
        self.player = None
        self.doubles = False
        self.doubles_forced = False
        self.head_played = False
        self.moves = None

    def get_moves(self, rolls, player):
        """Gets available moves."""
        self.moves = {}
        self.player = player
        self.rotate(self.player.color)

        if rolls == []:
            self.reset()
            return False

        if len(rolls) >= 3:
            rolls = [roll + roll * i for i, roll in enumerate(rolls)]
            self.doubles = True
        if len(rolls) == 2:
            rolls = [rolls[0], rolls[1], rolls[0] + rolls[1]]
        self.force_doubles(rolls)

        if self.count_points(s_index=0, t_index=18) == 0:
            self.player.bear_off = True
            self.rotate(self.player.color)

        for s_index, _ in enumerate(self.board):
            endpoint = len(self.board) - 1
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
                                if self.doubles_forced:
                                    s_index = 0
                                    t_index = rolls[0]
                                self.add_moves(s_index, t_index)
                        else:
                            if self.doubles and not self.doubles_forced:
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
        if self.moves == {}:
            self.reset()
            return False
        else:
            return True

    def reset(self):
        """Sets head_played and doubles flags to False values."""
        self.head_played = False
        self.doubles = False

    def force_doubles(self, rolls):
        """A second checker off the head is forced if roll on first move is > 2."""
        if len(self.board[0].stack) == 15 and rolls[0] >= 3 and self.doubles:
            self.doubles_forced = True
        if len(self.board[0].stack) == 13 and self.doubles_forced:
            self.doubles_forced = False
        if len(self.board[0].stack) == 14 and rolls[0] <= 2 and self.doubles:
            self.head_played = False

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
        """When bearing off sets out of index target indexes to endpoint."""
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

    def player_move(self, s_index, mouse_coords):
        """Moves checker from one point to another."""
        played_indexes = False
        for t_index in self.moves[s_index]:
            returned_t_index = t_index
            t_index = self.check_endpoint(t_index)
            if self.board[t_index].rect.collidepoint(mouse_coords):
                self.move_checker(s_index, t_index)
                self.board[t_index].align_checkers()
                if s_index == 0:
                    self.head_played = True
                played_indexes = (s_index, returned_t_index)
        self.lit_points(s_index, "off")
        self.board[s_index].align_checkers()
        return played_indexes

    def cpu_move(self):
        """Makes random moves if player is CPU."""
        s_index = choice(list(self.moves.keys()))
        t_index = choice(self.moves[s_index])
        if s_index == 0:
            self.head_played = True
        if self.player.bear_off:
            t_index = max(self.moves[s_index])
        self.move_checker(s_index, t_index)
        return s_index, t_index

    def check_winner(self):
        if self.player.bear_off and len(self.board[-1].stack) == 15:
            self.player.winner = True


dices = Dices()
player1 = Player("w")
player2 = Player("b")
white_checkers = [Checker("w") for _ in range(15)]
black_checkers = [Checker("b") for _ in range(15)]
points = [Point(index) for index in range(26)]
points[0].stack = white_checkers
points[0].align_checkers()
points[12].stack = black_checkers
points[12].align_checkers()
board = Board(*points)
checkers_sprites = pygame.sprite.Group(*white_checkers, *black_checkers)
points_sprites = pygame.sprite.Group(*points)

moving = False
game_over = False

while not game_over:

    for event in pygame.event.get():
        if event.type == pygame.QUIT or \
            event.type == pygame.KEYDOWN and \
                event.key == pygame.K_ESCAPE:
            game_over = True

    mouse_coords = pygame.mouse.get_pos()

    if board.moves and player.cpu:
        dices.remove(board.cpu_move())
        dices.kill()
        dices.update()

    if board.board == None:
        cpu = choice([player1, player2])
        cpu.cpu = True if cpu == player1 else cpu == player2
        player = dices.kick_off(player1, player2)
        board.get_moves(dices.roll(), player)

    if not board.get_moves(dices.rolls, player) and not player.winner:
        player = player2 if player == player1 else player1
        board.get_moves(dices.roll(), player)

    if event.type == pygame.MOUSEBUTTONDOWN and not moving:
        for s_index in board.moves.keys():
            if board.board[s_index].rect.collidepoint(mouse_coords):
                board.lit_points(s_index, "on")
                moving_checker = board.board[s_index].stack[-1]
                moving = True
                break

    if event.type == pygame.MOUSEMOTION and moving:
        moving_checker.rect.center = mouse_coords

    if event.type == pygame.MOUSEBUTTONUP and moving:
        moving = False
        move_indexes = board.player_move(s_index, mouse_coords)
        if move_indexes:
            dices.remove(move_indexes)
            dices.kill()
            dices.update()

    board.check_winner()

    screen.fill(BEIGE)
    screen.blit(back, ((WIDTH - back_width) / 2, HEIGHT - back_height))
    screen.blit(player.get_label(), ((WIDTH - back_width) / 2, 8))
    points_sprites.draw(screen)
    checkers_sprites.draw(screen)
    dices.sprites.draw(screen)
    pygame.display.flip()

    fps = 0.3 if player.cpu else 30
    clock.tick(fps)

    if player.winner:
        game_over = True
        pygame.time.wait(3000)

pygame.quit()
