import pygame
from settings import * 
from pathlib import Path

# class to represent an individual tile object 

class Wall(pygame.sprite.Sprite):
    def __init__(self,pos,groups):
        super().__init__(groups)
        
        # src\sprites\env\wall.png
        folder = Path("sprites\env")
        file = folder / "wall.png"
        
        self.image = pygame.image.load("sprites\env\wall.png")
       
        self.rect = self.image.get_rect(topleft = pos)
        self.hitbox = self.rect.inflate(0,-10)
        
    