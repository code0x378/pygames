import csv
import os
import random
import time

import pygame as pg
from pygame.sprite import Sprite

from common.utils import draw_text

pg.mixer.init()
pg.init()
pg.display.set_caption("SpaceRunner")

SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768
SHOT_DELAY = .20
GAME_LENGTH = 8
LIVES = 2
FONT_SMALL = pg.font.Font(os.path.join("res", "fonts", 'gameplayed.ttf'), 18)
FONT_MEDIUM = pg.font.Font(os.path.join("res", "fonts", 'gameplayed.ttf'), 32)
FONT_LARGE = pg.font.Font(os.path.join("res", "fonts", 'gameplayed.ttf'), 48)
IMAGE_UI_BG = pg.image.load(os.path.join("res", "images", "background_ui.png"))


# ----------------------------------------------------------------------------
# Paddle
# ----------------------------------------------------------------------------

class Paddle(pg.sprite.Sprite):
    def __init__(self):
        super(Paddle, self).__init__()
        self.surf = pg.image.load(os.path.join("res", "images", "ship_01.png")).convert()
        self.surf.set_colorkey((0, 0, 0), pg.RLEACCEL)
        self.size = self.surf.get_size()
        self.surf = pg.transform.scale(self.surf, (int(self.size[0] * .1), int(self.size[1] * .1)))
        self.rect = self.get_rect()

    def reset(self):
        self.rect = self.get_rect()

    def update(self, pressed_keys):
        if pressed_keys[pg.K_UP]:
            self.rect.move_ip((0, -5))
        if pressed_keys[pg.K_DOWN]:
            self.rect.move_ip((0, 5))
        if pressed_keys[pg.K_LEFT]:
            self.rect.move_ip((-5, 0))
        if pressed_keys[pg.K_RIGHT]:
            self.rect.move_ip((5, 0))

        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT

    def get_rect(self):
        return self.surf.get_rect(center=((SCREEN_WIDTH - self.surf.get_width()) / 2, SCREEN_HEIGHT))


# ----------------------------------------------------------------------------
# Hud
# ----------------------------------------------------------------------------
#
# class Hud:
#
#     def __init__(self, game, lives_image):
#         self.game = game
#         self.lives_image = lives_image
#
#     def update(self):
#         draw_text(self.game.screen, f"Level: {self.game.level}", 120, 10, FONT_MEDIUM)
#         draw_text(self.game.screen, f"Score: {self.game.get_score()}", 120, 50, FONT_MEDIUM)
#         draw_text(self.game.screen, f"Time: {self.game.get_time()}", SCREEN_WIDTH - 100, 10, FONT_MEDIUM)
#         self.draw_lives(self.game.screen, self.lives_image)
#
#     def draw_lives(self, surf, image):
#         lives = self.game.lives
#         while lives > 0:
#             sprite = Sprite()
#             sprite.image = image
#             sprite.image.set_colorkey((0, 0, 0), pg.RLEACCEL)
#             size = sprite.image.get_size()
#             sprite.image = pg.transform.scale(sprite.image, (int(size[0] * .05), int(size[1] * .05)))
#             sprite.rect = image.get_rect()
#             sprite.rect.topleft = (SCREEN_WIDTH - (100 * lives), SCREEN_HEIGHT - 75)
#             surf.blit(sprite.image, sprite.rect)
#             lives -= 1


# ----------------------------------------------------------------------------
# 2HandedPong
# ----------------------------------------------------------------------------

