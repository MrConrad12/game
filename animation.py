import pygame

from const import CARD_SIZE, HEIGHT, WIDTH

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


class AnimatedCard:
    def __init__(self, game, image_path, initial_size = CARD_SIZE, add_size = 20, offsetX=10, offsetY=10, posX = WIDTH // 2, posY = HEIGHT //2):
        self.game = game
        self.original_image = pygame.image.load(image_path)
        self.image = self.original_image.copy()
        self.initial_size = initial_size
        self.final_size = initial_size + add_size
        self.current_size = initial_size
        self.animation_speed = 3
        self.rect = self.image.get_rect()
        self.rect.topleft = (posX + offsetX, posY + offsetY)
        self.isSelected = False

    def update(self):
        # Animer le changement de taille
        if not self.isSelected:
            if self.rect.collidepoint(pygame.mouse.get_pos()):
                if self.current_size < self.final_size:
                    self.current_size += self.animation_speed
            else:
                if self.current_size > self.initial_size:
                    self.current_size -= self.animation_speed
        else:
            self.current_size = self.final_size

        # Redimensionner l'image
        self.image = pygame.transform.scale(self.original_image, (self.current_size, self.current_size))
        self.rect = self.image.get_rect(center=self.rect.center)
        self.game.screen.blit(self.image, self.rect)

class AnimatedButton:
    def __init__(self, game, image_path, width, height, add_size=20, offsetX=50, offsetY=50, posX=WIDTH // 2, posY=HEIGHT // 2):
        self.game = game
        self.isSelected = False
        self.original_image = pygame.image.load(image_path)
        self.image = self.original_image.copy()  
        self.width = width
        self.height = height
        self.add_size = add_size
        self.animation_speed = 3 
        self.rect = self.image.get_rect()
        self.rect.topleft = (posX + offsetX, posY + offsetY)

    def update(self):
        # Animer le changement de taille
        if not self.isSelected:
            if self.rect.collidepoint(pygame.mouse.get_pos()):
                if self.rect.width < self.width + self.add_size:
                    self.rect.width += self.animation_speed
                    self.rect.height += self.animation_speed * (self.height / self.width)  
            else:
                if self.rect.width > self.width:
                    self.rect.width -= self.animation_speed
                    self.rect.height -= self.animation_speed * (self.height / self.width)             

        # Redimensionner l'image
        self.image = pygame.transform.scale(self.original_image, (self.rect.width, self.rect.height))
        self.rect = self.image.get_rect(center=self.rect.center)
        self.game.screen.blit(self.image, self.rect)
