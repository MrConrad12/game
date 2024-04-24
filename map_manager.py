import sys
import pygame
import pytmx
import pyscroll
from const import *
from enemy import Enemy
from player import Player
from timer_manager import GameTimer, TimeManager

class MapManager:
    def __init__(self, game, map_game='map', path_map= 'map/forest_map/forest_map.tmx'):
        self.map = map_game
        self.map_path = path_map
        self.map_zoom = 1
        
        self.game = game
        self.player = None
        self.enemies = pygame.sprite.Group()
        
        self.group = None
        self.collisions = pygame.sprite.Group()
        self.void = pygame.sprite.Group()
        self.finish = pygame.sprite.Group()
        self.tmx_data = None
        self.timer=None

    def load_map(self, map_game, path_map):
        # load map
        self.map = map_game
        self.map_path = path_map
        self.timer = GameTimer(2*100)
        
        self.tmx_data = pytmx.util_pygame.load_pygame(self.map_path)
        map_data = pyscroll.data.TiledMapData(self.tmx_data)
        map_layer = pyscroll.orthographic.BufferedRenderer(map_data,(WIDTH, HEIGHT))
        self.group = pyscroll.PyscrollGroup(map_layer=map_layer, default_layer=9)
        map_layer.zoom = self.map_zoom
        
        self.load_map_element()
        
        # charger le joueur sur la map
        player_pos = self.tmx_data.get_object_by_name('player')
        
        self.player = Player(self, player_pos.x, player_pos.y)
        self.player.obstacles = self.collisions.copy()
        self.player.void = self.void.copy()
        self.player.finish = self.finish.copy()
        
        ## add player
        for obj in self.tmx_data.objects:
            if obj.type == 'enemy':
                enemy = Enemy(self.game, self.player, obj.x, obj.y)
                self.enemies.add(enemy)
                enemy.obstacles = self.collisions.copy()
                self.group.add(enemy)

        self.group.add(self.player)
        
    def load_map_element(self):
        # recoit les collision
        self.load_element("collision", self.collisions)
        self.load_element("void", self.void)
        self.load_element("finish", self.finish)
        
    
    def load_element(self, type, element_liste):
        for obj in self.tmx_data.objects:
            if obj.type == type:
                obstacle = pygame.sprite.Sprite() 
                obstacle.rect = pygame.Rect(obj.x, obj.y, obj.width, obj.height)  # Définir le rectangle de collision
                element_liste.add(obstacle) 
    def update(self):
        self.timer.update()
        self.timer.draw(self.game.screen, (WIDTH // 2, 30))  
        self.group.update()
        self.group.center(self.player.rect.center)
        self.group.draw(self.game.screen)
        
        if pygame.sprite.spritecollideany(self.player, self.enemies) or pygame.sprite.spritecollideany(self.player, self.void):
            self.game.win = False
            self.game.game_state = START_MENU
        if pygame.sprite.spritecollideany(self.player, self.finish):
            self.game.win = True
            self.game.game_state = START_MENU

