import pygame
from const import *


class MenuGame:
    def __init__(self, game):
        self.game = game
        self.play_button_image = pygame.image.load('assets/bouton.png')
        self.help_button_image = pygame.image.load('assets/help_button.png')
        self.exit_button_image = pygame.image.load('assets/exit_button.png')
        self.back_button_image = pygame.image.load('assets/home_button.png')

        self.play_button_rect = self.play_button_image.get_rect()
        self.exit_button_rect = self.exit_button_image.get_rect()
        self.back_button_rect = self.back_button_image.get_rect()
        self.setup_button_positions()

    def setup_button_positions(self):
        self.play_button_rect.centerx = WIDTH // 2
        self.play_button_rect.centery = HEIGHT // 2
        self.exit_button_rect.centerx = WIDTH // 2
        self.exit_button_rect.centery = HEIGHT // 2 + 80
        self.back_button_rect.topright = (WIDTH - 10, 10)

    def draw_start_menu(self):
        self.game.screen.blit(self.game.background, (0, -200))
        self.game.screen.blit(self.play_button_image, self.play_button_rect)
        self.game.screen.blit(self.exit_button_image, self.exit_button_rect)
        pygame.display.update()

    def handle_button_clicks(self, mouse_pos):
        if self.game.game_state == START_MENU:
            if self.play_button_rect.collidepoint(mouse_pos):
                self.game.game_state = GAME
            elif self.exit_button_rect.collidepoint(mouse_pos):
                self.game.running = False
        elif self.game.game_state == GAME:
            if self.back_button_rect.collidepoint(mouse_pos):
                self.game.game_state = START_MENU
