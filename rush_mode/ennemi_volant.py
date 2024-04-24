import pygame


class EnnemiVolant:
    def __init__(self, x, y, color):
        self.width = 64
        self.height = 64
        self.rect = pygame.Rect(x, y, self.width, self.height)
        self.life = 5
        self.color = color

    def afficher_ennemi_volant(self, fenetre):
        font = pygame.font.SysFont(None, 20)
        life_text = font.render(f"{self.life}/5", True, self.color)
        fenetre.blit(life_text, (self.rect.x, self.rect.y - 32))
        pygame.draw.rect(fenetre, self.color, self.rect)
