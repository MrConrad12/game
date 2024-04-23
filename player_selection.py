import pygame
from animation import Animation
from const import *

class SelectablePlayer(pygame.sprite.Sprite):
    def __init__(self, image,x = SELECTABLE_PLAYER_POS_X, y = SELECTABLE_PLAYER_POS_Y) :
        super().__init__()
        self.states = ['idle']
        self.name = 'player'
        self.state = 'idle_left'
        self.animation = Animation(self.name, self.states, 'idle_left', animation_speed=.6,sprite_size=(192,192))
        self.animation.path = image
        self.image = self.animation.image
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
    def update(self):
        self.image = self.animation.animate(self.state)