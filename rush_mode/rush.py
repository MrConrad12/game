
import random
import pygame

from player import Player
from projectile import Projectile
from const import *
from ennemi_volant import EnnemiVolant

BLANC = (255, 255, 255)
NOIR = (0, 0, 0)
ROUGE = (255, 0, 0)
VERT = (0, 255, 0)

# Paramètres de la fenêtre et lancement du jeu
largeur = 1080
hauteur = 700

pygame.init()

pygame.display.set_caption("Avarun: The Way To Liberty")
clock = pygame.time.Clock()
global continuer


class Rush:
    def __init__(self, window_width, window_height):
        self.fenetre = pygame.display.set_mode((window_width, window_height), pygame.HWSURFACE, pygame.DOUBLEBUF)
        player_height = 64
        self.ground_image = pygame.image.load("rush_mode/assets/ground.png").convert_alpha()
        self.ground_width = self.ground_image.get_width()
        self.ground_height = self.ground_image.get_height()
        self.player = Player(x=50, y=(window_height - player_height - self.ground_height), color=NOIR)
        self.obstacles = []
        self.ennemis_volants = []
        self.projectiles = []

        # define game variables
        self.scroll = 0

        self.score = 0
        self.vitesse_jeu = 5
        self.generation_ennemi = 0.002  # Fréquence de la génération des adversaires

        # Intégration de fond parallax
        self.bg_layers = []
        for i in range(1,6):
            self.bg_layer = pygame.image.load(f"rush_mode/assets/plx-{i}.png").convert_alpha()
            self.bg_layers.append(self.bg_layer)
        self.bg_width = self.bg_layers[0].get_width()




    def draw_bg(self):
        for x in range(10000):
            speed = 1
            for i in self.bg_layers:
                self.fenetre.blit(i, ((x * self.bg_width) - self.scroll * speed, 0))
                speed += 0.2

    def draw_ground(self):
        for x in range(10000):
            self.fenetre.blit(self.ground_image, ((x * self.ground_width) - self.scroll * 2.5, hauteur - self.ground_height))

    """def generer_obstacle(self):
        if random.random() < self.generation_ennemi:
            obstacle = Obstacle(largeur, hauteur - 64, ROUGE)
            self.obstacles.append(obstacle)"""

    def attendre_touche(self):
        attente = True
        while attente:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    attente = False
                    pygame.quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_y:
                        jeu = Rush(largeur, hauteur)
                        jeu.jouer()
                        attente = False
                    elif event.key == pygame.K_n:
                        attente = False

    def generer_ennemis_volants(self):
        if random.random() < self.generation_ennemi * 1.1:
            ennemi_volant = EnnemiVolant(largeur, random.randint(int(hauteur * 0.25), int(hauteur * 0.8)), NOIR)
            self.ennemis_volants.append(ennemi_volant)

    def jouer(self):
        continuer = True
        while continuer:
            self.fenetre.fill(VERT)
            clock.tick(90)

            self.draw_bg()
            self.draw_ground()

            key = pygame.key.get_pressed()
            if key[pygame.K_SPACE]:
                self.player.sauter()
            elif key[pygame.K_DOWN]:
                self.player.glisser()
            elif key[pygame.K_x]:
                projectile = Projectile(self.player.rect.right, self.player.rect.centery - 15, 15, ROUGE)
                self.projectiles.append(projectile)

            self.scroll += 5

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    continuer = False

            #self.generer_obstacle()
            self.generer_ennemis_volants()

            if self.detecter_collision():
                for obstacle in self.obstacles:
                    if obstacle is not None and obstacle.life <= 0:
                        self.obstacles.remove(obstacle)
                for ennemi_volant in self.ennemis_volants:
                    if ennemi_volant is not None and ennemi_volant.life <= 0:
                        self.ennemis_volants.remove(ennemi_volant)



            # for bg_layer in self.bg_layers:
            #     bg_layer.update()
            #
            # for bg_layer in self.bg_layers:
            #     bg_layer.afficher(self.fenetre)


            else:
                global score_text, font
                self.score += 1

                if self.player.saut:
                    self.player.rect.y -= self.player.vitesse_saut * 2
                    self.player.vitesse_saut -= 1
                    if self.player.vitesse_saut < -16:
                        self.player.saut = False
                        self.player.vitesse_saut = 16

                if self.player.glisse:
                    if self.player.duree_glissade > 0:
                        self.player.rect.y = hauteur - self.player.height // 2
                        self.player.rect.height = self.player.height // 2
                        self.player.duree_glissade -= 1
                    else:
                        self.player.glisse = False
                        self.player.rect.y = hauteur - self.player.height
                        self.player.rect.height = self.player.height
                        self.player.duree_glissade = 60

                if self.obstacles:
                    for obstacle in self.obstacles:
                        obstacle.rect.x -= self.vitesse_jeu
                        if obstacle.rect.right <= 0:
                            self.obstacles.remove(obstacle)
                            obstacle.rect.x = largeur
                            obstacle.rect.bottom = hauteur

                if self.ennemis_volants:
                    for ennemi_volant in self.ennemis_volants:
                        ennemi_volant.rect.x -= self.vitesse_jeu + 2
                        if ennemi_volant.rect.right <= 0:
                            ennemi_volant.rect.x = largeur
                            ennemi_volant.rect.y = random.randint(10, hauteur - ennemi_volant.rect.height - 10)

                for projectile in self.projectiles:
                    projectile.rect.x += projectile.vitesse
                    projectile.afficher_projectile(self.fenetre)

                self.projectiles = [p for p in self.projectiles if p.rect.x < largeur]

                font = pygame.font.SysFont(None, 30)
                score_text = font.render(f"Score: {self.score}", True, NOIR)
                self.fenetre.blit(score_text, (largeur - 150, 20))

                self.player.afficher(self.fenetre)
                if self.obstacles:
                    for obstacle in self.obstacles:
                        obstacle.afficher_obstacle(self.fenetre)
                if self.ennemis_volants:
                    for ennemi_volant in self.ennemis_volants:
                        ennemi_volant.afficher_ennemi_volant(self.fenetre)

            pygame.display.update()

    def detecter_collision(self):
        global continuer
        for obstacle in self.obstacles:
            if obstacle and self.player.rect.colliderect(obstacle.rect):
                self.afficher_game_over()
                pygame.display.update()
                self.attendre_touche()
                continuer = False

        for ennemi_volant in self.ennemis_volants:
            if ennemi_volant and self.player.rect.colliderect(ennemi_volant.rect):
                self.afficher_game_over()
                pygame.display.update()
                self.attendre_touche()
                continuer = False

        if self.projectiles:
            for projectile in self.projectiles:
                for obstacle in self.obstacles:
                    if obstacle and projectile.rect.colliderect(obstacle.rect):
                        obstacle.life -= 1
                        self.projectiles.remove(projectile)
                        return True

                for ennemi_volant in self.ennemis_volants:
                    if ennemi_volant and projectile.rect.colliderect(ennemi_volant.rect):
                        ennemi_volant.life -= 1
                        self.projectiles.remove(projectile)
                        return True

        return False

    def afficher_game_over(self):
        global score_text
        font = pygame.font.SysFont(None, 100)
        game_over_text = font.render("Game Over", True, ROUGE)
        game_over_text_2 = font.render("Voulez-vous rejouer? Y/N", True, NOIR)
        game_over_rect = game_over_text.get_rect(center=(largeur // 2, hauteur // 2))
        game_over_rect_2 = game_over_text_2.get_rect(center=(largeur // 2, (hauteur // 2) + 50))
        self.fenetre.blit(game_over_text, game_over_rect)
        self.fenetre.blit(game_over_text_2, game_over_rect_2)
        self.fenetre.blit(score_text, ((largeur - score_text.get_width()) // 2, 20))


game = Rush(largeur, hauteur)
game.jouer()
