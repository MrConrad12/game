import pygame
from pygame.locals import *
from pygame.math import Vector2
from pygame.sprite import AbstractGroup
from animation import Animation
from const import ACC, FRIC, GRAVITY
from projectile import Projectile

player_data = {
    'player1':{
        'lives': 3,
        'damage': 3,
        'speed': 2,
        'jump': 15,
        'aptitude': 'None'
    },
    'player2':{
        'lives': 3,
        'damage': 4,
        'jump': 15,
        'speed': 2,
        'aptitude': 'double_jump'
    },
    'player3':{
        'lives' : 3,
        'damage' : 2,
        'jump': 15,
        'speed': 3,
        'aptitude': 'sprint'
    },
    'player4':{
        'lives' : 4,
        'damage' : 3,
        'jump': 18,
        'speed': 1,
        'aptitude': 'swim'
    }
}

class Player(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        super().__init__()
        self.double_jump = False
        self.game = game
        
        # stat du joueur
        self.name = 'player1'
        self.current_player = player_data[self.name]
        self.lives = self.current_player['lives']
        self.damage = self.current_player['damage']
        self.speed = self.current_player['speed']
        self.jump_value = self.current_player['jump']
        self.apptitude = self.current_player['aptitude']
    
        # equipement du joueur
        self.all_projectiles = pygame.sprite.Group()

        
        # l'animation du joueur
        self.states = ['idle','walk','jump','run','walk+attack',]
        self.animation = Animation('player', self.states, 'idle_right')
        self.state = 'idle_right'
        self.last_direction = 'right'
        self.image = self.animation.image
        self.rect = self.image.get_rect()

        # mouvement du joueur
        self.position = Vector2((x, y))
        self.vel = Vector2(0, 0)
        self.acc = Vector2(0, 0)
        self.jumping = False
        self.feet = pygame.Rect(0, self.rect.height - 12, self.rect.width * .5, 12)        
        self.hits = False
        
        # interaction du joueur
        self.is_riding = False
        

    def update(self):
        """actualisation du joueur"""
        self.move()
        self.touch_ground()
        self.image = self.animation.animate(self.state)
        #pygame.draw.rect(self.game.screen, (255, 50, 0), self.feet, 2)
    
    def move(self):
        """gestion des deplacements"""
        self.acc = Vector2(0,-GRAVITY if self.hits else GRAVITY)
        self.key_handler()
        self.acc.x += self.vel.x * FRIC
        self.vel += self.acc
        self.position += self.vel + 0.5 * self.acc
        self.rect.midbottom = self.position   
        
    def jump(self):
        """gestion du saut et du double saut"""
        if not self.jumping:
            if self.double_jump:
                self.acc.y = -self.jump_value
                self.double_jump = False
            else:
                self.acc.y = -self.jump_value
                self.double_jump = True
            self.jumping = True
            
    def touch_ground(self):
        """verification s'il touche le sol"""
        self.rect.topleft = self.position
        self.feet.midbottom = self.rect.midbottom
        if self.vel.y > 0:
            if self.hits:
                self.vel.y = 0
                self.jumping = False
                self.double_jump = False
                
    def attack(self):
        """gestion des attack"""
        if self.last_direction == 'right':
            self.state = 'walk+attack_right'
        else:
            self.state = 'walk+attack_left'
            
    def launch_projectile(self):
        self.all_projectiles.add(Projectile(self))
        
    
                
    def ride(self, obj):
        """monter sur une monture"""
        if obj.is_readable:
            self.rect.x = obj.x + (obj.width - self.rect.width)
            self.rect.y = obj.y - self.rect.height * 4 / 5
            self.is_riding = True
            
    def come_down(self, obj):
        """descendre d'une monture"""
        self.is_riding = False

    def key_handler(self):
        """gestion des touches"""
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