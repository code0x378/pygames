import os
import random

import pygame as pg

from spacerunner.settings import SCREEN_WIDTH


class Star(pg.sprite.Sprite):
    def __init__(self, type):
        super(Star, self).__init__()
        if type == 1:
            self.tempImage = pg.image.load(os.path.join("res", "images", "starSmall.png")).convert()
        elif type == 2:
            self.tempImage = pg.image.load(os.path.join("res", "images", "speedLine.png")).convert()
        elif type == 3:
            self.tempImage = pg.image.load(os.path.join("res", "images", "nebula.png")).convert()
        else:
            self.tempImage = pg.image.load(os.path.join("res", "images", "starLarge.png")).convert()

        self.surf = self.tempImage.copy()
        alpha = random.randint(20, 120)
        self.surf.fill((255, 255, 255, alpha), None, pg.BLEND_RGBA_MULT)
        self.rect = self.surf.get_rect(center=(random.randint(0, SCREEN_WIDTH),
                                               random.randint(10, 20)))
        self.speed = random.randint(1, 2)

    def update(self):
        self.rect.move_ip(0, self.speed)
        if self.rect.right < 0:
            self.kill()
