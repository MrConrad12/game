import pygame
from const import ITEM_PATH


class Projectile(pygame.sprite.Sprite):
    def __init__(self, map, player, direction):
        super().__init__()
        self.velocity = player.launch_speed
        self.map = map
        self.player = player
        self.projectile_path = f'{ITEM_PATH}weapons.png'
        self.image = pygame.image.load(self.projectile_path)
        self.image = pygame.transform.scale(self.image, (30, 30))
        self.origin_image = self.image
        self.projectile_distance = 500
        self.direction = direction  # Nouvelle variable pour le sens du projectile
        if self.direction == 'right':
            self.angle = 225  # Angle pour lancer vers la droite
        else:
            self.angle = 45  # Angle pour lancer vers la gauche
        self.image = pygame.transform.rotozoom(self.origin_image, self.angle, 1)
        self.rect = self.image.get_rect()
        self.rect.x = player.rect.x + 20
        self.rect.y = player.rect.y + 30
        self.original_x = self.rect.x  # Position originale du projectile

    def remove(self):
        self.player.all_projectiles.remove(self)

    def check_collision(self, sprite, group):
        return pygame.sprite.spritecollide(sprite, group, False, pygame.sprite.collide_mask)

    def update(self):
        """Gestion des collisions des projectiles avec les ennemis"""
        self.move()
        for enemy in self.check_collision(self, self.map.enemies):
            self.kill()
            enemy.is_dead = True
        # Si le projectile dépasse une certaine distance de son origine, il se supprime
        if abs(self.rect.x - self.original_x) > self.projectile_distance:  # Changer la distance selon le besoin
            self.kill()

    def move(self):
        if self.direction == 'right':
            self.rect.x += self.velocity
        else:
            self.rect.x -= self.velocity