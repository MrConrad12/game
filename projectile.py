import pygame


class Projectile(pygame.sprite.Sprite):
    def __init__(self, player):
        super().__init__()
        self.velocity = 2
        self.player = player
        self.projectile_path = 'Spear.png'
        self.image = pygame.image.load(self.projectile_path )
        self.image = pygame.transform.scale(self.image, (30, 30))
        self.angle = -45
        self.origin_image = self.image
        self.image = pygame.transform.rotozoom(self.origin_image, self.angle, 1)
        self.rect = self.image.get_rect()
        self.rect.x = player.rect.x + 90
        self.rect.y = player.rect.y + 30

    def remove(self):
        self.player.all_projectiles.remove(self)
        
    def check_collision(self, sprite, group):
        return pygame.sprite.spritecollide(sprite, group, False, pygame.sprite.collide_mask)

    def update(self):
        """gestion des collisions des projectiles avec les enemies"""
        self.rect.x += self.velocity
        for enemy in self.check_collision(self, self.game.all_ennemies):
            self.remove()
            enemy.damage(self.player.attack)
        if self.rect.x > 1080:
            self.remove()
    

