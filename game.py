import pygame
from const import *
from map_manager import MapManager
from screen import ScreenGame
from audio_manager import AudioManager
from pygame.mixer import *
from timer_manager import GameTimer

# Defense, armes, score gagnant
pygame.mixer.init()
class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Gounki")
        self.clock = pygame.time.Clock()
        self.play_time = 180
        
        self.game_state = START_MENU       
        self.win = True
         
        self.map = MapManager(self)
        self.audio_manager = AudioManager(self)
        self.map.load_map( 'map', 'map/forest_map/forest_map.tmx')
        self.menu = ScreenGame(self)
        self.timer = GameTimer(self.play_time)

    def handle_events(self):
        """ gestion des touches de souris"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self.menu.handle_button_clicks(mouse_pos)
           
    def game(self):
        """charge le jeu (avec la map)"""      
        self.map.update()
        self.menu.draw_hud()

    def run(self):
        self.running = True
        self.menu.draw_welcome_page()
        while self.running:
            if self.game_state == START_MENU:
                self.menu.draw_start_menu()
            elif self.game_state == LEVEL:
                self.menu.draw_level_menu()
            elif self.game_state == GAME:
                self.game()
            self.handle_events()
            pygame.display.update()
            self.clock.tick(FPS)
            
        pygame.quit()
        
if __name__ =='__main__':
    game = Game()
    game.run()