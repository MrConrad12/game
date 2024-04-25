
import pygame
from pygame.mixer import *
from const import BGM_PATH, EFFECT_SOUND

pygame.init()
class AudioManager:
    def __init__(self, game):
        pygame.mixer.init()
        self.sfx_volume  = 0.4
        self.music_volume  = 0.4
        self.bgm_menu = f"{BGM_PATH}menu_01.ogg"
        self.bgm_game = f"{BGM_PATH}game_01.mp3"
        
        self.sound_effects = self.load_sound_effects()    

        
        
    def load_sound_effects(self):
        
        sound_effects = {
            "forward_effect": pygame.mixer.Sound(f"{EFFECT_SOUND}forward_effect.ogg"),
            "backward_effect": pygame.mixer.Sound(f"{EFFECT_SOUND}backward_effect.ogg"),
            "close_effect":pygame.mixer.Sound(f"{EFFECT_SOUND}close_effect.ogg"),
            "game_over_effect":pygame.mixer.Sound(f"{EFFECT_SOUND}game_over_effect.mp3"),
        }
        for sound, effect in sound_effects.items():
            effect.set_volume(self.sfx_volume)
            sound_effects[sound] = effect
        return sound_effects
    
    def play_sound(self, music):
        self.sound_effects[music].play()
        
    def load_bgm_menu(self):
        """charger la music de fond"""
        music.load(self.bgm_menu)
        pygame.mixer.music.set_volume(self.music_volume)
        music.play(loops=-1, fade_ms=1000)
        
    def load_bgm_game(self):
        """charger la music de fond"""
        music.load(self.bgm_game)
        pygame.mixer.music.set_volume(self.music_volume)
        music.play(loops=-1, fade_ms=1000)
        
        
    def play_bgm(self):
        """jouer le son en arriere plan"""
        music.play(loops=0, fade_ms=1000)

    def cut_music(self):
        if(pygame.mixer.music.load != None):
            pygame.mixer.music.stop()
            pygame.mixer.music.unload()
        
