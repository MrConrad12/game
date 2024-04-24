import pygame
from pygame.locals import *
from pygame.math import Vector2
from pygame.sprite import AbstractGroup
from animation import Animation
from const import ACC, FRIC, GRAVITY, PLAYER_DATA
from melee import Melee
from projectile import Projectile


class Player(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        super().__init__()
        self.double_jump = False
        self.game = game
        # stat du joueur
        self.name = 'player1'
        self.current_player = PLAYER_DATA[self.name]
        self.lives = self.current_player['lives']
        self.damage = self.current_player['damage']
        self.speed = self.current_player['speed']
        self.jump_value = self.current_player['jump']
        self.aptitude = self.current_player['aptitude']
    
        # etat du joueur
        self.current_lives = self.lives
        self.current_attacks = self.damage
        self.is_dead = True
        
        # equipement du joueur
        self.all_projectiles = pygame.sprite.Group()
        self.all_melee = pygame.sprite.Group()

        
        # l'animation du joueur
        self.states = ['idle','walk','jump','run','walk+attack',]
        self.animation = Animation('player', self.states, 'idle_right')
        self.state = 'idle_right'
        self.last_direction = 'right'
        self.image = self.animation.image
        self.rect = self.image.get_rect()

        # mouvement du joueur
        self.on_ground = False
        
        self.obstacles = []
        self.vel = Vector2(0, 0)
    
        self.rect.topleft = (x, y)
        
        self.acc = Vector2(0, 0)
        self.jumping = False
        
        
        # interaction du joueur
        self.is_riding = False

    def update(self):
        """actualisation du joueur"""
        self.handle_input()
        self.move()
        
    def move(self):
        """gestion des deplacements"""
        #self.acc = Vector2(0,-GRAVITY if self.hits else GRAVITY)

        self.acc.x += self.vel.x * FRIC
        self.vel += self.acc
        self.acc = Vector2(0,GRAVITY)
        self.acc.x += self.vel.x * FRIC
        self.vel += self.acc
        
        self.rect.x += self.vel.x + 0.5 * self.acc.x
        # Vérifier les collisions horizontales
        self.check_collisions(self.vel.x, 0)
         # Appliquer les déplacements verticaux
        self.rect.y += self.vel.y + 0.5 * self.acc.y
        # Vérifier les collisions verticales
        self.on_ground = False
        
        self.check_collisions(0, self.vel.y)
        self.image = self.animation.animate(self.state)
        
    def check_collisions(self, dx, dy):
        for obstacle in self.obstacles:
            if self.rect.colliderect(obstacle.rect):
                # Collision horizontale
                if dx > 0:
                    self.rect.right = obstacle.rect.left
                if dx < 0:
                    self.rect.left = obstacle.rect.right
                # Collision verticale
                if dy > 0:
                    self.rect.bottom = obstacle.rect.top
                    self.on_ground = True
                    self.vel.y = 0
                if dy < 0:
                    self.rect.top = obstacle.rect.bottom
                    self.vel.y = 0
            
    def jump(self):
        """gestion du saut et du double saut"""
        if not self.jumping : 
            self.vel.y = -self.jump_value
        """if self.double_jump:
            self.vel.y = -self.jump_value
            self.double_jump = False
        else:
            self.vel.y = -15
            self.double_jump = True"""
        self.jumping = False

    def attack(self):
        """gestion des attack"""
        if self.last_direction == 'right':
            self.state = 'walk+attack_right'
        else:
            self.state = 'walk+attack_left'
        self.launch_projectile()
            
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
        
    def get_damage(self):
        if(self.current_lives > 0):
            self.current_lives -= 1
        else:
            self.is_dead = True
    
    def get_live(self):
        if(self.current_lives <= self.lives):
            self.current_lives += 1
    
    def launch_projectile(self):
        if(self.current_attacks > 0):
            self.all_projectiles.add(Projectile(self))
            self.current_attacks -= 1
    
    def get_projectile(self):
        if(self.current_attacks<=self.attack):
            self.current_attacks += 1
            
    def launch_melee(self):
        self.all_melee.add(Melee(self))

    def handle_input(self):
        """gestion des touches"""
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[K_LEFT]:
            self.acc.x = -self.speed
            if pressed_keys[K_LSHIFT] or pressed_keys[K_RSHIFT]:
                self.acc.x *= 1.5
                self.state = 'run_left'
            else:
                self.state = 'walk_left'
                self.last_direction = 'left'
        elif pressed_keys[K_RIGHT]:
            self.acc.x = self.speed
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