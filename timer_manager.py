             
import pygame
from const import FPS, WIDTH


class Timer:
    def __init__(self, x = WIDTH // 2, y = 10):
        self.timer = 60000
        self.timer_render_rect = None
        self.timer_pos_x = x
        self.timer_pos_y = y
        self.font = pygame.font.Font(None, 27)

    def update_timer(self):
        """actualise le timer et l'affiche"""
        timer_render = self.font.render(f"{self.timer / 1000:.2f}", True, (0,0,0))
        self.timer_render_rect = timer_render.get_rect(center=(self.timer_pos_x, self.timer_pos_y))
        self.timer -= FPS % 60
    
    def reset_timer(self, value = 60000):
        self.timer = value