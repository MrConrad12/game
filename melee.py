import pygame

class Melee(pygame.sprite.Sprite):

    def __init__(self, player):
        super().__init__()
        self.player = player
        self.image = pygame.image.load('Spear.png')
        self.image = pygame.transform.scale(self.image, (30, 30))
        self.angle = -45
        self.origin_image = self.image
        self.image = pygame.transform.rotozoom(self.origin_image, self.angle, 1)
        self.velocity = 1

        self.rect = self.image.get_rect()
        self.rect.x = player.rect.x + 60
        self.rect.y = player.rect.y + 30

    # def rotate(self):
        # Faire tourner le projectile
    # self.rect = self.image.get_rect(center=self.rect.center)

    def remove(self):
        self.player.all_melee.remove(self)

    def melee(self):
        self.rect.x += self.velocity
        if self.rect.x > self.player.rect.x + 100:
            self.remove()

        # Verifier si l'attaque de melee est en collision avec le monstre
        for enemy in self.player.game.check_collision(self, self.player.game.all_Ennemies):
            # Supprimer le projectile
            self.remove()
            # Infliger des degats
            enemy.Damage(self.player.attack)
