import pygame
from settings import *


class Enemy_C(pygame.sprite.Sprite):
    def __init__(self,pos,groups,obstacle_sprites,create_attack,destroy_attack):
        
        self.id = '4'
        self.sprite_type = "cpu_ai"    
        
        idle_down_folder = Path('sprites/characters/cpu_c/down_idle/idle_down.png')
        self.image_import = pygame.image.load(idle_down_folder) # import image 
        self.image = pygame.transform.scale(self.image_import,(64,64));   # scale sprite sheet