import pygame
import random
import sys

# Initialisation de Pygame
pygame.init()

# Définition des constantes
SCREEN_WIDTH = 1080
SCREEN_HEIGHT = 700
PLAYER_WIDTH = 64
PLAYER_HEIGHT = 64
OBSTACLE_WIDTH = 32
OBSTACLE_HEIGHT = 64
ENEMY_WIDTH = 64
ENEMY_HEIGHT = 64
PROJECTILE_WIDTH = 16
PROJECTILE_HEIGHT = 8

# Couleurs
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Classe pour le joueur
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((PLAYER_WIDTH, PLAYER_HEIGHT))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.center = (SCREEN_WIDTH // 4, SCREEN_HEIGHT - PLAYER_HEIGHT // 2)
        self.velocity = 0
        self.jump_height = -15

    def update(self):
        self.velocity += 1
        self.rect.y += self.velocity
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT
            self.velocity = 0

    def jump(self):
        if self.rect.bottom == SCREEN_HEIGHT:
            self.velocity = self.jump_height

# Classe pour les obstacles
class Obstacle(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((OBSTACLE_WIDTH, OBSTACLE_HEIGHT))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.center = (SCREEN_WIDTH, SCREEN_HEIGHT - OBSTACLE_HEIGHT // 2)
        self.velocity = -5

    def update(self):
        self.rect.x += self.velocity
        if self.rect.right <= 0:
            self.rect.left = SCREEN_WIDTH
            self.rect.bottom = SCREEN_HEIGHT - OBSTACLE_HEIGHT // 2

# Classe pour les ennemis volants
class FlyingEnemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((ENEMY_WIDTH, ENEMY_HEIGHT))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.center = (SCREEN_WIDTH, random.randint(0, SCREEN_HEIGHT - ENEMY_HEIGHT))
        self.velocity = -7

    def update(self):
        self.rect.x += self.velocity
        if self.rect.right <= 0:
            self.rect.left = SCREEN_WIDTH
            self.rect.centery = random.randint(0, SCREEN_HEIGHT - ENEMY_HEIGHT)

# Classe pour les projectiles
class Projectile(pygame.sprite.Sprite):
    def __init__(self, player_rect):
        super().__init__()
        self.image = pygame.Surface((PROJECTILE_WIDTH, PROJECTILE_HEIGHT))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.center = player_rect.center
        self.velocity = 10

    def update(self):
        self.rect.x += self.velocity
        if self.rect.left >= SCREEN_WIDTH:
            self.kill()

# Fonction principale du jeu
def main():
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Dino Game")
    clock = pygame.time.Clock()
    player = Player()
    obstacles = pygame.sprite.Group()
    flying_enemies = pygame.sprite.Group()
    projectiles = pygame.sprite.Group()
    all_sprites = pygame.sprite.Group()
    all_sprites.add(player)

    score = 0

    running = True
    game_over = False
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                game_over = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    player.jump()
                elif event.key == pygame.K_DOWN:
                    pass  # Placeholder for sliding action
                elif event.key == pygame.K_ESCAPE:
                    running = False
                    game_over = False
                elif event.key == pygame.K_SPACE:
                    projectiles.add(Projectile(player.rect))

        if not game_over:
            screen.fill(BLACK)

            for sprite in all_sprites:
                screen.blit(sprite.image, sprite.rect)

            obstacles.update()
            obstacles.draw(screen)

            flying_enemies.update()
            flying_enemies.draw(screen)

            projectiles.update()
            projectiles.draw(screen)

            all_sprites.update()

            # Gestion des collisions
            hits = pygame.sprite.spritecollide(player, obstacles, False)
            if hits:
                game_over = True

            hits = pygame.sprite.spritecollide(player, flying_enemies, False)
            if hits:
                game_over = True

            hits = pygame.sprite.groupcollide(projectiles, obstacles, True, True)
            if hits:
                score += 1

            hits = pygame.sprite.groupcollide(projectiles, flying_enemies, True, True)
            if hits:
                score += 1

            # Affichage du score
            font = pygame.font.Font(None, 36)
            score_text = font.render("Score: " + str(score), True, WHITE)
            screen.blit(score_text, (10, 10))

            pygame.display.flip()
            clock.tick(30)
        else:
            # Affichage de l'écran de game over
            font = pygame.font.Font(None, 72)
            game_over_text = font.render("Game Over", True, WHITE)
            screen.blit(game_over_text, (SCREEN_WIDTH // 2 - 200, SCREEN_HEIGHT // 2 - 50))

            font = pygame.font.Font(None, 36)
            score_text = font.render("Score: " + str(score), True, WHITE)
            screen.blit(score_text, (SCREEN_WIDTH // 2 - 80, SCREEN_HEIGHT // 2 + 50))

            pygame.display.flip()

            # Attente de la réponse de l'utilisateur
            while True:
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_y:
                            main()
                        elif event.key == pygame.K_n:
                            running = False
                            break
                if not running:
                    break

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
