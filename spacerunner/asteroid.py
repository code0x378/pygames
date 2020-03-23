import os
import random
import time

import pygame as pg

from pygame.locals import (
    RLEACCEL,
)

from spacerunner.settings import SCREEN_WIDTH, SCREEN_HEIGHT


class Asteroid(pg.sprite.Sprite):
    def __init__(self):
        super(Asteroid, self).__init__()
        self.type = random.randint(1, 2)
        self.angle = 0
        self.start_time = time.time()
        if self.type == 1:
            self.surf = pg.image.load(os.path.join("res", "images", "asteroid_03.png")).convert()
            self.size = self.surf.get_size()
            self.surf = pg.transform.scale(self.surf, (int(self.size[0]*.2), int(self.size[1]*.2)))
        else:
            self.surf = pg.image.load(os.path.join("res", "images", "asteroid_05.png")).convert()
            self.size = self.surf.get_size()
            self.surf = pg.transform.scale(self.surf, (int(self.size[0]*.15), int(self.size[1]*.15)))
        self.surf.set_colorkey((0, 0, 0), RLEACCEL)
        self.rect = self.surf.get_rect(center=(random.randint(0, SCREEN_WIDTH),
                                               random.randint(10, 30)))
        self.speed_x = random.randint(3, 6)
        self.speed_y = random.randint(-2, 2)
        self.surf = pg.transform.rotate(self.surf , self.angle)

    def update(self, level):
        # increase angle
        if time.time() - self.start_time > .2:
            self.start_time = time.time()
            self.angle += 1
            self.angle %= 360
            self.surf = pg.transform.rotate(self.surf , self.angle)
        self.rect.move_ip(self.speed_y , self.speed_x + level)
        if self.rect.bottom > SCREEN_HEIGHT:
            self.kill()