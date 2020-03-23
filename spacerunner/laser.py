import os

import pygame as pg

from pygame.locals import (
    RLEACCEL,
)
class Laser(pg.sprite.Sprite):
    def __init__(self, rect):
        super(Laser, self).__init__()
        self.surf = pg.image.load(os.path.join("res", "images", "rocket_01.png")).convert()
        self.surf.set_colorkey((0, 0, 0), RLEACCEL)
        self.size = self.surf.get_size()
        self.surf = pg.transform.scale(self.surf, (int(self.size[0]*.1), int(self.size[1]*.1)))
        self.rect = self.surf.get_rect(center=(rect.left + 50, rect.top))
        self.speed = 5

    def update(self):
        self.rect.move_ip(0, -self.speed)
        if self.rect.top < 0:
            self.kill()