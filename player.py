import pygame
from pygame.locals import *
from pygame.math import Vector2
from const import ACC, FRIC, GRAVITY

class Player(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        super().__init__()
        path = 'assets/player/'
        self.double_jump = False
        self.game = game
        self.sprite_dict = {
            'idle_left': self.load_sprites(path + 'player_idle_4_left'),
            'idle_right': self.load_sprites(path + 'player_idle_4_right'),
            'walk_left': self.load_sprites(path + 'player_walk_6_left'),
            'walk_right': self.load_sprites(path + 'player_walk_6_right'),
            'jump_left': self.load_sprites(path + 'player_jump_8_left'),
            'jump_right': self.load_sprites(path + 'player_jump_8_right'),
            'sprint_left': self.load_sprites(path + 'player_run_6_left'),
            'sprint_right': self.load_sprites(path + 'player_run_6_right'),
            'attack_left': self.load_sprites(path + 'player_walk+attack_6_left'),
            'attack_right': self.load_sprites(path + 'player_walk+attack_6_right')
        }
        self.current_sprite = 0
        self.sprite_counter = 0
        self.sprite_state = 'idle_right'
        self.last_direction = 'right'

        self.image = self.sprite_dict['idle_right'][0]
        self.rect = self.image.get_rect()

        self.position = Vector2((x, y))
        self.vel = Vector2(0, 0)
        self.acc = Vector2(0, 0)
        self.jumping = False
        self.feet = pygame.Rect(0, self.rect.height - 12, self.rect.width * .5, 12)        
        self.hits = False

    def load_sprites(self, sprite_type, sprite_size=(32, 32)):
        img = pygame.image.load(f'{sprite_type}.png')
        sprites = []
        for i in range(img.get_width() // sprite_size[0]):
            for j in range(img.get_height() // sprite_size[1]):
                sprite = pygame.Surface(sprite_size)
                sprite.blit(img, (0, 0), (i * sprite_size[0], j * sprite_size[1], sprite_size[0], sprite_size[1]))
                sprite = pygame.transform.scale(sprite, (64, 64))
                sprite.set_colorkey((0, 0, 0))
                sprites.append(sprite)
        return sprites

    def move(self):
        
        self.acc = Vector2(0,0 if self.hits else GRAVITY)
        self.key_handler()
        self.acc.x += self.vel.x * FRIC
        self.vel += self.acc
        self.position += self.vel + 0.5 * self.acc
        self.rect.midbottom = self.position
       

    def attack(self):
        if self.last_direction == 'right':
            self.sprite_state = 'attack_right'
        else:
            self.sprite_state = 'attack_left'

    def jump(self):
        if self.double_jump:
            self.vel.y = -15
            self.double_jump = False
        else:
         
            self.vel.y = -15
            self.double_jump = True


    def touch_ground(self):
        self.rect.topleft = self.position
        self.feet.midbottom = self.rect.midbottom
        if self.vel.y > 0:
            if self.hits:
                self.vel.y = 0
                self.jumping = False
                self.double_jump = False

    def update(self):
        self.move()
        self.touch_ground()
        self.sprite_counter += 1
        if self.sprite_counter >= 10:
            self.current_sprite += 1
            if self.current_sprite >= len(self.get_sprites()):
                self.current_sprite = 0
            self.image = self.get_sprites()[self.current_sprite]
            self.sprite_counter = 0

        if self.sprite_state == 'attack_left' or self.sprite_state == 'attack_right':
            self.sprite_counter += 1
            if self.sprite_counter >= len(self.get_sprites()) * 3:
                self.sprite_state = 'idle_' + self.last_direction
                self.sprite_counter = 0
        pygame.draw.rect(self.game.screen, (255, 50, 0), self.feet, 2)

    def key_handler(self):
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[K_LEFT]:
            self.acc.x = -ACC
            if pressed_keys[K_LSHIFT] or pressed_keys[K_RSHIFT]:
                self.acc.x *= 1.5
                self.sprite_state = 'sprint_left'
            else:
                self.sprite_state = 'walk_left'
                self.last_direction = 'left'
        elif pressed_keys[K_RIGHT]:
            self.acc.x = ACC
            if pressed_keys[K_LSHIFT] or pressed_keys[K_RSHIFT]:
                self.acc.x *= 1.5
                self.sprite_state = 'sprint_right'
            else:
                self.sprite_state = 'walk_right'
                self.last_direction = 'right'
        elif pressed_keys[K_UP]:
            self.attack()
        else:
            if self.jumping:
                self.sprite_state = 'jump_' + self.last_direction
            else:
                self.sprite_state = 'idle_' + self.last_direction

    def get_sprites(self):
        return self.sprite_dict[self.sprite_state]
