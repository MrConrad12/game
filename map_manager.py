import sys
import pygame
import pytmx
import pyscroll
from const import *
from player import Player

class MapManager:
    def __init__(self, game, map_game='map', path_map= 'map/air_map/air_map.tmx'):
        self.map = map_game
        self.map_path = path_map
        self.map_zoom = 1.5
        
        self.game = game
        self.player = None
        self.enemies = []
        
        self.group = None
        self.collisions = []
        self.void = []
        self.tmx_data = None
        
    def load_map(self, map_game, path_map):
        # load map
        self.map = map_game
        self.map_path = path_map
        self.tmx_data = pytmx.util_pygame.load_pygame(self.map_path)
        map_data = pyscroll.data.TiledMapData(self.tmx_data)
        map_layer = pyscroll.orthographic.BufferedRenderer(map_data,(WIDTH, HEIGHT))
        map_layer.zoom = self.map_zoom
        
        self.load_map_element()
        
        # charger le joueur sur la map
        player_pos = self.tmx_data.get_object_by_name('player')
        self.player = Player(self, player_pos.x, player_pos.y)
        
        # charger les enemies sur la map
        self.group = pyscroll.PyscrollGroup(map_layer=map_layer, default_layer=5)
        self.group.add(self.player)
        
    def load_map_element(self):
        # receive collisions
        self.load_element("collisions", self.collisions)
        self.load_element("void", self.void)
            
    def load_element(self, type, element_liste):
        for obj in self.tmx_data.objects:
            if obj.type == type:
                element_liste.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))
    
    def update(self):
        self.group.update()
        for sprite in self.group.sprites():
            sprite.rect.topleft = sprite.position

            if sprite.feet.collidelist(self.collisions) > -1:
                sprite.hits = True
                
                sprite.touch_ground()
            else:
                sprite.hits = False
        self.group.center(self.player.rect.center)
        self.group.draw(self.game.screen)
