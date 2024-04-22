import sys
import pygame
import pytmx
import pyscroll
from const import *
from player import Player
class MapManager:
    def __init__(self, game, map_game='map', path_map= '../map/forest_map.tmx'):
        self.map = map_game
        self.map_path = path_map
        self.map_zoom = 1.5
        self.game = game
        self.walls = []
        self.enemies = []
        self.group = None
        self.tmx_data = None
        
    def load_map(self, map_game, path_map):
        # load map
        self.map = map_game
        self.map_path = path_map
        self.tmx_data = pytmx.util_pygame.load_pygame(self.map_path)
        map_data = pyscroll.data.TiledMapData(self.tmx_data)
        map_layer = pyscroll.orthographic.BufferedRenderer(map_data, self.game.screen.get_size())
        map_layer.zoom = self.map_zoom
        
        self.load_map_element()
        
        player_pos = self.tmx_data.get_object_by_name('player')
        self.game.player = Player(self, player_pos.x, player_pos.y)
        
        self.group = pyscroll.PyscrollGroup(map_layer=map_layer, default_layer=5)
        self.group.add(self.game.player)
        
    def load_map_element(self):
         # receive collision
        for obj in self.tmx_data.objects:
            if obj.type == 'collision':
                self.walls.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))
                
            # add after enemy manager
            """
            if obj.type == 'enemy':
                self.enemies.append(None)
                
            if obje
            """
    def update(self):
        self.group.update()
        for sprite in self.group.sprites():
            if sprite.feet.collidelist(self.walls) > -1:
                sprite.hits = True
                sprite.touch_ground()
            else:
                sprite.hits = False
        self.group.center(self.game.player.rect.center)
        self.group.draw(self.game.screen)
