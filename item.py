import random
import pygame

from game_entity import GameEntity

class Item(GameEntity):
    def __init__(self, player, x, y, image):
        super().__init__()
        self.image = pygame.image.load(image)
        self.image = pygame.transform.scale(self.image,(32,32))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.float_speed = random.choice([1, -1]) 
        self.player = player
        self.float_range = 5  
        self.float_counter = 0  

    def update(self):
        self.animation()
        
    def animation(self):
        '''Animation de flottement'''
        self.rect.y += self.float_speed
        self.float_counter += 1
        if abs(self.float_counter) >= self.float_range:
            self.float_speed *= -1
            self.float_counter *= -1