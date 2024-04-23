import math
import random
import pygame
import sys

from const import FONT_PATH
PATH = "assets/panneau2.jpg" 
class ImageResizeAnimation:
    def __init__(self, image_path, initial_size, final_size):
        self.original_image = pygame.image.load(image_path)
        self.image = self.original_image.copy() 
        self.initial_size = initial_size
        self.final_size = final_size
        self.current_size = initial_size
        self.animation_speed = 3  # Vitesse de l'animation
        self.rect = self.image.get_rect()

    def update(self):
        # Animer le changement de taille
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            if self.current_size < self.final_size:
                self.current_size += self.animation_speed
        else:
            if self.current_size > self.initial_size:
                self.current_size -= self.animation_speed

        # Redimensionner l'image
        self.image = pygame.transform.scale(self.original_image, (self.current_size, self.current_size))
        self.rect = self.image.get_rect(center=self.rect.center)

    def draw(self, surface):
        surface.blit(self.image, self.rect)

def size_animation():
    pygame.init()

    # Configurer l'écran
    screen_width, screen_height = 800, 600
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Image Resize Animation")

    # Couleurs
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)

    # Créer l'objet ImageResizeAnimation
    image_path = PATH
    initial_size = 100
    final_size = 120
    image_animation = ImageResizeAnimation(image_path, initial_size, final_size)

    clock = pygame.time.Clock()

    running = True
    while running:
        screen.fill(WHITE)

        # Gérer les événements
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break

        # Mettre à jour et dessiner l'image
        image_animation.update()
        image_animation.draw(screen)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()
    
    
