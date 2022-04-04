import pygame
from settings import * 

# class to represent an individual tile object 

class Tile(pygame.sprite.Sprite):
    def __init__(self,pos,groups):
        super().__init__(groups)
        self.image = pygame.image.load("rock.png").convert_alpha()
        self.rect = self.image.get_rect(topLeft = pos)
        self.hitbox = self.rect.inflate(0,-10)
    