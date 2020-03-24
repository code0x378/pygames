import os
import random
import time

import pygame as pg
from pygame.sprite import Sprite

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
IMAGE_UI_BG = pg.image.load(os.path.join("res", "images", "background_UI.png"))


# ----------------------------------------------------------------------------
# Utils
# ----------------------------------------------------------------------------

def draw_text(surf, text, x, y, font=FONT_MEDIUM):
    text_surface = font.render(text, True, (255, 255, 255))
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)


# ----------------------------------------------------------------------------
# Player
# ----------------------------------------------------------------------------

class Player(pg.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.surf = pg.image.load(os.path.join("res", "images", "ship_01.png")).convert()
        self.surf.set_colorkey((0, 0, 0), pg.RLEACCEL)
        self.size = self.surf.get_size()
        self.surf = pg.transform.scale(self.surf, (int(self.size[0] * .1), int(self.size[1] * .1)))
        self.reset()

    def reset(self):
        self.rect = self.surf.get_rect(center=((SCREEN_WIDTH - self.surf.get_width()) / 2, SCREEN_HEIGHT))

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


# ----------------------------------------------------------------------------
# Laser
# ----------------------------------------------------------------------------

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
        alpha = random.randint(20, 75)
        self.surf.fill((255, 255, 255, alpha), None, pg.BLEND_RGBA_MULT)
        self.rect = self.surf.get_rect(center=(random.randint(0, SCREEN_WIDTH),
                                               random.randint(10, 20)))
        self.speed = random.randint(1, 2)

    def update(self):
        self.rect.move_ip(0, self.speed)
        if self.rect.right < 0:
            self.kill()


# ----------------------------------------------------------------------------
# Laser
# ----------------------------------------------------------------------------

class Laser(pg.sprite.Sprite):
    def __init__(self, rect):
        super(Laser, self).__init__()
        self.surf = pg.image.load(os.path.join("res", "images", "rocket_01.png")).convert()
        self.surf.set_colorkey((0, 0, 0), pg.RLEACCEL)
        self.size = self.surf.get_size()
        self.surf = pg.transform.scale(self.surf, (int(self.size[0] * .1), int(self.size[1] * .1)))
        self.rect = self.surf.get_rect(center=(rect.left + 50, rect.top))
        self.speed = 5

    def update(self):
        self.rect.move_ip(0, -self.speed)
        if self.rect.top < 0:
            self.kill()


# ----------------------------------------------------------------------------
# Asteroid
# ----------------------------------------------------------------------------

class Asteroid(pg.sprite.Sprite):
    def __init__(self):
        super(Asteroid, self).__init__()
        self.type = random.randint(1, 2)
        self.angle = random.randint(0, 359)
        self.start_time = time.time()
        if self.type == 1:
            self.surf = pg.image.load(os.path.join("res", "images", "asteroid_09.png")).convert()
            self.size = self.surf.get_size()
            self.surf = pg.transform.scale(self.surf, (int(self.size[0] * .25), int(self.size[1] * .25)))
        else:
            self.surf = pg.image.load(os.path.join("res", "images", "asteroid_05.png")).convert()
            self.size = self.surf.get_size()
            self.surf = pg.transform.scale(self.surf, (int(self.size[0] * .15), int(self.size[1] * .15)))
        self.surf.set_colorkey((0, 0, 0), pg.RLEACCEL)
        self.rect = self.surf.get_rect(center=(random.randint(0, SCREEN_WIDTH),
                                               random.randint(10, 30)))
        self.speed_x = random.randint(3, 6)
        self.speed_y = random.randint(-2, 2)
        self.surf = pg.transform.rotate(self.surf, self.angle)

    def update(self, level):
        self.rect.move_ip(self.speed_y, self.speed_x + level)
        if self.rect.bottom > SCREEN_HEIGHT:
            self.kill()


# ----------------------------------------------------------------------------
# Hud
# ----------------------------------------------------------------------------

class Hud:

    def __init__(self, game, lives_image):
        self.game = game
        self.lives_image = lives_image

    def update(self):
        draw_text(self.game.screen, f"Level: {self.game.level}", 120, 10)
        draw_text(self.game.screen, f"Score: {self.game.get_score()}", 120, 50)
        draw_text(self.game.screen, f"Time: {self.game.get_time()}", SCREEN_WIDTH - 100, 10)
        self.draw_lives(self.game.screen, self.lives_image)

    def draw_lives(self, surf, image):
        lives = self.game.lives
        while lives > 0:
            sprite = Sprite()
            sprite.image = image
            sprite.image.set_colorkey((0, 0, 0), pg.RLEACCEL)
            size = sprite.image.get_size()
            sprite.image = pg.transform.scale(sprite.image, (int(size[0] * .05), int(size[1] * .05)))
            sprite.rect = image.get_rect()
            sprite.rect.topleft = (SCREEN_WIDTH - (100 * lives), SCREEN_HEIGHT - 75)
            surf.blit(sprite.image, sprite.rect)
            lives -= 1


# ----------------------------------------------------------------------------
# SpaceRunner
# ----------------------------------------------------------------------------

class SpaceRunner:
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
        if self.active:
            self.score = (time.localtime(time.time() - self.start_time).tm_sec * 10) + (self.aliens_killed * 100) - (
                    self.shots_fired * 10)
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
            draw_text(self.screen, "( Spacebar ) Shoot", SCREEN_WIDTH / 2, (SCREEN_HEIGHT / 2) - 80)
            draw_text(self.screen, "( Arrows ) Move", SCREEN_WIDTH / 2, (SCREEN_HEIGHT / 2) - 0)
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
            draw_text(self.screen, "( P ) lay", SCREEN_WIDTH / 2, (SCREEN_HEIGHT / 2) - 80)
            draw_text(self.screen, "( H ) elp", SCREEN_WIDTH / 2, (SCREEN_HEIGHT / 2) - 0)
            draw_text(self.screen, "( Q ) uit", SCREEN_WIDTH / 2, (SCREEN_HEIGHT / 2) + 80)
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
            draw_text(self.screen, f"Level: {self.level}", SCREEN_WIDTH / 2, (SCREEN_HEIGHT / 2) - 300)
            draw_text(self.screen, f"Level Complete", SCREEN_WIDTH / 2, (SCREEN_HEIGHT / 2) - 200, FONT_LARGE)
            draw_text(self.screen, f"Score: {self.get_score()}", SCREEN_WIDTH / 2,
                      (SCREEN_HEIGHT / 2) - 100)
            draw_text(self.screen, "( C ) ontinue", SCREEN_WIDTH / 2, (SCREEN_HEIGHT / 2) - 0)
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
                      (SCREEN_HEIGHT / 2) - 280)
            draw_text(self.screen, f"Game Paused", SCREEN_WIDTH / 2, (SCREEN_HEIGHT / 2) - 200, FONT_LARGE)
            draw_text(self.screen, "( C ) ontinue", SCREEN_WIDTH / 2, (SCREEN_HEIGHT / 2) - 80)
            draw_text(self.screen, "( R ) estart", SCREEN_WIDTH / 2, (SCREEN_HEIGHT / 2) - 0)
            draw_text(self.screen, "( Q ) uit", SCREEN_WIDTH / 2, (SCREEN_HEIGHT / 2) + 80, )
            pg.display.flip()

    def display_end(self):
        menu = True
        while menu:
            for event in pg.event.get():
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE or event.key == pg.K_c:
                        menu = False
                    elif event.key == pg.K_q:
                        quit()
                    elif event.key == pg.K_RETURN or event.key == pg.K_r:
                        menu = False
                elif event.type == pg.QUIT:
                    quit()

            self.screen.blit(IMAGE_UI_BG, self.screen.get_rect())
            draw_text(self.screen, f"Score: {self.get_score()}", SCREEN_WIDTH / 2,
                      (SCREEN_HEIGHT / 2) - 280)
            draw_text(self.screen, f"Game Over", SCREEN_WIDTH / 2, (SCREEN_HEIGHT / 2) - 200, FONT_LARGE)
            draw_text(self.screen, "( C ) ontinue", SCREEN_WIDTH / 2, (SCREEN_HEIGHT / 2) - 80)
            draw_text(self.screen, "( R ) estart", SCREEN_WIDTH / 2, (SCREEN_HEIGHT / 2) - 0)
            draw_text(self.screen, "( Q ) uit", SCREEN_WIDTH / 2, (SCREEN_HEIGHT / 2) + 80, )
            pg.display.flip()

    # ----------------------------------------------------------------------------
    # Event Loop
    # ----------------------------------------------------------------------------

    def run(self):
        background_image = pg.image.load(os.path.join("res", "images", f"background_0{random.randint(1, 4)}.png"))
        lives_image = pg.image.load(os.path.join("res", "images", "ship_01.png")).convert()

        hud = Hud(self, lives_image)
        self.display_start()

        running = True
        while running:

            self.active = True

            if time.time() - self.start_time > GAME_LENGTH:
                self.active = False
                self.level = self.level + 1
                self.display_level_complete()
                self.last_shot = time.time()
                self.start_time = time.time()
                self.active = True
                for enemy in self.enemies:
                    enemy.kill()
                for laser in self.lasers:
                    laser.kill()

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
            self.enemies.update(self.level)
            self.stars.update()
            self.lasers.update()
            self.screen.fill((94, 63, 107))
            self.screen.blit(background_image, self.screen.get_rect())

            for entity in self.all_sprites:
                self.screen.blit(entity.surf, entity.rect)

            if pg.sprite.spritecollideany(self.player, self.enemies):
                if self.lives == 0:
                    self.active = False
                    self.display_end()
                    self.reset()
                elif self.lives > 0:
                    self.lives -= 1

                self.player.reset()
                for enemy in self.enemies:
                    enemy.kill()
                for laser in self.lasers:
                    laser.kill()
                self.last_shot = time.time()
                self.start_time = time.time()
                self.active = True

            for laser in self.lasers:
                hit = pg.sprite.spritecollide(laser, self.enemies, dokill=True)
                if hit:
                    self.aliens_killed = self.aliens_killed + 1
                    laser.kill()

            hud.update()
            pg.display.flip()
            self.fpsClock.tick(60)

        pg.mixer.music.stop()
        pg.quit()


if __name__ == "__main__":
    spacerunner = SpaceRunner()
    spacerunner.run()
