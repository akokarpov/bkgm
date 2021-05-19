
import os
import pygame
from random import randint

class Dices:
    """Class of dices to return rand numbers and corresponding images."""

    def __init__(self, bkgm) -> None:
        self.screen = bkgm.screen
        self.settings = bkgm.settings
        self.rolls = []
        self.roll_p1 = None
        self.roll_p2 = None
        self.sprites = pygame.sprite.Group()
        self.sound = self.settings.dices_sound
    
    def draw(self):
        """Draws rolls images on screen."""
        self.sprites.draw(self.screen)

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
            sprite.image.set_colorkey(self.settings.WHITE)
            sprite.rect = sprite.image.get_rect()
            sprite.rect.x = self.settings.WIDTH - (self.settings.back_width / 2) + offset_x
            sprite.rect.y = self.settings.HEIGHT - (self.settings.back_height / 2) - 25
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
        if indexes == None:
            return
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
        self.kill()
        self.update()