import pygame
import random

# Initialisation de Pygame
pygame.init()

# Taille de l'écran
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Couleurs
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Classe du joueur
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.speed = 5

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
        if keys[pygame.K_UP]:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN]:
            self.rect.y += self.speed

# Classe des items
class Item(pygame.sprite.Sprite):
    def __init__(self, player):
        super().__init__()
        self.image = pygame.image.load('assets/items/spear.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (32, 32))
        self.rect = self.image.get_rect()
        self.player = player
        self.rect.x = random.randrange(SCREEN_WIDTH - self.rect.width)
        self.rect.y = random.randrange(SCREEN_HEIGHT - self.rect.height)
        self.float_speed = random.choice([1, -1])  # Direction du flottement
        self.float_range = 5  # Amplitude du flottement
        self.float_counter = 0  # Compteur pour le flottement

    def update(self):
        # Animation de flottement
        self.rect.y += self.float_speed
        self.float_counter += 1
        pygame.sprite.spritecollide(self.player, self, True)
        if abs(self.float_counter) >= self.float_range:
            self.float_speed *= -1
            self.float_counter *= -1
       
import pygame
import random
import math

# Initialisation de Pygame
pygame.init()

# Définition des couleurs
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Taille de l'écran
WIDTH, HEIGHT = 800, 600

# Création de la fenêtre
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Jeu avec Pygame")



###################################
# ENEMIES ATTACK
###################################



# Classe pour le joueur
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH // 2, HEIGHT // 2)
        self.speed = 5
        self.lives = 3

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
        if keys[pygame.K_UP]:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN]:
            self.rect.y += self.speed

        # Limitation du joueur à l'intérieur de l'écran
        self.rect.x = max(0, min(self.rect.x, WIDTH - self.rect.width))
        self.rect.y = max(0, min(self.rect.y, HEIGHT - self.rect.height))

# Classe pour les ennemis
class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((30, 30))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = 2

    def update(self):
        # Déplacement de l'ennemi
        self.rect.x += random.randint(-self.speed, self.speed)
        self.rect.y += random.randint(-self.speed, self.speed)

# Classe pour les projectiles
class Projectile(pygame.sprite.Sprite):
    def __init__(self, start_x, start_y, target_x, target_y):
        super().__init__()
        self.image = pygame.Surface((10, 10))
        self.image.fill(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = (start_x, start_y)

        # Calcul de la direction vers le joueur
        dx = target_x - start_x
        dy = target_y - start_y
        distance = math.sqrt(dx ** 2 + dy ** 2)
        self.dx = dx / distance
        self.dy = dy / distance
        self.speed = 5

    def update(self):
        # Déplacement du projectile
        self.rect.x += self.speed * self.dx
        self.rect.y += self.speed * self.dy

# Groupe de sprites
all_sprites = pygame.sprite.Group()
enemies = pygame.sprite.Group()
projectiles = pygame.sprite.Group()

# Création du joueur
player = Player()
all_sprites.add(player)

# Création des ennemis
for _ in range(5):
    enemy = Enemy(random.randint(0, WIDTH), random.randint(0, HEIGHT))
    all_sprites.add(enemy)
    enemies.add(enemy)

# Horloge pour gérer la vitesse de rafraîchissement de l'écran
clock = pygame.time.Clock()
counter = 0
# Boucle de jeu
running = True
while running:
    counter += 1
    # Limite de rafraîchissement de l'écran
    clock.tick(60)

    # Gestion des événements
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Mise à jour de tous les sprites
    all_sprites.update()

    # Vérification des collisions entre les ennemis et le joueur
    hits = pygame.sprite.spritecollide(player, enemies, False)
    if hits:
        player.lives -= 1
        print("Le joueur a été touché ! Vies restantes :", player.lives)
        if player.lives <= 0:
            print("Game Over")
            running = False

    # Vérification de la distance entre les ennemis et le joueur pour lancer des projectiles
    for enemy in enemies:
        if math.hypot(player.rect.centerx - enemy.rect.centerx, player.rect.centery - enemy.rect.centery) < 150:
            # Création d'un projectile
            if (counter%20 == 0):
                projectile = Projectile(enemy.rect.centerx, enemy.rect.centery, player.rect.centerx, player.rect.centery)
                all_sprites.add(projectile)
                projectiles.add(projectile)
                counter = 0

    # Effacer l'écran
    screen.fill(WHITE)

    # Dessiner tous les sprites
    all_sprites.draw(screen)

    # Mise à jour de l'affichage
    pygame.display.flip()

# Fermeture de Pygame
pygame.quit()

###################################
# KILL ENEMIES
###################################
# Initialisation de Pygame
pygame.init()

# Définition des constantes
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
GROUND = SCREEN_HEIGHT - 100  # Niveau du sol
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Création de la fenêtre
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Mario-like Game")

# Chargement des images
player_img = pygame.Surface((50, 50))
player_img.fill(BLUE)
enemy_img = pygame.Surface((30, 30))
enemy_img.fill(RED)

# Classe pour le joueur
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = player_img
        self.rect = self.image.get_rect()
        self.rect.centerx = SCREEN_WIDTH // 2
        self.rect.bottom = GROUND
        self.speed_x = 0
        self.speed_y = 0
        self.jump_power = -15

    def update(self):
        # Déplacement horizontal
        self.rect.x += self.speed_x
        # Gravité
        self.speed_y += 1
        # Déplacement vertical
        self.rect.y += self.speed_y
        # Rebond au sol
        if self.rect.bottom > GROUND:
            self.rect.bottom = GROUND
            self.speed_y = 0

    def jump(self):
        # Sauter si sur le sol
        if self.rect.bottom == GROUND:
            self.speed_y = self.jump_power

    def jump_bounce(self):
        # Rebondir un peu en sautant sur un ennemi
        self.speed_y = -10

# Classe pour les ennemis
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = enemy_img
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, SCREEN_WIDTH - self.rect.width)
        self.rect.bottom = GROUND

    def update(self):
        # Les ennemis ne bougent pas, juste pour l'affichage
        pass

