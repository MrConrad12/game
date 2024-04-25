import pygame

class GameEntity(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        
    def manage_world_contact(self, collisions ):
        self.rect.x += self.vel.x + 0.5 * self.acc.x
        # Vérifier les collisions horizontales
        self.manage_collisions(collisions, self.vel.x, 0)
         # Appliquer les déplacements verticaux
        self.rect.y += self.vel.y + 0.5 * self.acc.y
        # Vérifier les collisions verticales
        self.on_ground = False
        self.manage_collisions(collisions, 0, self.vel.y)
        
            
    def manage_collisions(self, collisions, dx, dy):
        """ gere la collision avec les obstacles """
        for obstacle in collisions:
            if self.rect.colliderect(obstacle.rect):
                # Collision horizontale
                if dx > 0:
                    self.rect.right = obstacle.rect.left
                if dx < 0:
                    self.rect.left = obstacle.rect.right
                # Collision verticale
                if dy > 0:
                    self.rect.bottom = obstacle.rect.top
                    self.on_ground = True
                    self.vel.y = 0
                    self.jumping = False
                if dy < 0:
                    self.rect.top = obstacle.rect.bottom
                    self.vel.y = 0
                    
    def detect_collision(self, group):
        """ detecte la collision avec les autres entités"""
        collisions = pygame.sprite.spritecollide(self, group, False)
        return collisions
            