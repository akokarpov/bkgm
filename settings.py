
import os
import pygame

class Settings:
    def __init__(self) -> None:
        self.dices_sound = pygame.mixer.Sound(os.path.join("data", "dices.mp3"))
        self.font = pygame.font.Font('freesansbold.ttf', 40)
        self.SCREEN_SIZE = self.WIDTH, self.HEIGHT = 1024, 768
        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)
        self.GREEN = (0, 255, 0, 100)
        self.BEIGE = (244, 234, 195)
        self.TRANSPARENT = (0, 0, 0, 0)
        self.back_width = 800
        self.back_height = 714
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