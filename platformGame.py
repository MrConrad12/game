import pygame
from pygame.locals import *
HEIGHT = 700
WIDTH = 1040
ACC = 0.5
FRIC = -0.12
FPS = 60

class Platform(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((WIDTH, 20))
        self.image.fill((255,0,0))
        self.rect = self.image.get_rect(center = (WIDTH/2, HEIGHT - 10))
    def move(self):
        pass
class Block(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill((255, 0, 0))  # Fill the block with red color
        self.rect = self.image.get_rect(topleft=(x, y))

    def move(self):
        pass