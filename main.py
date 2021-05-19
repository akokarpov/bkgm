
import pygame
from settings import Settings
from player import Player
from point import Point
from dices import Dices
from checker import Checker
from board import Board
from random import choice


class Backgammon:
    """Main game class with key attributes."""

    def __init__(self) -> None:
        pygame.init()
        pygame.display.set_caption("Russian Long Backgammon")
        self.settings = Settings()
        self.screen = pygame.display.set_mode(self.settings.SCREEN_SIZE)
        self.clock = pygame.time.Clock()
        self.dices = Dices(self)
        self.player1 = Player("w", self)
        self.player2 = Player("b", self)
        self.checkers = [Checker(num, self) for num in range(30)]
        self.points = [Point(num, self) for num in range(26)]
        self.board = Board(self)
        self.sprites_group = pygame.sprite.Group(*self.points, *self.checkers)
        self.game_reset()

    def game_reset(self):
        cpu = choice([self.player1, self.player2])
        cpu.cpu = True if cpu == self.player1 else cpu == self.player2
        self.player = self.dices.kick_off(self.player1, self.player2)
        self.board.get_moves(self.dices.roll(), self.player)

    def check_events(self):
        """Checks events in events loop."""
        for event in pygame.event.get():
            mouse = pygame.mouse.get_pos()
            if event.type == pygame.QUIT or \
                event.type == pygame.KEYDOWN and \
                    event.key == pygame.K_ESCAPE:
                self.settings.game_over = True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.board.take_checker(mouse):
                    self.settings.is_checker_moving = True
            elif event.type == pygame.MOUSEBUTTONUP:
                if self.settings.is_checker_moving:
                    self.dices.remove(self.board.player_move(mouse))
                    self.settings.is_checker_moving = False

    def update_screen(self):
        """Draws images and sprites on screen."""
        self.screen.fill(self.settings.BEIGE)
        self.board.blitme()
        self.player.blitme()
        self.dices.draw()
        if self.settings.is_checker_moving:
            self.board.moving_checker.set_pos(*pygame.mouse.get_pos())
        self.sprites_group.draw(self.screen)
        pygame.display.flip()
        fps = 0.5 if self.player.cpu else 30
        self.clock.tick(fps)

    def run(self):
        """Executes the main game loop."""
        while not self.settings.game_over:

            self.check_events()

            if not self.board.get_moves(self.dices.rolls, self.player):
                self.player = self.player2 if self.player == self.player1 else self.player1
                self.board.get_moves(self.dices.roll(), self.player)
            
            if self.player.cpu:
                self.dices.remove(self.board.cpu_move())

            self.update_screen()

        pygame.time.wait(3000)
        pygame.quit()


if __name__ == "__main__":
    bkgm = Backgammon()
    bkgm.run()
