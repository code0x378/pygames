import os

import pygame as pg
from pygame.locals import (
    RLEACCEL,
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
)

from core.game import Game

SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768
SHOT_DELAY = .20
GAME_LENGTH = 8

class Player(pg.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.surf = pg.image.load(os.path.join("res", "images", "player.png")).convert()
        self.surf.set_colorkey((0, 0, 0), RLEACCEL)
        self.rect = self.surf.get_rect(center=((SCREEN_WIDTH - self.surf.get_width()) / 2, SCREEN_HEIGHT))

    def update(self, pressed_keys):
        if pressed_keys[K_UP]:
            self.rect.move_ip((0, -5))
        if pressed_keys[K_DOWN]:
            self.rect.move_ip((0, 5))
        if pressed_keys[K_LEFT]:
            self.rect.move_ip((-5, 0))
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip((5, 0))

        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT