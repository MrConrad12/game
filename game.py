import pygame
from const import *
from map_manager import MapManager
from player import Player
from screen import MenuGame

class Game:
    def __init__(self):
        pygame.init()
        self.background = pygame.image.load('assets/decoration/fond1.jpg')
        self.background = pygame.transform.scale(self.background, (WIDTH, HEIGHT *1.4))
        self.welcome_background = pygame.image.load('assets/decoration/fond2.jpg')
        self.welcome_background = pygame.transform.scale(self.welcome_background, (WIDTH, HEIGHT *1.4))
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Game")
        self.clock = pygame.time.Clock()
        self.game_state = START_MENU        
        self.current_map = MapManager(self)
        self.current_map.load_map( 'map', 'map/map_industrie/map_industrie.tmx')
        self.menu = MenuGame(self)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self.menu.handle_button_clicks(mouse_pos)
           
    def run_game(self):
        """charge le jeu (avec la map)"""
        self.current_map.update()
        if self.game_state == GAME:
            self.screen.blit(self.menu.home_button['image'], self.menu.home_button['rect'])
        pygame.display.update()
        self.clock.tick(FPS)

    def run(self):
        self.running = True
        self.menu.draw_welcome_page()
        pygame.time.delay(1000)  
        while self.running:
            if self.game_state == START_MENU:
                self.menu.draw_start_menu()
            elif self.game_state == LEVEL:
                self.menu.draw_level_menu()
            elif self.game_state == GAME:
                self.run_game()
            self.handle_events()
        pygame.quit()
if __name__ =='__main__':
    game = Game()
    game.run()