class TwoHandedPong:
    def __init__(self):
        # self.display_splash()
        self.fpsClock = pg.time.Clock()
        self.screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.ADDENEMY = pg.USEREVENT + 1
        self.ADDSTAR = pg.USEREVENT + 2
        pg.time.set_timer(self.ADDENEMY, 150)
        pg.time.set_timer(self.ADDSTAR, 750)

        self.last_shot = time.time()
        self.score = 0
        self.level = 1
        self.lives = LIVES
        self.font = pg.font.Font(os.path.join("res", "fonts", 'gameplayed.ttf'), 48)
        self.start_time = time.time()
        self.aliens_killed = 0
        self.shots_fired = 0

        self.active = False
        self.game_length = GAME_LENGTH

        self.player = Paddle()
        self.enemies = pg.sprite.Group()
        self.stars = pg.sprite.Group()
        self.lasers = pg.sprite.Group()
        self.all_sprites = pg.sprite.Group()
        self.all_sprites.add(self.player)
        self.all_sprites.add(self.stars)

        pg.mixer.music.load(os.path.join("res", "sounds", "background.ogg"))
        pg.mixer.music.play(loops=-1)
        pg.mixer.music.set_volume(0.1)

    def reset(self):
        self.last_shot = time.time()
        self.score = 0
        self.level = 1
        self.lives = LIVES
        self.start_time = time.time()
        self.aliens_killed = 0
        self.active = False
        self.game_length = GAME_LENGTH
        self.shots_fired = 0

    def get_score(self):
        return self.score

    def get_time(self):
        return self.game_length - time.localtime(time.time() - self.start_time).tm_sec

    # ----------------------------------------------------------------------------
    # GUI
    # ----------------------------------------------------------------------------

    def display_splash(self):
        screen = pg.display.set_mode((500, 80), pg.NOFRAME)
        background = pg.Surface(screen.get_size())
        background.fill((2, 24, 244))
        screen.blit(background, (0, 0))
        # screen.blit(pg.font.Font('gameplayed.ttf', 72).render('Loading...', 1, (255, 255, 255)), (90, 10))
        pg.display.update()
        time.sleep(2)

    def display_help(self):
        menu = True
        while menu:
            for event in pg.event.get():
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE or event.key == pg.K_q or event.key == pg.K_b or event.key == pg.K_RETURN:
                        menu = False
                elif event.type == pg.QUIT:
                    quit()

            self.screen.blit(IMAGE_UI_BG, self.screen.get_rect())
            draw_text(self.screen, "Help", SCREEN_WIDTH / 2, (SCREEN_HEIGHT / 2) - 200, FONT_LARGE)
            draw_text(self.screen, "( Spacebar ) Shoot", SCREEN_WIDTH / 2, (SCREEN_HEIGHT / 2) - 80, FONT_MEDIUM)
            draw_text(self.screen, "( Arrows ) Move", SCREEN_WIDTH / 2, (SCREEN_HEIGHT / 2) - 0, FONT_MEDIUM)
            # draw_text(self.screen, "( Q ) uit", SCREEN_WIDTH / 2, (SCREEN_HEIGHT / 2) + 80)
            pg.display.flip()

    def display_start(self):
        menu = True
        while menu:
            for event in pg.event.get():
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_q:
                        quit()
                    elif event.key == event.key == pg.K_h:
                        self.display_help()
                    elif event.key == pg.K_RETURN or event.key == pg.K_p:
                        menu = False
                elif event.type == pg.QUIT:
                    quit()

            self.screen.blit(IMAGE_UI_BG, self.screen.get_rect())
            draw_text(self.screen, f"New Game", SCREEN_WIDTH / 2, (SCREEN_HEIGHT / 2) - 200, FONT_LARGE)
            draw_text(self.screen, "( P ) lay", SCREEN_WIDTH / 2, (SCREEN_HEIGHT / 2) - 80, FONT_MEDIUM)
            draw_text(self.screen, "( H ) elp", SCREEN_WIDTH / 2, (SCREEN_HEIGHT / 2) - 0, FONT_MEDIUM)
            draw_text(self.screen, "( Q ) uit", SCREEN_WIDTH / 2, (SCREEN_HEIGHT / 2) + 80, FONT_MEDIUM)
            pg.display.flip()

    def display_level_complete(self):
        menu = True
        while menu:
            for event in pg.event.get():
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        menu = False
                    elif event.key == pg.K_q:
                        quit()
                    elif event.key == pg.K_RETURN or event.key == pg.K_c:
                        menu = False
                elif event.type == pg.QUIT:
                    quit()

            self.screen.blit(IMAGE_UI_BG, self.screen.get_rect())
            draw_text(self.screen, f"Level: {self.level}", SCREEN_WIDTH / 2, (SCREEN_HEIGHT / 2) - 300, FONT_MEDIUM)
            draw_text(self.screen, f"Level Complete", SCREEN_WIDTH / 2, (SCREEN_HEIGHT / 2) - 200, FONT_LARGE)
            draw_text(self.screen, f"Score: {self.get_score()}", SCREEN_WIDTH / 2,
                      (SCREEN_HEIGHT / 2) - 100, FONT_MEDIUM)
            draw_text(self.screen, "( C ) ontinue", SCREEN_WIDTH / 2, (SCREEN_HEIGHT / 2) - 0, FONT_MEDIUM)
            pg.display.flip()

    def display_paused(self):
        menu = True
        while menu:
            for event in pg.event.get():
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        menu = False
                    elif event.key == pg.K_q:
                        quit()
                    elif event.key == pg.K_r:
                        self.active = False
                        self.reset()
                        menu = False
                    elif event.key == pg.K_RETURN or event.key == pg.K_c:
                        menu = False
                elif event.type == pg.QUIT:
                    quit()

            self.screen.blit(IMAGE_UI_BG, self.screen.get_rect())
            draw_text(self.screen, f"Score: {self.get_score()}", SCREEN_WIDTH / 2,
                      (SCREEN_HEIGHT / 2) - 280, FONT_MEDIUM)
            draw_text(self.screen, f"Game Paused", SCREEN_WIDTH / 2, (SCREEN_HEIGHT / 2) - 200, FONT_LARGE)
            draw_text(self.screen, "( C ) ontinue", SCREEN_WIDTH / 2, (SCREEN_HEIGHT / 2) - 80, FONT_MEDIUM)
            draw_text(self.screen, "( R ) estart", SCREEN_WIDTH / 2, (SCREEN_HEIGHT / 2) - 0, FONT_MEDIUM)
            draw_text(self.screen, "( Q ) uit", SCREEN_WIDTH / 2, (SCREEN_HEIGHT / 2) + 80,  FONT_MEDIUM)
            pg.display.flip()

    def display_end(self):
        menu = True
        while menu:
            for event in pg.event.get():
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        menu = False
                    elif event.key == pg.K_q:
                        quit()
                    elif event.key == pg.K_RETURN or event.key == pg.K_r:
                        menu = False
                elif event.type == pg.QUIT:
                    quit()

            self.screen.blit(IMAGE_UI_BG, self.screen.get_rect())
            draw_text(self.screen, f"Score: {self.get_score()}", SCREEN_WIDTH / 2,
                      (SCREEN_HEIGHT / 2) - 280, FONT_MEDIUM)
            draw_text(self.screen, f"Game Over", SCREEN_WIDTH / 2, (SCREEN_HEIGHT / 2) - 200, FONT_LARGE)
            draw_text(self.screen, "( R ) estart", SCREEN_WIDTH / 2, (SCREEN_HEIGHT / 2) - 0, FONT_MEDIUM)
            draw_text(self.screen, "( Q ) uit", SCREEN_WIDTH / 2, (SCREEN_HEIGHT / 2) + 80, FONT_MEDIUM )
            pg.display.flip()

    # ----------------------------------------------------------------------------
    # Event Loop
    # ----------------------------------------------------------------------------

    def run(self):
        background_image = pg.image.load(os.path.join("res", "images", f"background_0{random.randint(1, 4)}.png"))
        lives_image = pg.image.load(os.path.join("res", "images", "ship_01.png")).convert()

        # hud = Hud(self, lives_image)
        self.display_start()

        running = True
        while running:

            self.active = True


            for event in pg.event.get():
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        self.active = False
                        self.display_paused()
                    elif event.key == pg.K_SPACE:
                        if time.time() - self.last_shot > SHOT_DELAY:
                            self.last_shot = time.time()
                            laser = Laser(self.player.rect)
                            self.lasers.add(laser)
                            self.all_sprites.add(laser)
                            self.shots_fired = self.shots_fired + 1
                elif event.type == pg.QUIT:
                    running = False

            # hud.update()
            pg.display.flip()
            self.fpsClock.tick(60)

        pg.mixer.music.stop()
        pg.quit()


if __name__ == "__main__":
    twohandedpong = TwoHandedPong()
    twohandedpong.run()
