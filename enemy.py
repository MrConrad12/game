import pygame
import random


class Enemy(pygame.sprite.Sprite):

    def __init__(self, game):
        super().__init__()
        self.game = game
        self.health = 100
        self.Maxhealth = 100
        self.Attack = 0.2
        self.velocity = random.randint(1, 3)
        self.image = pygame.image.load("Wolf.jpg")
        self.image = pygame.transform.scale(self.image, (50, 80))
        self.rect = self.image.get_rect()
        self.rect.x += 1000 + random.randint(0, 300)
        self.rect.y += 600
        self.loot_amount = 10

    def Damage(self, amount):
        # Mettre les degats du personnage
        self.health -= amount

        # Verifier si les points de vie plus petit ou egal a 0
        if self.health <= 0:
            # Reapparaitre le monstre
            self.rect.x = 1000 + random.randint(0, 300)
            self.velocity = random.randint(1, 3)
            self.health = self.Maxhealth
            self.game.add_score(self.loot_amount)

    def set_loot_amount(self, amount):
        self.loot_amount = amount

    def Update_health_bar(self, surface):
        # definir la couleur de notre barre de vie
        bar_color = (110, 210, 40)
        # definir la couleur de notre arriere barre de vie
        back_bar_color = (60, 60, 60)

        # definir la position de notre barre de vie ainsi que sa longeur et epaisseur
        healthbar_position = [self.rect.x - 1, self.rect.y - 10, self.health, 3]
        # definir la position de notre barre de vie arriere
        back_healthbar_position = [self.rect.x - 1, self.rect.y - 10, self.Maxhealth, 3]

        # dessiner la barre de vie
        pygame.draw.rect(surface, back_bar_color, back_healthbar_position)
        pygame.draw.rect(surface, bar_color, healthbar_position)

    def forward(self):
        self.rect.x -= self.velocity
        # Detecter si il ya une collision
        if self.game.check_collision(self, self.game.all_Players):
            # Infliger des degats
            self.game.player.Damage(self.Attack)
            self.game.player.health_number -= 1
