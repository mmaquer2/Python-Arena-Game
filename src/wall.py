import pygame
from settings import * 
from pathlib import Path

# class to represent an individual tile object 
class Wall(pygame.sprite.Sprite):
    def __init__(self,pos,groups):
        super().__init__(groups)
        folder = Path("sprites/env/rock.png")
        self.image = pygame.image.load(folder)
        self.rect = self.image.get_rect(topleft = pos)
        self.hitbox = self.rect.inflate(0,-10)
        
    