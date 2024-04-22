import pygame
from animation import AnimatedButton
from const import *
from player_selection import SelectablePlayer
level_image = {
    'Whispering Woods':'assets/panneau2.jpg',
    'Coral Reef':'assets/panneau2.jpg',
    'Skyfall Peaks':'assets/panneau2.jpg',
    'Machine Room':'assets/panneau2.jpg',
    'Forgotten Tower':'assets/panneau2.jpg',
    'Rush mode':'assets/panneau2.jpg',
}
class MenuGame:
    def __init__(self, game):
        self.game = game
        self.play_button = self.draw_image_button('assets/bouton.png')
        self.help_button = self.draw_image_button('assets/help_button.png', offsetY = 80)
        self.exit_button = self.draw_image_button('assets/exit_button.png', offsetY = 160)
        self.home_button = self.draw_image_button('assets/home_button.png', posX = WIDTH - 60, posY= 60 )

        self.levels = self.load_level()
        self.player = SelectablePlayer()
        
    def load_level(self):
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
            levels[level] = AnimatedButton(self.game, image, posX=x, posY=y, offsetX=offsetX, offsetY=offsetY)
        return levels

    def draw_image_button(self, image_src, offsetX = 0, offsetY = 0, posX = WIDTH // 2, posY = HEIGHT //2):
        image = pygame.image.load(image_src)
        rect = image.get_rect()
        print(rect)
        rect.centerx = posX + offsetX
        rect.centery = posY + offsetY
        return {'image':image, 'rect':rect}

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
        
    def draw_setting_menu():
        pass

    def draw_level_menu(self):
        self.game.screen.blit(self.game.background, (0, -200))
        for level in self.levels:
            self.levels[level].update()
        self.game.screen.blit(self.home_button['image'], self.home_button['rect'])
        self.game.screen.blit(self.home_button['image'], self.home_button['rect'])
        self.game.screen.blit(self.player.image, self.player.rect)
        self.player.update()
        pygame.display.update()

    def handle_button_clicks(self, mouse_pos):
        if self.game.game_state == START_MENU:
            if self.play_button['rect'].collidepoint(mouse_pos):
                self.game.game_state = GAME
            elif self.help_button['rect'].collidepoint(mouse_pos):
                self.game.game_state = LEVEL
            elif self.exit_button['rect'].collidepoint(mouse_pos):
                self.game.running = False
   
        if self.home_button['rect'].collidepoint(mouse_pos):
            self.game.game_state = START_MENU
        
        # choose level
        
    def chose_level(self, mouse_pos):
        for level, bouton in self.levels.items():
            if bouton['rect'].collidepoint(mouse_pos):
                print(level)
