import pygame
from pygame.locals import *
from pygame.math import Vector2 as vec
HEIGHT = 700
WIDTH = 1040
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        path = 'assets/player/'

        # Load enemy sprites
        self.sprites = {
            'idle_left': self.load_sprites(path + 'player_idle_4_left', 4),
            'idle_right': self.load_sprites(path + 'player_idle_4_right',4),
            'walk_left': self.load_sprites(path + 'player_walk_6_left',6),
            'walk_right':  self.load_sprites(path + 'player_walk_6_right',6)
        }

        # Set initial sprite state and image
        self.sprite_state = 'idle_right'
        self.surf = self.sprites['idle_right'][0]
        self.rect = self.surf.get_rect()

        # Set enemy position and size
        self.rect.x = WIDTH - 100
        self.rect.y = HEIGHT - 100
        self.width = 64
        self.height = 64

        # Set enemy movement variables
        self.vel = vec(2, 0)
        self.accel = vec(0.5, 0)
        self.fric = vec(-0.1, 0)
        self.gravity = vec(0, 0.5)

        # Set enemy animation variables
        self.current_sprite = 0
        self.sprite_counter = 0
        self.sprite_duration = 10

    def load_sprites(self, path, num_sprites):
        sprites = []
        for i in range(1, num_sprites + 1):
            img = pygame.image.load(f'{path}.png').convert_alpha()
            img = pygame.transform.scale(img, (64, 64))
            sprites.append(img)
        return sprites

    def update(self, platforms):
        self.sprite_counter += 1
        if self.sprite_counter >= self.sprite_duration:
            self.current_sprite += 1
            if self.current_sprite >= len(self.sprites[self.sprite_state]):
                self.current_sprite = 0
            self.image = self.sprites[self.sprite_state][self.current_sprite]
            self.sprite_counter = 0

        self.vel -= self.accel
        self.rect.x -= self.vel.x
        self.rect.y -= self.vel.y

        hits = pygame.sprite.spritecollide(self, platforms, False)
        if hits:
            if self.vel.y > 0:
                self.rect.y = hits[0].rect.top
                self.vel.y = 0
            elif self.vel.y < 0:
                self.rect.y = hits[0].rect.bottom
                self.vel.y = 0
            if self.vel.x > 0:
                self.rect.x = hits[0].rect.left - self.width
                self.vel.x = 0
                self.accel.x = -self.accel.x
            elif self.vel.x < 0:
                self.rect.x = hits[0].rect.right
                self.vel.x = 0
                self.accel.x = -self.accel.x

        self.vel.x += self.fric.x
        if abs(self.vel.x) < 0.1:
            self.vel.x = 0

        if self.vel.x > 0:
            self.sprite_state = 'walk_right'
        elif self.vel.x < 0:
            self.sprite_state = 'walk_left'
        else:
            self.sprite_state = 'idle_right' if self.accel.x > 0 else 'idle_left'
    def move(self):
        pass