class ImageFloatAnimation:
    def __init__(self, image_path, screen_width, screen_height):
        self.image = pygame.image.load(image_path)
        self.rect = self.image.get_rect()
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.reset()

    def reset(self):
        self.rect.x = random.randint(0, self.screen_width - self.rect.width)
        self.rect.y = self.screen_height
        self.speed_x = random.uniform(-1, 1)  # Vitesse horizontale aléatoire
        self.speed_y = random.uniform(-2, -1)  # Vitesse verticale aléatoire

    def update(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        # Si l'image sort de l'écran, la réinitialiser
        if self.rect.top > self.screen_height or self.rect.right < 0 or self.rect.left > self.screen_width:
            self.reset()

    def draw(self, surface):
        surface.blit(self.image, self.rect)

def floating_animation():
    pygame.init()

    # Configurer l'écran
    screen_width, screen_height = 800, 600
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Floating Image Animation")

    # Couleur de fond
    WHITE = (255, 255, 255)

    # Créer l'objet ImageFloatAnimation
    image_path = PATH 
    image_animation = ImageFloatAnimation(image_path, screen_width, screen_height)

    clock = pygame.time.Clock()

    running = True
    while running:
        screen.fill(WHITE)

        # Gérer les événements
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break

        # Mettre à jour et dessiner l'image
        image_animation.update()
        image_animation.draw(screen)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()



class ImageFloatAnimationStatic:
    def __init__(self, image_path, screen_width, screen_height):
        self.image = pygame.image.load(image_path)
        self.rect = self.image.get_rect(center=(screen_width // 2, screen_height // 2))
        self.amplitude = 20  # Amplitude du mouvement
        self.frequency = 0.05  # Fréquence du mouvement
        self.angle = 0

    def update(self):
        # Calculer la nouvelle position en fonction du temps
        self.angle += self.frequency
        delta_y = self.amplitude * math.sin(self.angle)
        self.rect.y = delta_y + (self.rect.y + self.rect.height // 2)

    def draw(self, surface):
        surface.blit(self.image, self.rect)

def float_animation_static():
    pygame.init()

    # Configurer l'écran
    screen_width, screen_height = 800, 600
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Floating Image Animation")

    # Couleur de fond
    WHITE = (255, 255, 255)

    # Créer l'objet ImageFloatAnimation
    image_path = PATH 
    image_animation = ImageFloatAnimationStatic(image_path, screen_width, screen_height)

    clock = pygame.time.Clock()

    running = True
    while running:
        screen.fill(WHITE)

        # Gérer les événements
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break

        # Mettre à jour et dessiner l'image
        image_animation.update()
        image_animation.draw(screen)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()
import pygame
import sys

class Button:
    def __init__(self, text, position):
        self.font = pygame.font.Font(None, 36)
        self.text = text
        self.image = self.font.render(text, True, (0, 0, 0))
        self.rect = self.image.get_rect(topleft=position)

    def draw(self, surface):
        surface.blit(self.image, self.rect)

def slide_animation(surface, start_pos, end_pos, button, direction):
    # Calculer la différence de position
    dx = end_pos[0] - start_pos[0]
    dy = end_pos[1] - start_pos[1]

    # Effectuer l'animation
    step = 10
    for i in range(step):
        surface.fill((255, 255, 255))  # Efface l'écran
        button.rect.x = start_pos[0] + int(dx * i / step) if direction == 'left' else start_pos[0] - int(dx * i / step)
        button.rect.y = start_pos[1] + int(dy * i / step)
        button.draw(surface)
        pygame.display.flip()
        pygame.time.delay(20)

def main():
    pygame.init()

    # Configurer l'écran
    screen_width, screen_height = 800, 600
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Button Slide Animation")

    # Couleur de fond
    WHITE = (255, 255, 255)

    # Créer les boutons
    button1 = Button("Menu 1", (50, 50))
    button2 = Button("Menu 2", (50, 50))
    menu1_buttons = [button1]
    menu2_buttons = [button2]

    clock = pygame.time.Clock()

    current_menu = menu1_buttons
    while True:
        screen.fill(WHITE)

        # Gérer les événements
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Clic gauche
                if current_menu == menu1_buttons and button1.rect.collidepoint(event.pos):
                    slide_animation(screen, button1.rect.topleft, (-button1.rect.width, 50), button1, 'left')
                    current_menu = menu2_buttons
                elif current_menu == menu2_buttons and button2.rect.collidepoint(event.pos):
                    slide_animation(screen, button2.rect.topleft, (50, 50), button2, 'right')
                    current_menu = menu1_buttons

        # Dessiner les boutons actuels
        for button in current_menu:
            button.draw(screen)

        pygame.display.flip()
        clock.tick(60)

class ImageWithText:
    def __init__(self, image_path, text, font_path, image_position, font_size=36):
        pygame.init()

        # Initialisation de la fenêtre
        self.screen_width, self.screen_height = 800, 600
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Image with Text")

        # Chargement de l'image
        self.image = pygame.image.load(image_path)
        self.image_rect = self.image.get_rect(center=image_position)

        # Chargement de la police personnalisée
        self.font = pygame.font.Font(font_path, font_size)

        # Création de la surface pour le texte
        self.text_surface = self.font.render(text, True, (255, 255, 255))
        self.text_rect = self.text_surface.get_rect(center=self.image_rect.center)

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            # Effacement de l'écran
            self.screen.fill((0, 0, 0))

            # Affichage de l'image
            self.screen.blit(self.image, self.image_rect)

            # Affichage du texte
            self.screen.blit(self.text_surface, self.text_rect)

            pygame.display.flip()

        pygame.quit()
        sys.exit()
import pygame
from pygame.locals import *

class VideoManager:
    def __init__(self, video_path, screen_width=800, screen_height=600):
        pygame.init()

        # Initialisation de la fenêtre
        self.screen = pygame.display.set_mode((screen_width, screen_height))
        pygame.display.set_caption("Video Player")

        # Chargement de la vidéo
        self.video = pygame.movie.Movie(video_path)
        self.video_screen = pygame.Surface((screen_width, screen_height))

        # Démarrage de la lecture
        self.video.set_display(self.video_screen)
        self.video.play()

    def play_video(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                    running = False

            # Effacement de l'écran
            self.screen.fill((0, 0, 0))

            # Affichage de la vidéo
            self.screen.blit(self.video_screen, (0, 0))

            pygame.display.flip()
            pygame.time.Clock().tick(30)

        self.video.stop()
        pygame.quit()

import pygame
import sys
import pygame
import sys
class ImageWithText:
    def __init__(self, image_path, text_lines, image_position, font_path=None, font_size=24, font_color=(255, 255, 255)):
        pygame.init()

        # Charger l'image
        self.image = pygame.image.load(image_path)
        self.image_rect = self.image.get_rect(center=image_position)

        # Créer la police
        if font_path is not None:
            self.font = pygame.font.Font(font_path, font_size)
        else:
            self.font = pygame.font.SysFont(None, font_size)

        # Préparer les lignes de texte
        self.text_surfaces = []
        self.text_rects = []
        max_width = 0
        total_height = 0
        for line in text_lines:
            text_surface = self.font.render(line, True, font_color)
            text_rect = text_surface.get_rect()
            self.text_surfaces.append(text_surface)
            self.text_rects.append(text_rect)
            total_height += text_rect.height
            if text_rect.width > max_width:
                max_width = text_rect.width

        # Positionner les textes
        y_offset = self.image_rect.centery - total_height / 2
        for surface, rect in zip(self.text_surfaces, self.text_rects):
            rect.centerx = self.image_rect.centerx
            rect.top = y_offset
            y_offset += rect.height

        # Centrer le groupe de texte par rapport à l'image
        text_group_rect = pygame.Rect(0, 0, max_width, total_height)
        text_group_rect.center = self.image_rect.center
        for rect in self.text_rects:
            rect.centerx = text_group_rect.centerx

    def draw(self, screen):
        # Dessiner l'image
        screen.blit(self.image, self.image_rect)

        # Dessiner les lignes de texte
        for surface, rect in zip(self.text_surfaces, self.text_rects):
            screen.blit(surface, rect.topleft)
import pygame
import sys

# Constantes de couleur
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Constantes de jeu
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
PLAYER_SIZE = 50
PLAYER_SPEED = 5
PLAYER_JUMP_POWER = 14  # Puissance du saut
GRAVITY = 0.8

# Classe pour le joueur
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((PLAYER_SIZE, PLAYER_SIZE))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.vx = 0
        self.vy = 0
        self.on_ground = False

    def update(self, keys):
        # Gestion des déplacements
        self.vx = 0
        if keys[pygame.K_LEFT]:
            self.vx = -PLAYER_SPEED
        if keys[pygame.K_RIGHT]:
            self.vx = PLAYER_SPEED

        # Appliquer la gravité
        if not self.on_ground:
            self.vy += GRAVITY

        # Appliquer les déplacements horizontaux
        self.rect.x += self.vx

        # Vérifier les collisions horizontales
        self.check_collisions(self.vx, 0)

        # Appliquer les déplacements verticaux
        self.rect.y += self.vy

        # Vérifier les collisions verticales
        self.on_ground = False
        self.check_collisions(0, self.vy)

    def jump(self):
        # Le joueur ne peut sauter que s'il est au sol
        if self.on_ground:
            self.vy = -PLAYER_JUMP_POWER

    def check_collisions(self, dx, dy):
        for obstacle in obstacles:
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
                    self.vy = 0
                if dy < 0:
                    self.rect.top = obstacle.rect.bottom
                    self.vy = 0

# Classe pour les obstacles
class Obstacle(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

# Initialisation de Pygame
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Platformer Game")

# Création des sprites
all_sprites = pygame.sprite.Group()
obstacles = pygame.sprite.Group()

player = Player(100, SCREEN_HEIGHT - PLAYER_SIZE - 100)
all_sprites.add(player)

# Création du sol
ground = Obstacle(0, SCREEN_HEIGHT - 50, SCREEN_WIDTH, 50)
obstacles.add(ground)
all_sprites.add(ground)

# Création des obstacles
obstacle1 = Obstacle(300, SCREEN_HEIGHT - 100, 100, 20)
obstacle2 = Obstacle(500, SCREEN_HEIGHT - 300, 150, 30)
obstacles.add(obstacle1, obstacle2)
all_sprites.add(obstacle1, obstacle2)

clock = pygame.time.Clock()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.jump()

    keys = pygame.key.get_pressed()
    player.update(keys)

    # Affichage
    screen.fill(WHITE)
    all_sprites.draw(screen)
    pygame.display.flip()

    clock.tick(60)

pygame.quit()
sys.exit()

