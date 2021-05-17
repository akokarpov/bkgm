
import os
import pygame
from settings import Settings


class Checker(pygame.sprite.Sprite):
    """Class of chechers: either white or black."""

    def __init__(self, number):
        pygame.sprite.Sprite.__init__(self)
        self.settings = Settings()
        self.color = "w" if number < 15 else "b"
        file = "w_checker.png" if number < 15 else "b_checker.png"
        self.image = pygame.image.load(os.path.join("data", file)).convert()
        self.image.set_colorkey(self.settings.WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0
