import pygame
from animation import AnimatedButton, AnimatedCard
from const import *
from map_manager import MapManager
from player_selection import SelectablePlayer
BUTTON_PATH = "assets/bouton/"

level_image = {
    'Whispering Woods':f'{BUTTON_PATH}5.png',
    'Coral Reef':f'{BUTTON_PATH}3.png',
    'Skyfall Peaks':f'{BUTTON_PATH}4.png',
    'Machine Room':f'{BUTTON_PATH}2.png',
    'Forgotten Tower':f'{BUTTON_PATH}1.png',
    'Rush mode':f'{BUTTON_PATH}6.png',
}
class MenuGame:
    def __init__(self, game):
        self.game = game
        self.level_selected = "Whispering Woods"
        player = game.current_map.player
        
        # bouton pour le menu prinipale
        self.start_button = self.draw_image_button(f'bouton.png')
        self.help_button = self.draw_image_button(f'help_button.png', offsetY = 80)
        self.exit_button = self.draw_image_button(f'exit_button.png', offsetY = 160)
        self.home_button = self.draw_image_button(f'home_button.png', posX = WIDTH - 60, posY= 60 )
        
        # bouton pour les niveaux
        self.levels = self.load_level_boutton()
        self.play_button = AnimatedButton(self.game, f'{BUTTON_PATH}cadre.png', width = 80, height = 50, posY=HEIGHT - 120)
                
        # bouton pour le personnage
        self.change_right_player = AnimatedCard(self.game, f'{BUTTON_PATH}next_right.png', 80,posX=SELECTABLE_PLAYER_POS_X + 45, posY=SELECTABLE_PLAYER_POS_Y - 25, add_size=5)
        self.change_left_player = AnimatedCard(self.game, f'{BUTTON_PATH}next_left.png', 80,posX=SELECTABLE_PLAYER_POS_X - 160, posY=SELECTABLE_PLAYER_POS_Y - 25, add_size=5)
        
        # statistiques
        self.player_stat_data = [f"Live:  {player.lives}", f"Speed: {player.speed}", f"Damage: {player.damage}", f"+ {player.aptitude}"]
        self.player_stat = ImageWithTextGroup(self.game.screen, 'panneau0.png', self.player_stat_data,(SELECTABLE_PLAYER_POS_X,  SELECTABLE_PLAYER_POS_Y * 2.6), resizing=True, size=(220,200))
        self.image = ImageWithText(self.game.screen,'cadre.png', f"{player.name}", (SELECTABLE_PLAYER_POS_X,  SELECTABLE_PLAYER_POS_Y * 1.8), True, (200, 80), font_size=36)
        self.player = SelectablePlayer(image="assets/selectable_player/player1")
        
        self.chose = False
    def load_level_boutton(self):
        """charger les boutons de selection des niveaux"""
        levels = {}
        space = 10
        x_spacing = CARD_SIZE + space
        y_spacing = CARD_SIZE + space
        
        # gestion des espacement pour creer 2 lignes de 3 colonnes
        for i,(level, image) in enumerate(level_image.items()):
            row = i // 3  
            col = i % 3  
            x = (col * x_spacing) - 20
            y = (row * y_spacing) - 20
            levels[level] = AnimatedCard(self.game, image, CARD_SIZE,posX=x, posY=y, offsetX=0, offsetY=0)
        return levels

    def draw_image_button(self, image_src, offsetX = 0, offsetY = 0, posX = WIDTH // 2, posY = HEIGHT //2):
        image = pygame.image.load(BUTTON_PATH+image_src)
        rect = image.get_rect()
        rect.centerx = posX + offsetX
        rect.centery = posY + offsetY
        return {'image':image, 'rect':rect}
     
    def draw_setting_menu(self):
        pass

    def draw_welcome_page(self):
        background = pygame.image.load('assets/decoration/fond2.jpg')
        background = pygame.transform.scale(background, (WIDTH, HEIGHT *1.4))
        self.game.screen.blit(self.game.welcome_background, (0, -200))
        pygame.display.update()

    def draw_start_menu(self):
        self.game.screen.blit(self.game.background, (0, -200))
        self.game.screen.blit(self.start_button['image'], self.start_button['rect'])
        self.game.screen.blit(self.help_button['image'], self.help_button['rect'])
        self.game.screen.blit(self.exit_button['image'], self.exit_button['rect'])
        pygame.display.update()
   
    def draw_level_menu(self):
        self.game.screen.blit(self.game.background, (0, -200))
        for level in self.levels:
            self.levels[level].update()
        self.game.screen.blit(self.home_button['image'], self.home_button['rect'])
        self.game.screen.blit(self.home_button['image'], self.home_button['rect'])
        self.game.screen.blit(self.player.image, self.player.rect)
        self.change_right_player.update()
        self.change_left_player.update()
        self.image.draw()
        self.player_stat.draw()
        self.player.update()
        pygame.display.update()

    def handle_button_clicks(self, mouse_pos):
        """ gestion des clique de souris """
        if self.game.game_state == START_MENU:
            if self.start_button['rect'].collidepoint(mouse_pos):
                self.game.game_state = GAME
            elif self.help_button['rect'].collidepoint(mouse_pos):
                self.game.game_state = LEVEL
            elif self.exit_button['rect'].collidepoint(mouse_pos):
                self.game.running = False
        if self.home_button['rect'].collidepoint(mouse_pos):
            self.game.game_state = START_MENU
       
        
    def chose_level(self, mouse_pos):
        for level, bouton in self.levels.items():
            if bouton.rect.collidepoint(mouse_pos) and not self.chose:
                self.level_selected = level
                self.level[bouton].isSelected = True
                """self.game.current_map = MapManager(self.game)
                self.game.current_map.load_map( 'map', 'map/forest_map/forest_map.tmx')"""
            self.level[bouton].isSelected = False

class ImageWithText:
    def __init__(self, screen, image_path, text, position, resizing=False, size=(100,100), font_path=FONT_PATH, font_size=22):
        pygame.init()
        self.screen = screen
        self.image = pygame.image.load(BUTTON_PATH+image_path)
        if(resizing):
            self.image = pygame.transform.scale(self.image, size)
        self.image_rect = self.image.get_rect(center=position)
        self.font = pygame.font.Font(font_path, font_size)
        self.text_surface = self.font.render(text, True, (255, 255, 255))
        self.text_rect = self.text_surface.get_rect(center=self.image_rect.center)

    def draw(self):
        self.screen.blit(self.image, self.image_rect)
        self.screen.blit(self.text_surface, self.text_rect)

class ImageWithTextGroup:
    def __init__(self, screen, image_path, text_lines, position,resizing=False, size=(100,100), font_path=FONT_PATH, font_size=28, font_color=(255, 255, 255)):
        pygame.init()

        self.image = pygame.image.load(BUTTON_PATH+image_path)
        if(resizing):
            self.image = pygame.transform.scale(self.image, size)
        self.image_rect = self.image.get_rect(center=position)
        self.screen = screen
        self.font = pygame.font.Font(font_path, font_size)

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

    def draw(self):
        # Dessiner l'image
        self.screen.blit(self.image, self.image_rect)

        # Dessiner les lignes de texte
        for surface, rect in zip(self.text_surfaces, self.text_rects):
            self.screen.blit(surface, rect.topleft)