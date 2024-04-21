import pygame


class Animation:
    def __init__(self, path, states, inital_state):
        self.states = states
        self.path = path
        self.animation_speed = 1
        self.sprite_dic = self.load_image()
        self.image = self.sprite_dic[inital_state][0]
        self.current_sprite = 0
        self.sprite_counter = 0
    def load_image(self):
        sprite_dic = {}
        for (state, image) in self.states.items():
            for side in ['left', 'right']:
                sprite_dic[state + '_' + side] = self.load_sprites(self.path + image + '_' + side)
        return sprite_dic
    
    def load_sprites(self, sprite_type, sprite_size=(32, 32)):
        img = pygame.image.load(f'{sprite_type}.png')
        sprites = []
        for i in range(img.get_width() // sprite_size[0]):
            for j in range(img.get_height() // sprite_size[1]):
                sprite = pygame.Surface(sprite_size)
                sprite.blit(img, (0, 0), (i * sprite_size[0], j * sprite_size[1], sprite_size[0], sprite_size[1]))
                sprite = pygame.transform.scale(sprite, (64, 64))
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
    
    