# Groupe de sprites
all_sprites = pygame.sprite.Group()
enemies = pygame.sprite.Group()

# Création du joueur
player = Player()
all_sprites.add(player)

# Création des ennemis
for _ in range(100):
    enemy = Enemy()
    all_sprites.add(enemy)
    enemies.add(enemy)

# Horloge pour gérer la vitesse de rafraîchissement de l'écran
clock = pygame.time.Clock()

# Boucle de jeu
"""running = True
while running:
    # Limite de rafraîchissement de l'écran
    clock.tick(60)

    # Gestion des événements
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player.speed_x = -5
            elif event.key == pygame.K_RIGHT:
                player.speed_x = 5
            elif event.key == pygame.K_SPACE:
                player.jump()
    if player.rect.bottomleft[0] <= 0 or player.rect.bottomright[0]>=WIDTH:
        player.speed_x = -player.speed_x

    # Mise à jour de tous les sprites
    all_sprites.update()

    # Vérification des collisions entre le joueur et les ennemis
    hits = pygame.sprite.spritecollide(player, enemies, False)
    for enemy in hits:
        # Si le joueur saute sur l'ennemi
        if player.speed_y > 0 and player.rect.bottom < enemy.rect.bottom:
            player.jump_bounce()
            enemy.kill()  # L'ennemi meurt
        

    # Effacer l'écran
    screen.fill(WHITE)

    # Dessiner tous les sprites
    all_sprites.draw(screen)

    # Mise à jour de l'affichage
    pygame.display.flip()

# Fermeture de Pygame
pygame.quit()


"""
"""import pygame
import numpy as np

# Initialisation de Pygame
pygame.init()

# Définition des constantes
CELL_SIZE = 2
GRID_WIDTH = 100
GRID_HEIGHT = 100
SCREEN_WIDTH = CELL_SIZE * GRID_WIDTH
SCREEN_HEIGHT = CELL_SIZE * GRID_HEIGHT
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Création de la fenêtre
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Jeu de la Vie")

# Fonction pour initialiser la grille
def initialize_grid():
    return np.random.choice([0, 1], size=(GRID_WIDTH, GRID_HEIGHT))

# Fonction pour mettre à jour la grille selon les règles du jeu de la vie
def update_grid(grid):
    new_grid = np.zeros_like(grid)
    for x in range(1, GRID_WIDTH - 1):
        for y in range(1, GRID_HEIGHT - 1):
            neighbors_sum = np.sum(grid[x - 1 : x + 2, y - 1 : y + 2]) - grid[x, y]
            if grid[x, y] == 1:
                if neighbors_sum < 2 or neighbors_sum > 3:
                    new_grid[x, y] = 0
                else:
                    new_grid[x, y] = 1
            elif neighbors_sum == 3:
                new_grid[x, y] = 1
    return new_grid

# Fonction pour dessiner la grille
def draw_grid(grid):
    screen.fill(WHITE)
    for x in range(GRID_WIDTH):
        for y in range(GRID_HEIGHT):
            if grid[x, y] == 1:
                pygame.draw.rect(screen, BLACK, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))
    pygame.display.flip()

# Initialisation de la grille
grid = initialize_grid()

# Horloge pour contrôler la vitesse de rafraîchissement
clock = pygame.time.Clock()

# Boucle de jeu
running = True
while running:
    # Limite de rafraîchissement de l'écran
    clock.tick(10)

    # Gestion des événements
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Mise à jour de la grille
    grid = update_grid(grid)

    # Dessiner la grille
    draw_grid(grid)

# Fermeture de Pygame
pygame.quit()
"""