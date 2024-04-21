import pygame
import math

def cubic_bezier_ease_in(t):
    P0 = (0, 0)
    P1 = (0.42, 0)
    P2 = (1, 1)
    P3 = (1, 1)
    t *= 2 * math.pi 
    x = P0[0] + t * (P1[0] - P0[0]) + math.pow(t, 2) * (2 * P2[0] - 2 * P1[0]) + math.pow(t, 3) * (P3[0] - 3 * P2[0] + 3 * P1[0] - P0[0])
    #y = P0[1] + t * (P1[1] - P0[1]) + math.pow(t, 2) * (2 * P2[1] - 2 * P1[1]) + math.pow(t, 3) * (P3[1] - 3 * P2[1] + 3 * P1[1] - P0[1])
    return x if math.sin(t) > 0 else 1 - x

class Animation:
    def __init__(self, name, states, inital_state, animation_speed = 1, sprite_size = (64,64)):
        self.states = states
        self.path = f'assets/{name}/{name}'
        self.animation_speed = animation_speed
        self.sprite_size = sprite_size
        self.sprite_dic = self.load_image()
        
        self.image = self.sprite_dic[inital_state][0]
        self.current_sprite = 0
        self.sprite_counter = 0
    def load_image(self):
        sprite_dic = {}
        for state in self.states:
            for side in ['left', 'right']:
                sprite_dic[state + '_' + side] = self.load_sprites(self.path +  '_' + state + '_' + side)
        return sprite_dic
    
    def load_sprites(self, sprite_type, sprite_size=(32, 32)):
        img = pygame.image.load(f'{sprite_type}.png')
        sprites = []
        for i in range(img.get_width() // sprite_size[0]):
            for j in range(img.get_height() // sprite_size[1]):
                sprite = pygame.Surface(sprite_size)
                sprite.blit(img, (0, 0), (i * sprite_size[0], j * sprite_size[1], sprite_size[0], sprite_size[1]))
                sprite = pygame.transform.scale(sprite, self.sprite_size)
                sprite.set_colorkey((0, 0, 0))
                sprites.append(sprite)
        return sprites
    def animate(self, state):
        self.sprite_counter += self.animation_speed 
        if self.sprite_counter >= 10:
            self.current_sprite += 1
            if self.current_sprite >= len(self.get_sprites(state)):
                self.current_sprite = 0
            self.image = self.get_sprites(state)[self.current_sprite]
            self.sprite_counter = 0
        return self.image
    def get_sprites(self, state):
        return self.sprite_dic[state]
    
    