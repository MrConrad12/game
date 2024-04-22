import pygame

from const import WIDTH

class Projectile(pygame.sprite.Sprite):

    def __init__(self, player):
        super().__init__()
        self.velocity = 2
        self.player = player
        self.image = pygame.image.load('Projectile.png')
        self.rect = self.image.get_rect()
        self.rect.x = player.rect.x + 90
        self.rect.y = player.rect.y + 30
        self.origin_image = self.image
        self.angle = 0

    def rotate(self):
        """ fait tourner le projectile """
        self.angle += 10
        self.image = pygame.transform.rotozoom(self.origin_image, self.angle, 1)
        self.rect = self.image.get_rect(center=self.rect.center)

    def remove(self):
        self.player.all_projectiles.remove(self)

    def move_projectile(self):
        """ gere le deplacement du projectile """
        self.rect.x += self.velocity
        self.rotate()
        if self.rect.x > WIDTH:
            self.remove()

