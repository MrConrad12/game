import sys
import pygame
import pytmx
import pyscroll
from const import *
from player import Player
from ecran import MenuGame

class Game:
    def __init__(self):
        pygame.init()
        self.background = pygame.image.load('assets/decoration/fond.jpg')

        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Game")
        self.clock = pygame.time.Clock()
        self.game_state = START_MENU

        # Load map
        tmx_data = pytmx.util_pygame.load_pygame('../map/forest_map.tmx')
        map_data = pyscroll.data.TiledMapData(tmx_data)
        map_layer = pyscroll.orthographic.BufferedRenderer(map_data, self.screen.get_size())
        map_layer.zoom = 1

        # List of collision rectangles
        self.walls = []
        for obj in tmx_data.objects:
            if obj.type == 'ground':
                self.walls.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))

        self.group = pyscroll.PyscrollGroup(map_layer=map_layer, default_layer=9)
        player_pos = tmx_data.get_object_by_name('player')

        self.player = Player(self, player_pos.x, player_pos.y)
        self.group.add(self.player)

        self.menu = MenuGame(self)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self.menu.handle_button_clicks(mouse_pos)
            if event.type == pygame.KEYDOWN:
                self.handle_key_presses(event)

    def handle_key_presses(self, event):
        if self.game_state == GAME:
            if event.key == pygame.K_SPACE:
                self.player.jump()
            if event.key == pygame.K_LSHIFT or event.key == pygame.K_RSHIFT:
                self.player.double_jump = True

    def update_and_draw_game(self):
        self.group.update()

        # Collision detection
        for sprite in self.group.sprites():
            if sprite.feet.collidelist(self.walls) > -1:
                sprite.hits = True
                sprite.touch_ground()
            else:
                sprite.hits = False
        self.group.center(self.player.rect.center)
        self.group.draw(self.screen)

        if self.game_state == GAME:
            self.screen.blit(self.menu.back_button_image, self.menu.back_button_rect)

        pygame.display.update()
        self.clock.tick(FPS)

    def run(self):
        self.running = True
        while self.running:
            if self.game_state == START_MENU:
                self.menu.draw_start_menu()
            elif self.game_state == GAME:
                self.update_and_draw_game()
            self.handle_events()
        pygame.quit()

if __name__ == "__main__":
    game = Game()
    game.run()
