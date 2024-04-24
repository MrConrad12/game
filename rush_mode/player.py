import pygame


class Player:
    def __init__(self, x, y, color):
        self.width = 64
        self.height = 64
        self.rect = pygame.Rect(x, y, self.width, self.height)
        self.saut = False
        self.glisse = False
        self.vitesse_saut = 16
        self.duree_glissade = 60
        self.color = color

    def afficher(self, fenetre):
        pygame.draw.rect(fenetre, self.color, self.rect)

    def sauter(self):
        self.saut = True

    def glisser(self):
        self.glisse = True
