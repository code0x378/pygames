import os
import random
import time
from datetime import datetime

import pygame
from pygame.locals import (
    RLEACCEL,
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    K_RETURN,
    K_SPACE,
    K_q,
    K_p,
    K_r,
    K_c,
    KEYDOWN,
    QUIT
)

SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768
SHOT_DELAY = .20
GAME_LENGTH = 8


class Game():
    def __init__(self):
        self.score = 0
        self.level = 1
        self.font = pygame.font.Font(os.path.join("res", "fonts", 'gameplayed.ttf'), 48)
        self.start_time = datetime.now()
        self.aliens_killed = 0
        self.active = False
        self.score = 0
        self.level = 1

    def draw_text(self, surf, text, size, x, y):
        self.font = pygame.font.Font(os.path.join("res", "fonts", 'gameplayed.ttf'), size)
        text_surface = self.font.render(text, True, (255, 255, 255))
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        surf.blit(text_surface, text_rect)

    def get_score(self):
        if self.active:
            self.score = ((datetime.now() - self.start_time).seconds * 10) + (self.aliens_killed * 100)
        return self.score

    def get_time(self):
        return GAME_LENGTH - (datetime.now() - self.start_time).seconds


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.surf = pygame.image.load(os.path.join("res", "images", "player.png")).convert()
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


class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super(Enemy, self).__init__()
        self.type = random.randint(1, 2)
        if self.type == 1:
            self.surf = pygame.image.load(os.path.join("res", "images", "meteorSmall.png")).convert()
        else:
            self.surf = pygame.image.load(os.path.join("res", "images", "meteorLarge.png")).convert()
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


class Laser(pygame.sprite.Sprite):
    def __init__(self, rect):
        super(Laser, self).__init__()
        self.surf = pygame.image.load(os.path.join("res", "images", "laserGreen.png")).convert()
        self.surf.set_colorkey((0, 0, 0), RLEACCEL)
        self.rect = self.surf.get_rect(center=(rect.left + 50, rect.top))
        self.speed = 5

    def update(self):
        self.rect.move_ip(0, -self.speed)
        if self.rect.top < 0:
            self.kill()


class Star(pygame.sprite.Sprite):
    def __init__(self, type):
        super(Star, self).__init__()
        if type == 1:
            self.tempImage = pygame.image.load(os.path.join("res", "images", "starSmall.png")).convert()
        elif type == 2:
            self.tempImage = pygame.image.load(os.path.join("res", "images", "speedLine.png")).convert()
        elif type == 3:
            self.tempImage = pygame.image.load(os.path.join("res", "images", "nebula.png")).convert()
        else:
            self.tempImage = pygame.image.load(os.path.join("res", "images", "starLarge.png")).convert()

        self.surf = self.tempImage.copy()
        alpha = random.randint(20, 120)
        self.surf.fill((255, 255, 255, alpha), None, pygame.BLEND_RGBA_MULT)
        self.rect = self.surf.get_rect(center=(random.randint(0, SCREEN_WIDTH),
                                               random.randint(10, 20)))
        self.speed = random.randint(1, 2)

    def update(self):
        self.rect.move_ip(0, self.speed)
        if self.rect.right < 0:
            self.kill()


def display_start(game, screen):
    menu = True
    while menu:
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE or event.key == K_q:
                    quit()
                elif event.key == K_RETURN or event.key == K_p:
                    menu = False
            elif event.type == QUIT:
                quit()

        screen.fill((50, 50, 50))
        game.draw_text(screen, f"Level: {game.level}", 24, SCREEN_WIDTH / 2, (SCREEN_HEIGHT / 2) - 300)
        game.draw_text(screen, "(P)lay", 48, SCREEN_WIDTH / 2, (SCREEN_HEIGHT / 2) - 80)
        game.draw_text(screen, "(Q)uit", 48, SCREEN_WIDTH / 2, (SCREEN_HEIGHT / 2) - 0)
        pygame.display.flip()


