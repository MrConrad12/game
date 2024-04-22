import pygame
from pygame.locals import *
from pygame.math import Vector2
from pygame.sprite import AbstractGroup
from animation import Animation, cubic_bezier_ease_in
from const import ACC, FRIC, GRAVITY


class Player(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        super().__init__()
        self.double_jump = False
        self.game = game
        
        # about player's animation
        self.states = ['idle','walk','jump','run','walk+attack',]
        self.animation = Animation('player', self.states, 'idle_right')
        self.state = 'idle_right'
        self.last_direction = 'right'
        self.image = self.animation.image
        self.rect = self.image.get_rect()

        # about player's movement
        self.position = Vector2((x, y))
        self.vel = Vector2(0, 0)
        self.acc = Vector2(0, 0)
        self.jumping = False
        self.feet = pygame.Rect(0, self.rect.height - 12, self.rect.width * .5, 12)        
        self.hits = False

    def update(self):
        self.move()
        self.touch_ground()
        self.image = self.animation.animate(self.state)
        #pygame.draw.rect(self.game.screen, (255, 50, 0), self.feet, 2)
    
    def move(self):
        self.acc = Vector2(0,0 if self.hits else GRAVITY)
        self.key_handler()
        self.acc.x += self.vel.x * FRIC
        self.vel += self.acc
        self.position += self.vel + 0.5 * self.acc
        self.rect.midbottom = self.position   

    def attack(self):
        if self.last_direction == 'right':
            self.state = 'walk+attack_right'
        else:
            self.state = 'walk+attack_left'

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
                
    def key_handler(self):
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[K_LEFT]:
            self.acc.x = -ACC
            if pressed_keys[K_LSHIFT] or pressed_keys[K_RSHIFT]:
                self.acc.x *= 1.5
                self.state = 'run_left'
            else:
                self.state = 'walk_left'
                self.last_direction = 'left'
        elif pressed_keys[K_RIGHT]:
            self.acc.x = ACC
            if pressed_keys[K_LSHIFT] or pressed_keys[K_RSHIFT]:
                self.acc.x *= 1.5
                self.state = 'run_right'
            else:
                self.state = 'walk_right'
                self.last_direction = 'right'
        elif pressed_keys[K_UP]:
            self.attack()
        else:
            if self.jumping:
                self.state = 'jump_' + self.last_direction
            else:
                self.state = 'idle_' + self.last_direction
        if pressed_keys[K_SPACE]:
            self.state = 'jump_'+ self.last_direction
            self.jump()