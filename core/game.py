import os
import time

import pygame as pg


class Game():
    def __init__(self, game_length):
        self.score = 0
        self.level = 1
        self.font = pg.font.Font(os.path.join("res", "fonts", 'gameplayed.ttf'), 48)
        self.start_time = time.time()
        self.aliens_killed = 0
        self.active = False
        self.score = 0
        self.level = 1
        self.game_length = game_length

    def draw_text(self, surf, text, size, x, y):
        self.font = pg.font.Font(os.path.join("res", "fonts", 'gameplayed.ttf'), size)
        text_surface = self.font.render(text, True, (255, 255, 255))
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        surf.blit(text_surface, text_rect)

    def get_score(self):
        if self.active:
            self.score = (time.localtime(time.time() - self.start_time).tm_sec * 10) + (self.aliens_killed * 100)
        return self.score

    def get_time(self):
        return self.game_length - time.localtime(time.time() - self.start_time).tm_sec
