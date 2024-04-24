
import pygame

from const import BUTTON_PATH, FONT_PATH


class ImageWithText:
    def __init__(self, screen, image_path, text, position, resizing=False, size=(100,100), font_path=FONT_PATH, font_size=22):
        pygame.init()
        self.screen = screen
        self.image = pygame.image.load(BUTTON_PATH+image_path)
        if(resizing):
            self.image = pygame.transform.scale(self.image, size)
        self.rect = self.image.get_rect(center=position)
        self.font = pygame.font.Font(font_path, font_size)
        self.text_surface = self.font.render(text, True, (255, 255, 255))
        self.text_rect = self.text_surface.get_rect(center=self.rect.center)

    def draw(self):
        self.screen.blit(self.image, self.rect)
        self.screen.blit(self.text_surface, self.text_rect)

class ImageWithTextGroup:
    def __init__(self, screen, image_path, text_lines, position,resizing=False, size=(100,100), font_path=FONT_PATH, font_size=28, font_color=(255, 255, 255)):
        pygame.init()

        self.image = pygame.image.load(BUTTON_PATH+image_path)
        if(resizing):
            self.image = pygame.transform.scale(self.image, size)
        self.rect = self.image.get_rect(center=position)
        self.screen = screen
        self.font = pygame.font.Font(font_path, font_size)

        # Préparer les lignes de texte
        self.text_surfaces = []
        self.text_rects = []
        max_width = 0
        total_height = 0
        for line in text_lines:
            text_surface = self.font.render(line, True, font_color)
            text_rect = text_surface.get_rect()
            self.text_surfaces.append(text_surface)
            self.text_rects.append(text_rect)
            total_height += text_rect.height
            if text_rect.width > max_width:
                max_width = text_rect.width

        # Positionner les textes
        y_offset = self.rect.centery - total_height / 2
        for surface, rect in zip(self.text_surfaces, self.text_rects):
            rect.centerx = self.rect.centerx
            rect.top = y_offset
            y_offset += rect.height

        # Centrer le groupe de texte par rapport à l'image
        text_group_rect = pygame.Rect(0, 0, max_width, total_height)
        text_group_rect.center = self.rect.center
        for rect in self.text_rects:
            rect.centerx = text_group_rect.centerx

    def draw(self):
        # Dessiner l'image
        self.screen.blit(self.image, self.rect)

        # Dessiner les lignes de texte
        for surface, rect in zip(self.text_surfaces, self.text_rects):
            self.screen.blit(surface, rect.topleft)