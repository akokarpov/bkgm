
import pygame
from settings import Settings
from player import Player
from point import Point
from dices import Dices
from checker import Checker
from board import Board
from random import choice


class Backgammon:
    def __init__(self) -> None:
        pygame.init()
        pygame.display.set_caption("Russian Long Backgammon")
        self.settings = Settings()
        self.screen = pygame.display.set_mode(self.settings.SCREEN_SIZE)
        self.clock = pygame.time.Clock()
        self.player1 = Player("w", self.screen)
        self.player2 = Player("b", self.screen)
        self.checkers = [Checker(number) for number in range(30)]
        self.points = [Point(number, *self.checkers) for number in range(26)]
        self.dices = Dices(self.screen)
        self.board = Board(self.screen, *self.points)
        self.sprites_group = pygame.sprite.Group(*self.points, *self.checkers)
        self.moving = False
        self.game_over = False
        self.player = None

    def run(self):
        while not self.game_over:

            for event in pygame.event.get():
                if event.type == pygame.QUIT or \
                    event.type == pygame.KEYDOWN and \
                        event.key == pygame.K_ESCAPE:
                    self.game_over = True

            mouse_coords = pygame.mouse.get_pos()

            if self.board.moves and self.player.cpu:
                self.dices.remove(self.board.cpu_move())
                self.dices.kill()
                self.dices.update()

            if self.board.board == None:
                cpu = choice([self.player1, self.player2])
                cpu.cpu = True if cpu == self.player1 else cpu == self.player2
                self.player = self.dices.kick_off(self.player1, self.player2)
                self.board.get_moves(self.dices.roll(), self.player)

            if not self.board.get_moves(self.dices.rolls, self.player) and not self.player.winner:
                self.player = self.player2 if self.player == self.player1 else self.player1
                self.board.get_moves(self.dices.roll(), self.player)

            if event.type == pygame.MOUSEBUTTONDOWN and not self.moving:
                for s_index in self.board.moves.keys():
                    if self.board.board[s_index].rect.collidepoint(mouse_coords):
                        self.board.lit_points(s_index, "on")
                        moving_checker = self.board.board[s_index].stack[-1]
                        self.moving = True
                        break

            if event.type == pygame.MOUSEMOTION and self.moving:
                moving_checker.rect.center = mouse_coords

            if event.type == pygame.MOUSEBUTTONUP and self.moving:
                self.moving = False
                played_indexes = self.board.player_move(s_index, mouse_coords)
                if played_indexes:
                    self.dices.remove(played_indexes)
                    self.dices.kill()
                    self.dices.update()

            self.board.check_winner()

            self.screen.fill(self.settings.BEIGE)
            self.board.blitme()
            self.player.blitme()
            self.dices.draw()
            self.sprites_group.draw(self.screen)
            pygame.display.flip()

            fps = 0.5 if self.player.cpu else 30
            self.clock.tick(fps)

            if self.player.winner:
                self.game_over = True
                pygame.time.wait(3000)

        pygame.quit()


if __name__ == "__main__":
    bkgm = Backgammon()
    bkgm.run()
