import random
import pygame

class Item(pygame.sprite.Sprite):
    def __init__(self, player, image):
        super().__init__()
        self.image = pygame.image.load(image)
        self.rect = self.image.get_rect()
        self.float_speed = random.choice([1, -1]) 
        self.player = player
        self.float_range = 5  
        self.float_counter = 0  

    def update(self):
        self.animation()
        pygame.sprite.spritecollide(self.player, self, True)
        
    def animation(self):
        '''Animation de flottement'''
        self.rect.y += self.float_speed
        self.float_counter += 1
        if abs(self.float_counter) >= self.float_range:
            self.float_speed *= -1
            self.float_counter *= -1