
import pygame
from settings import Settings


class Point(pygame.sprite.Sprite):
    """Points contain checkers and are interated by the Board class."""

    def __init__(self, number, *checkers):
        pygame.sprite.Sprite.__init__(self)
        self.settings = Settings()
        self.number = number
        if self.number == 0:
            self.stack = list(checkers[:15])
        elif self.number == 12:
            self.stack = list(checkers[15:])
        else:
            self.stack = []
        self.image = pygame.Surface((50, 300), pygame.SRCALPHA)
        self.rect = self.image.get_rect()
        self.rect.x = self.settings.point_coords[self.number][0]
        self.rect.y = self.settings.point_coords[self.number][1]
        self.align_checkers()

    def backlit(self, mode="off"):
        """Fills point will color if mode is set to 'on'."""
        if self.number < 12 or self.number == 25:
            points = [(0, 0), (50, 0), (25, 280)]
        else:
            points = [(0, 300), (50, 300), (25, 0)]
        if mode == "on":
            color = self.settings.GREEN
        else:
            color = self.settings.TRANSPARENT
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
                checker.rect.y = self.settings.HEIGHT - 72 - offset_y - step_y
            if checker in self.stack[:5]:
                offset_y = 0
            elif checker in self.stack[5:10]:
                offset_y = -275
            elif checker in self.stack[10:]:
                offset_y = -525
            step_y += 50
