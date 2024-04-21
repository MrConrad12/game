import sys
import pygame
import pytmx
import pyscroll
from const import *
from player import Player
from screen import MenuGame
class MapManager:
    
    def __init__(self, game):
        self.map = 'map'
        self.mad_path = ''
        
    def load_map(self):
        tmx_data = pytmx.util_pygame.load_pygame(self.mad_path)
        map_data = pyscroll.data.TiledMapData(tmx_data)
        map_layer = pyscroll.orthographic.BufferedRenderer(map_data, self.screen.get_size())
        map_layer.zoom = 2
        self.walls = []
        for obj in tmx_data.objects:
            if obj.type == 'collision':
                self.walls.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))

        self.group = pyscroll.PyscrollGroup(map_layer=map_layer, default_layer=5)
        self.group.add(self.game.player)
