import random

import pygame

from animation import Animation
from const import GRAVITY
from game_entity import GameEntity


class Enemy(GameEntity):
    def __init__(self, map, player, x, y):
        super().__init__()
        self.health = 1
        self.Maxhealth = 1
        self.Attack = 1
        self.velocity = 1
        self.distance = 200
        
        self.player = player
        self.states = ['walk','attack']
        self.name = 'enemy'
        self.state = 'walk_right'
        self.animation = Animation(self.name, self.states, 'walk_right', animation_speed=.6)
        self.animation.path = "../assets/enemy"
        
        self.map = map
        self.image = self.animation.image
        self.rect = self.image.get_rect()
        self.initial_pos = x
        self.rect.x = x
        self.rect.y = y
        self.obstacles = []
        self.vel = pygame.Vector2(0, 0)
        self.acc = pygame.Vector2(0,0)

        self.loot_amount = 10
        self.direction = 1
        self.on_ground = False

    def damage(self, amount):
        self.health -= amount
        if self.health <= 0:
            self.rect.x = 1000 + random.randint(0, 300)
            self.velocity = random.randint(1, 3)
            self.health = self.Maxhealth
            #self.game.add_score(self.loot_amount)

    def set_loot_amount(self, amount):
        self.loot_amount = amount


    def set_player(self, player):
        self.player = player

    def update(self):
        self.move()
        self.manage_world_contact(self.map.collisions)
        
    def move(self):
        self.acc = pygame.Vector2(0,GRAVITY)
        self.vel += self.acc
        self.image = self.animation.animate(self.state)
        
        if abs(self.player.rect.x - self.rect.x) <= self.distance:
            self.state = 'walk'
                # Mettre à jour la direction en fonction de la position du joueur
            if self.player.rect.x > self.rect.x:
                self.direction = 1
                self.state = 'walk_right'
            else:
                self.direction = -1
                self.state = 'walk_left'

                # Mettre à jour la position de l'ennemi en fonction de la direction et de la distance maximale
            self.rect.x += self.velocity * self.direction
            if self.direction == 1:
                if self.rect.x >= self.initial_pos + self.distance:
                    self.rect.x = self.initial_pos + self.distance
                    self.direction = -1
                    self.state = 'attack_right'
            else:
                if self.rect.x <= self.initial_pos:
                    self.rect.x = self.initial_pos
                    self.direction = 1
                    self.state = 'attack_left'
            """else:
                self.state = 'idle_left'"""
        else: 
            # Mettre à jour la position de l'ennemi en fonction de la direction et de la distance maximale
            self.rect.x += self.velocity * self.direction
            if self.direction == 1:
                if self.rect.x >= self.initial_pos + self.distance:
                    self.direction = -1
                    self.state = 'walk_left'
            else:
                if self.rect.x <= self.initial_pos:
                    self.direction = 1
                    self.state = 'walk_right'

    