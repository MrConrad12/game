import pygame


class Projectile:
    def __init__(self, x, y, vitesse, color):
        self.width = 32
        self.height = 16
        self.rect = pygame.Rect(x, y, self.width, self.height)
        self.vitesse = vitesse
        self.color = color

    def afficher_projectile(self, fenetre):
        pygame.draw.rect(fenetre, self.color, self.rect)
