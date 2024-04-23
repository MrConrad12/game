import pygame
from animation import AnimatedCard
from const import *
from player_selection import SelectablePlayer
BUTTON_PATH = "assets/bouton/"

level_image = {
    'Whispering Woods':f'{BUTTON_PATH}panneau.png',
    'Coral Reef':f'{BUTTON_PATH}panneau.png',
    'Skyfall Peaks':f'{BUTTON_PATH}panneau.png',
    'Machine Room':f'{BUTTON_PATH}panneau.png',
    'Forgotten Tower':f'{BUTTON_PATH}panneau.png',
    'Rush mode':f'{BUTTON_PATH}panneau.png',
}
class MenuGame:
    def __init__(self, game):
        self.game = game
        self.level_selected = "Whispering Woods"

        self.play_button = self.draw_image_button(f'bouton.png')
        self.help_button = self.draw_image_button(f'help_button.png', offsetY = 80)
        self.exit_button = self.draw_image_button(f'exit_button.png', offsetY = 160)
        self.home_button = self.draw_image_button(f'home_button.png', posX = WIDTH - 60, posY= 60 )
        self.image = ImageWithText(self.game.screen,f'cadre.png', "Hello World", (SELECTABLE_PLAYER_POS_X,  SELECTABLE_PLAYER_POS_Y * 1.7), True, (250, 100))
        self.levels = self.load_level_boutton()
        self.change_right_player = AnimatedCard(self.game, f'{BUTTON_PATH}next_right.png', 80,posX=SELECTABLE_PLAYER_POS_X + 45, posY=SELECTABLE_PLAYER_POS_Y - 25)
        self.change_left_player = AnimatedCard(self.game, f'{BUTTON_PATH}next_left.png', 80,posX=SELECTABLE_PLAYER_POS_X - 160, posY=SELECTABLE_PLAYER_POS_Y - 25)
        self.player = SelectablePlayer(image="assets/selectable_player/player1")
        
    def load_level_boutton(self):
        levels = {}
        offsetX = 60
        offsetY = 60
        space = 20
        x_spacing = CARD_SIZE + space
        y_spacing = CARD_SIZE+ space
        for i,(level, image) in enumerate(level_image.items()):
            row = i // 3  
            col = i % 3  
            x = offsetX + (col * x_spacing)
            y = offsetY + (row * y_spacing)
            levels[level] = AnimatedCard(self.game, image, CARD_SIZE,posX=x, posY=y, offsetX=offsetX, offsetY=offsetY)
        return levels

    def draw_image_button(self, image_src, offsetX = 0, offsetY = 0, posX = WIDTH // 2, posY = HEIGHT //2):
        image = pygame.image.load(BUTTON_PATH+image_src)
        rect = image.get_rect()
        rect.centerx = posX + offsetX
        rect.centery = posY + offsetY
        return {'image':image, 'rect':rect}
     
    def draw_setting_menu(self):
        pass
    
    def draw_intro(self):
        pass

    def draw_welcome_page(self):
        background = pygame.image.load('assets/decoration/fond2.jpg')
        background = pygame.transform.scale(background, (WIDTH, HEIGHT *1.4))
        self.game.screen.blit(self.game.welcome_background, (0, -200))
        pygame.display.update()

    def draw_start_menu(self):
        self.game.screen.blit(self.game.background, (0, -200))
        self.game.screen.blit(self.play_button['image'], self.play_button['rect'])
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
        self.player.update()
        pygame.display.update()

    def handle_button_clicks(self, mouse_pos):
        """ gestion des clique de souris """
        if self.game.game_state == START_MENU:
            if self.play_button['rect'].collidepoint(mouse_pos):
                self.game.game_state = GAME
            elif self.help_button['rect'].collidepoint(mouse_pos):
                self.game.game_state = LEVEL
            elif self.exit_button['rect'].collidepoint(mouse_pos):
                self.game.running = False
        if self.home_button['rect'].collidepoint(mouse_pos):
            self.game.game_state = START_MENU
            
        # choisir le niveau
        self.chose_level(mouse_pos=mouse_pos)
        
    def chose_level(self, mouse_pos):
        for level, bouton in self.levels.items():
            if bouton.rect.collidepoint(mouse_pos):
                self.level_selected = level
class ImageWithText:
    def __init__(self, screen, image_path, text, position, resizing=False, size=(100,100), font_path=FONT_PATH, font_size=36):
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

        