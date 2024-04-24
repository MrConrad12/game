             
import pygame
from const import FPS, WIDTH


class TimeManager:
    def __init__(self, x = WIDTH // 2, y = 10):
        self.timer = 60000
        self.timer_render_rect = None
        self.timer_pos_x = x
        self.timer_pos_y = y
        self.timer_render = None
        self.font = pygame.font.Font(None, 27)

    def update_timer(self):
        """actualise le timer et l'affiche"""
        self.timer_render = self.font.render(f"{self.timer / 1000:.2f}", True, (0,0,0))
        self.timer_render_rect = self.timer_render.get_rect(center=(self.timer_pos_x, self.timer_pos_y))
        self.timer -= FPS % 60
        print(self.timer)
    def reset_timer(self, value = 60000):
        self.timer = value
        
import pygame

class GameTimer:
    def __init__(self, duration_seconds):
        self.duration_seconds = duration_seconds
        self.current_seconds = duration_seconds * FPS  # Convertir en nombre de frames
        self.finished = False
        self.font = pygame.font.Font(None, 48)
    
    def update(self):
        if not self.finished:
            self.current_seconds -= 1
            if self.current_seconds <= 0:
                self.current_seconds = 0
                self.finished = True
    
    def get_time_string(self):
        minutes = self.current_seconds // (FPS * 60)
        seconds = (self.current_seconds // FPS) % 60
        return f"{minutes:02}:{seconds:02}"
    
    def draw(self, screen, position):
        time_text = self.font.render(self.get_time_string(), True, (255, 255, 255))  # Couleur blanche
        time_rect = time_text.get_rect(center=position)
        screen.blit(time_text, time_rect)
    def reset(self):
        self.current_seconds = self.duration_seconds