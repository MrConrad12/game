import pygame
from pygame.locals import *
from pygame.math import Vector2
from pygame.sprite import AbstractGroup
from animation import Animation
from const import FRIC, GRAVITY, PLAYER_DATA
from game_entity import GameEntity
from melee import Melee
from projectile import Projectile

class Player(GameEntity):
    def __init__(self, map, x, y):
        super().__init__()
        self.double_jump = False
        self.map = map
        
        # stat du joueur
        self.name = 'player1'
        self.current_player = PLAYER_DATA[self.name]
        self.lives = self.current_player['lives']
        self.damage = self.current_player['damage']
        self.speed = self.current_player['speed']
        self.jump_value = self.current_player['jump']
        self.aptitude = self.current_player['aptitude']
    
        # stat du joueur
        self.current_lives = self.lives
        self.current_attacks = self.damage
        
        self.projectile_amount = 5
        self.projectile_delay = 40
        self.projectile_counter = 20
        
        self.damage_delay = 40
        self.damage_counter = 20
        self.launch_speed = 5
        
        self.regeneration_delay = 300
        self.regeneration_counter = 0
        
        self.is_dead = False
        self.is_hit = False
        
        # equipement du joueur
        self.all_projectiles = pygame.sprite.Group()
        self.all_melee = pygame.sprite.Group()

        # l'animation du joueur
        self.states = ['idle','walk','jump','run','walk+attack','hurt']
        self.animation_speed = 1
        self.animation = Animation('player', self.states, 'idle_right', animation_speed=self.animation_speed)
        self.state = 'idle_right'
        self.last_direction = 'right'
        self.image = self.animation.image
        self.rect = self.image.get_rect()

        # mouvement du joueur
        self.on_ground = False
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
        self.manage_world_contact(self.map.collisions)
        if self.detect_collision(self.map.void):
            self.is_dead = True
        for item in self.check_collision(self, self.map.items):
            if (self.projectile_amount<5):
                item.kill()
                self.get_projectile()
                
        if self.current_lives < self.lives:
            self.regeneration_counter += 1
            if self.regeneration_counter % self.regeneration_delay == 0:
                self.get_live()
                self.regeneration_counter = 0
        hits = pygame.sprite.spritecollide(self, self.map.enemies, False)
        
        for enemy in hits:
            # Si le joueur saute sur l'ennemi
            if self.vel.y > 0 and self.rect.bottom < enemy.rect.bottom and not enemy.is_dead:
                self.jump_bounce()
                enemy.is_dead = True
                
    def check_collision(self, sprite, group):
        return pygame.sprite.spritecollide(sprite, group, False, pygame.sprite.collide_mask)
    
    def move(self):
        """gestion des deplacements"""
        self.acc.x += self.vel.x * FRIC
        self.vel += self.acc
        self.acc = Vector2(0,GRAVITY)
        self.acc.x += self.vel.x * FRIC
        self.vel += self.acc
        self.image = self.animation.animate(self.state)
            
    def jump(self):
        """gestion du saut et du double saut"""
        self.state = 'jump_'+ self.last_direction
        self.jumping = True
        if self.on_ground:
            self.vel.y = -self.jump_value
            self.jumping = True
        elif self.double_jump and not self.jumping:
            self.vel.y = -self.jump_value
            self.double_jump = False
            self.jumping = True

    def jump_bounce(self):
        self.vel.y = -self.jump_value
        self.jumping = True
    def attack(self):
        """gestion des attack"""
        self.state = 'walk+attack_'+self.last_direction
                
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
        self.state = 'hurt_' + self.last_direction
        self.damage_counter +=1
        self.rect.x -= 1
        if self.damage_counter % self.damage_delay == 0:
            if self.current_lives > 0:
                self.current_lives -= 1
            else:
                self.is_dead = True
            self.damage_counter = 0
    
    def get_live(self):
        if(self.current_lives <= self.lives):
            self.current_lives += 1
    
    def launch_projectile(self):
        self.animation.animation_speed = 3.5
        self.projectile_counter += 1
        if self.projectile_counter % self.projectile_delay == 0:
            if(self.projectile_amount > 0):
                self.map.group.add(Projectile(self.map,self,self.last_direction))
                self.projectile_amount -= 1
            self.projectile_counter = 0
    
    def get_projectile(self):
        self.projectile_amount += 1
            
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
            self.launch_projectile()
        else:
            if self.jumping:
                self.state = 'jump_' + self.last_direction
            else:
                self.state = 'idle_' + self.last_direction
        if pressed_keys[K_SPACE]:
            self.jump()
        if self.is_hit:
            self.get_damage()
        self.animation.animation_speed = 1