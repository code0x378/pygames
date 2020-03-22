import os
import random

import pygame as pg

from pygame.locals import (
    RLEACCEL,
)

from spacerunner.settings import SCREEN_WIDTH, SCREEN_HEIGHT


class Asteroid(pg.sprite.Sprite):
    def __init__(self):
        super(Asteroid, self).__init__()
        self.type = random.randint(1, 2)
        if self.type == 1:
            self.surf = pg.image.load(os.path.join("res", "images", "meteorSmall.png")).convert()
        else:
            self.surf = pg.image.load(os.path.join("res", "images", "meteorLarge.png")).convert()
        self.surf.set_colorkey((0, 0, 0), RLEACCEL)
        self.rect = self.surf.get_rect(center=(random.randint(0, SCREEN_WIDTH),
                                               random.randint(10, 30)))
        self.speed = random.randint(3, 6)

    def update(self, level):
        if self.type == 1:
            self.rect.move_ip(-level, self.speed + level)
        else:
            self.rect.move_ip(level, self.speed + level)
        if self.rect.bottom > SCREEN_HEIGHT:
            self.kill()