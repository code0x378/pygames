import os
import random
import time

import pygame as pg

from core.game import Game
from core.player import Player
from spacerunner.asteroid import Asteroid
from spacerunner.laser import Laser
from spacerunner.settings import SCREEN_WIDTH, SCREEN_HEIGHT, GAME_LENGTH, SHOT_DELAY
from spacerunner.star import Star


class SpaceRunner():
    def __init__(self):
        pg.mixer.init()
        pg.init()
        pg.display.set_caption("SpaceRunner")
        # self.display_splash()
        self.fpsClock = pg.time.Clock()
        self.screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.ADDENEMY = pg.USEREVENT + 1
        self.ADDSTAR = pg.USEREVENT + 2
        pg.time.set_timer(self.ADDENEMY, 150)
        pg.time.set_timer(self.ADDSTAR, 750)
        self.game = Game(GAME_LENGTH)
        self.last_shot = time.time()

        self.player = Player()
        self.enemies = pg.sprite.Group()
        self.stars = pg.sprite.Group()
        self.lasers = pg.sprite.Group()
        self.all_sprites = pg.sprite.Group()
        self.all_sprites.add(self.player)
        self.all_sprites.add(self.stars)

        pg.mixer.music.load(os.path.join("res", "sounds", "background.ogg"))
        pg.mixer.music.play(loops=-1)
        pg.mixer.music.set_volume(0.1)

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

            self.screen.fill((50, 50, 50))
            self.game.draw_text(self.screen, "Shoot: Spacebar", 24, SCREEN_WIDTH / 2, (SCREEN_HEIGHT / 2) - 200)
            self.game.draw_text(self.screen, "Move: Arrows", 24, SCREEN_WIDTH / 2, (SCREEN_HEIGHT / 2) - 150)
            self.game.draw_text(self.screen, "Quit: Escape", 24, SCREEN_WIDTH / 2, (SCREEN_HEIGHT / 2) - 100)
            self.game.draw_text(self.screen, "(B)ack", 48, SCREEN_WIDTH / 2, (SCREEN_HEIGHT / 2))
            pg.display.flip()

    def display_start(self):
        menu = True
        while menu:
            for event in pg.event.get():
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE or event.key == pg.K_q:
                        quit()
                    elif event.key == event.key == pg.K_h:
                        self.display_help()
                    elif event.key == pg.K_RETURN or event.key == pg.K_p:
                        menu = False
                elif event.type == pg.QUIT:
                    quit()

            self.screen.fill((50, 50, 50))
            self.game.draw_text(self.screen, f"Level: {self.game.level}", 24, SCREEN_WIDTH / 2,
                                (SCREEN_HEIGHT / 2) - 300)
            self.game.draw_text(self.screen, "(P)lay", 48, SCREEN_WIDTH / 2, (SCREEN_HEIGHT / 2) - 160)
            self.game.draw_text(self.screen, "(H)elp", 48, SCREEN_WIDTH / 2, (SCREEN_HEIGHT / 2) - 80)
            self.game.draw_text(self.screen, "(Q)uit", 48, SCREEN_WIDTH / 2, (SCREEN_HEIGHT / 2) - 0)
            pg.display.flip()

    def display_level_complete(self):
        menu = True
        while menu:
            for event in pg.event.get():
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE or event.key == pg.K_q:
                        quit()
                    elif event.key == pg.K_RETURN or event.key == pg.K_c:
                        menu = False
                elif event.type == pg.QUIT:
                    quit()

            self.screen.fill((50, 50, 50))
            self.game.draw_text(self.screen, f"Level: {self.game.level}", 24, SCREEN_WIDTH / 2,
                                (SCREEN_HEIGHT / 2) - 300)
            self.game.draw_text(self.screen, f"Score: {self.game.get_score()}", 64, SCREEN_WIDTH / 2,
                                (SCREEN_HEIGHT / 2) - 200)
            self.game.draw_text(self.screen, "(C)ontinue", 48, SCREEN_WIDTH / 2, (SCREEN_HEIGHT / 2) - 80)
            self.game.draw_text(self.screen, "(Q)uit", 48, SCREEN_WIDTH / 2, (SCREEN_HEIGHT / 2) - 0)
            pg.display.flip()

    def display_end(self):
        menu = True
        while menu:
            for event in pg.event.get():
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE or event.key == pg.K_q:
                        quit()
                    elif event.key == pg.K_RETURN or event.key == pg.K_r:
                        menu = False
                elif event.type == pg.QUIT:
                    quit()

            self.screen.fill((50, 50, 50))
            self.game.draw_text(self.screen, f"Score: {self.game.get_score()}", 64, SCREEN_WIDTH / 2,
                                (SCREEN_HEIGHT / 2) - 200)
            self.game.draw_text(self.screen, "(R)estart", 48, SCREEN_WIDTH / 2, (SCREEN_HEIGHT / 2) - 80)
            self.game.draw_text(self.screen, "(Q)uit", 48, SCREEN_WIDTH / 2, (SCREEN_HEIGHT / 2) - 0)
            pg.display.flip()

    def clear_callback(surf, rect):
        color = (94, 63, 107)
        surf.fill(color, rect)

    def run(self):
        self.display_start()
        self.game = Game(GAME_LENGTH)

        running = True
        while running:

            self.game.active = True

            if time.time() - self.game.start_time > GAME_LENGTH:
                self.game.active = False
                self.game.level = self.game.level + 1
                self.display_level_complete()
                self.last_shot = time.time()
                self.game.start_time = time.time()
                # game.increase_level()
                self.game.active = True
                for enemy in self.enemies:
                    enemy.kill()
                for laser in self.lasers:
                    laser.kill()

            for event in pg.event.get():
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        running = False
                    elif event.key == pg.K_SPACE:
                        if time.time() - self.last_shot > SHOT_DELAY:
                            self.last_shot = time.time()
                            laser = Laser(self.player.rect)
                            self.lasers.add(laser)
                            self.all_sprites.add(laser)
                elif event.type == pg.QUIT:
                    running = False
                elif event.type == self.ADDENEMY:
                    new_enemy = Asteroid()
                    self.enemies.add(new_enemy)
                    self.all_sprites.add(new_enemy)
                elif event.type == self.ADDSTAR:
                    new_star = Star(random.randint(1, 4))
                    self.stars.add(new_star)
                    self.all_sprites.add(new_star)

            pressed_keys = pg.key.get_pressed()
            self.player.update(pressed_keys)
            self.enemies.update(self.game.level)
            self.stars.update()
            self.lasers.update()
            self.screen.fill((94, 63, 107))

            for entity in self.all_sprites:
                self.screen.blit(entity.surf, entity.rect)

            if pg.sprite.spritecollideany(self.player, self.enemies):
                self.game.active = False
                self.display_end()
                self.last_shot = time.time()
                self.game.start_time = time.time()
                self.game = Game(GAME_LENGTH)
                self.game.active = True
                for enemy in self.enemies:
                    enemy.kill()
                for laser in self.lasers:
                    laser.kill()

            for laser in self.lasers:
                hit = pg.sprite.spritecollide(laser, self.enemies, dokill=True)
                if hit:
                    self.game.aliens_killed = self.game.aliens_killed + 1
                    laser.kill()

            self.game.draw_text(self.screen, f"Score: {self.game.get_score()}", 32, 120, 10)
            self.game.draw_text(self.screen, f"Time: {self.game.get_time()}", 32, SCREEN_WIDTH - 100, 10)
            pg.display.flip()
            self.fpsClock.tick(60)

        pg.mixer.music.stop()
        pg.quit()


if __name__ == "__main__":
    spacerunner = SpaceRunner()
    spacerunner.run()