def display_level_complete(game, screen):
    menu = True
    while menu:
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE or event.key == K_q:
                    quit()
                elif event.key == K_RETURN or event.key == K_c:
                    menu = False
            elif event.type == QUIT:
                quit()

        screen.fill((50, 50, 50))
        game.draw_text(screen, f"Level: {game.level}", 24, SCREEN_WIDTH / 2, (SCREEN_HEIGHT / 2) - 300)
        game.draw_text(screen, f"Score: {game.get_score()}", 64, SCREEN_WIDTH / 2, (SCREEN_HEIGHT / 2) - 200)
        game.draw_text(screen, "(C)ontinue", 48, SCREEN_WIDTH / 2, (SCREEN_HEIGHT / 2) - 80)
        game.draw_text(screen, "(Q)uit", 48, SCREEN_WIDTH / 2, (SCREEN_HEIGHT / 2) - 0)
        pygame.display.flip()

def display_end(game, screen):
    menu = True
    while menu:
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE or event.key == K_q:
                    quit()
                elif event.key == K_RETURN or event.key == K_r:
                    menu = False
            elif event.type == QUIT:
                quit()

        screen.fill((50, 50, 50))
        game.draw_text(screen, f"Score: {game.get_score()}", 64, SCREEN_WIDTH / 2, (SCREEN_HEIGHT / 2) - 200)
        game.draw_text(screen, "(R)estart", 48, SCREEN_WIDTH / 2, (SCREEN_HEIGHT / 2) - 80)
        game.draw_text(screen, "(Q)uit", 48, SCREEN_WIDTH / 2, (SCREEN_HEIGHT / 2) - 0)
        pygame.display.flip()


def clear_callback(surf, rect):
    color = (94, 63, 107)
    surf.fill(color, rect)


def main():
    pygame.mixer.init()
    pygame.init()
    pygame.display.set_caption("SpaceRunner")

    fpsClock = pygame.time.Clock()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    ADDENEMY = pygame.USEREVENT + 1
    ADDSTAR = pygame.USEREVENT + 2
    pygame.time.set_timer(ADDENEMY, 150)
    pygame.time.set_timer(ADDSTAR, 750)
    last_shot = time.time()
    start_time = time.time()

    game = Game()
    player = Player()
    enemies = pygame.sprite.Group()
    stars = pygame.sprite.Group()
    lasers = pygame.sprite.Group()
    all_sprites = pygame.sprite.Group()
    all_sprites.add(player)
    all_sprites.add(stars)

    pygame.mixer.music.load(os.path.join("res", "sounds", "background.ogg"))
    pygame.mixer.music.play(loops=-1)
    pygame.mixer.music.set_volume(0.1)

    display_start(game, screen)

    running = True
    while running:

        game.active = True

        if (datetime.now() - game.start_time).seconds > GAME_LENGTH:
            game.active = False
            game.level = game.level + 1
            display_level_complete(game, screen)
            last_shot = time.time()
            start_time = time.time()
            # game.increase_level()
            for enemy in enemies:
                enemy.kill()
            for laser in lasers:
                laser.kill()

        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
                elif event.key == K_SPACE:
                    if time.time() - last_shot > SHOT_DELAY:
                        last_shot = time.time()
                        laser = Laser(player.rect)
                        lasers.add(laser)
                        all_sprites.add(laser)
            elif event.type == QUIT:
                running = False
            elif event.type == ADDENEMY:
                new_enemy = Enemy()
                enemies.add(new_enemy)
                all_sprites.add(new_enemy)
            elif event.type == ADDSTAR:
                new_star = Star(random.randint(1, 4))
                stars.add(new_star)
                all_sprites.add(new_star)

        pressed_keys = pygame.key.get_pressed()
        player.update(pressed_keys)
        enemies.update(game.level)
        stars.update()
        lasers.update()
        screen.fill((94, 63, 107))

        for entity in all_sprites:
            screen.blit(entity.surf, entity.rect)

        if pygame.sprite.spritecollideany(player, enemies):
            game.active = False
            display_end(game, screen)
            game = Game()
            game.active = True
            last_shot = time.time()
            player.kill()
            player = Player()

        for laser in lasers:
            hit = pygame.sprite.spritecollide(laser, enemies, dokill=True)
            if hit:
                game.aliens_killed = game.aliens_killed + 1
                laser.kill()

        game.draw_text(screen, f"Score: {game.get_score()}", 32, 120, 10)
        game.draw_text(screen, f"Time: {game.get_time()}", 32, SCREEN_WIDTH - 100, 10)
        pygame.display.flip()
        fpsClock.tick(60)

    pygame.mixer.music.stop()
    pygame.quit()


if __name__ == "__main__":
    main()
