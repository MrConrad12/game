import pygame
from animation import AnimatedButton, AnimatedCard
from buttons import ImageWithText, ImageWithTextGroup
from const import *
from map_manager import MapManager
from player_selection import SelectablePlayer

class MenuGame:
    def __init__(self, game):
        self.game = game
        self.level_selected = "Whispering Woods"
        player = game.current_map.player
        
        # bouton pour le menu prinipale
        self.start_button = self.draw_image_button(f'bouton.png')
        self.exit_button = self.draw_image_button(f'exit_button.png', offsetY = 80)
        self.home_button = self.draw_image_button(f'home_button.png', posX = WIDTH - 60, posY= 60 )
        
        # bouton pour les niveaux
        self.levels = self.load_level_boutton()
        self.play_button = AnimatedButton(self.game, f'{BUTTON_PATH}cadre.png', width = 80, height = 50, posY=HEIGHT - 120)
                
        # bouton pour le personnage
        #self.change_right_player = AnimatedCard(self.game, f'{BUTTON_PATH}next_right.png', 80,posX=SELECTABLE_PLAYER_POS_X + 45, posY=SELECTABLE_PLAYER_POS_Y - 25, add_size=5)
        #self.change_left_player = AnimatedCard(self.game, f'{BUTTON_PATH}next_left.png', 80,posX=SELECTABLE_PLAYER_POS_X - 160, posY=SELECTABLE_PLAYER_POS_Y - 25, add_size=5)
        
        # statistiques
        self.player_stat_data = [f"Live:  {player.lives}", f"Speed: {player.speed}", f"Damage: {player.damage}", f"+ {player.aptitude}"]
        self.player_stat = ImageWithTextGroup(self.game.screen, 'panneau0.png', self.player_stat_data,(SELECTABLE_PLAYER_POS_X,  SELECTABLE_PLAYER_POS_Y * 2.6), resizing=True, size=(220,200))
        self.image = ImageWithText(self.game.screen,'cadre.png', f"{player.name}", (SELECTABLE_PLAYER_POS_X,  SELECTABLE_PLAYER_POS_Y * 1.8), True, (200, 80), font_size=36)
        self.win_button = ImageWithText(self.game.screen,'cadre.png', "WIN", (WIDTH // 2,  HEIGHT //3), True, (200, 80), font_size=36)
        self.lose_button = ImageWithText(self.game.screen,'cadre.png', "LOSE", (WIDTH // 2,  HEIGHT //3), True, (200, 80), font_size=36)
        self.play_button = ImageWithText(self.game.screen,'cadre.png',"PLAY", (WIDTH // 2,  HEIGHT - 50), True, (200, 80), font_size=36)
        self.player = SelectablePlayer(image="assets/selectable_player/player1")
        
        self.choose = False
    def load_level_boutton(self):
        """charger les boutons de selection des niveaux"""
        levels = {}
        space = 10
        x_spacing = CARD_SIZE + space
        y_spacing = CARD_SIZE + space
        
        # gestion des espacement pour creer 2 lignes de 3 colonnes
        for i,(level_name, level_data) in enumerate(LEVELS.items()):
            image = level_data['image']
            path = level_data['path']
            row = i // 2 
            col = i % 2 
            x = (col * x_spacing) - 20
            y = (row * y_spacing) - 20
            levels[level_name] = AnimatedCard(self.game, image, CARD_SIZE,posX=x + 100, posY=y, offsetX=0, offsetY=0)
        return levels

    def draw_image_button(self, image_src, offsetX = 0, offsetY = 0, posX = WIDTH // 2, posY = HEIGHT //2):
        image = pygame.image.load(BUTTON_PATH+image_src)
        rect = image.get_rect()
        rect.centerx = posX + offsetX
        rect.centery = posY + offsetY
        return {'image':image, 'rect':rect}

    def draw_welcome_page(self):
        """menu d'acceuil"""
        background = pygame.image.load('assets/decoration/fond2.jpg')
        background = pygame.transform.scale(background, (WIDTH, HEIGHT *1.4))
        self.game.screen.blit(self.game.welcome_background, (0, -200))
        pygame.display.update()

    def draw_start_menu(self):
        """dessine le menu principal avec ces composants"""
        self.game.screen.blit(self.game.background, (0, -200))
        if self.game.win:
            self.win_button.draw()
        else:
            self.lose_button.draw()
        self.game.screen.blit(self.start_button['image'], self.start_button['rect'])
        self.game.screen.blit(self.exit_button['image'], self.exit_button['rect'])
        pygame.display.update()
   
    def draw_level_menu(self):
        """menu de niveau selection de personnage et de niveau"""
        self.game.screen.blit(self.game.background, (0, -200))
        for level in self.levels:
            self.levels[level].update()
        self.game.screen.blit(self.home_button['image'], self.home_button['rect'])
        self.game.screen.blit(self.player.image, self.player.rect)
        #self.change_right_player.update()
        #self.change_left_player.update()
        self.image.draw()
        self.play_button.draw()
        self.player_stat.draw()
        self.player.update()
        pygame.display.update()

    def handle_button_clicks(self, mouse_pos):
        """ gestion des clique de souris """
        if self.game.game_state == START_MENU:
            if self.start_button['rect'].collidepoint(mouse_pos):
                self.game.game_state = LEVEL
                self.game.audio_manager.play_sound('forward_effect')
            elif self.exit_button['rect'].collidepoint(mouse_pos):
                self.game.running = False
                self.game.audio_manager.play_sound('close_effect')
                pygame.time.delay(1000)  

        if self.home_button['rect'].collidepoint(mouse_pos):
            self.game.game_state = START_MENU
            self.game.audio_manager.play_sound('backward_effect')
            self.game.audio_manager.load_bgm_menu()
            
        if self.game.game_state == LEVEL:
            self.choose_level(mouse_pos)
            if self.play_button.rect.collidepoint(mouse_pos):
                self.game.current_map = MapManager(self.game)
                self.game.timer.current_duration = 60
                self.game.current_map.load_map( self.level_selected, LEVELS[self.level_selected]['path'])
                self.game.audio_manager.load_bgm_game()
                self.game.game_state = GAME
        
        
    def choose_level(self,mouse_pos):
        mouse_pos = pygame.mouse.get_pos()
        for level, button in self.levels.items():
            if button.rect.collidepoint(mouse_pos) and not button.isSelected:
                self.level_selected = level
                #self.levels[button].isSelected = True
                self.game.audio_manager.play_sound('forward_effect')
                button.isSelected = True                
            else:
                button.isSelected = False
