
import pygame
from pygame.mixer import *
from const import BGM_PATH, EFFECT_SOUND

pygame.init()
class SoundManager:
    def __init__(self):
        pygame.mixer.init()
        self.sfx_volume  = 0.4
        self.music_volume  = 0.4
        self.sound_effects = self.load_sound_effects()    
        self.bgm_menu = f"{BGM_PATH}menu_01.ogg"
        self.bgm_game = f"{BGM_PATH}game_01.mp3"
        
        #initialise les librairies musicales
        pygame.mixer.init()
        
    def load_sound_effects(self):
        sound_effects = {
            "forward_effect": pygame.mixer.Sound(f"{EFFECT_SOUND}forward_effect.ogg"),
            "backward_effect": pygame.mixer.Sound(f"{EFFECT_SOUND}backward_effect.ogg"),
            "close_effect":pygame.mixer.Sound(f"{EFFECT_SOUND}close_effect.ogg"),
            "game_over_effect":pygame.mixer.Sound(f"{EFFECT_SOUND}game_over_effect.mp3"),
        }
        for sound, load in sound_effects.items:
            sound[load].set_volume(self.sfx_volume)
        return sound_effects
    
    def play_sound(self, music):
        self.sound_effects[music]
        
    def load_bgm_music(self):
        """charger la music de fond"""
        music.load(self.bgm_menu)
        pygame.mixer.music.set_volume(self.music_volume)
        
    def play_bgm(self):
        """jouer le son en arriere plan"""
        music.play(loops=0, fade_ms=1000)

    def cut_music(self):
        if(pygame.mixer.music.load != None):
            pygame.mixer.music.stop()
            pygame.mixer.music.unload()
        
