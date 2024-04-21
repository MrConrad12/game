import pygame
from animation import Animation
from const import *


class SelectablePlayer(pygame.sprite.Sprite):
    def __init__(self) :
        super().__init__()
        self.states = ['idle']
        self.name = 'player'
        self.state = 'idle_left'
        self.animation = Animation(self.name, self.states, 'idle_left', animation_speed=.2,sprite_size=(192,192))
        self.image = self.animation.image
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH * 6/8 + 50
        self.rect.centery = HEIGHT / 3
    def update(self):
        self.image = self.animation.animate(self.state)