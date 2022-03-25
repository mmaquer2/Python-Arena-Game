
import pygame
from settings import *

class Level:
    
    def __init__(self):

        
        # create game sprites
        self.display_surface = pygame.display.get_surface();
        self.visible_sprites = pygame.sprite.Group();
        self.obstacle_sprites = pygame.sprite.Group();
        
        #create map()
    
    def createMap(self):
        for row_ind,row in enumerate(levelMap):
            for col_ind, col in enumerate(row):
                x = col_ind * tileSize;
                y = row_ind * tileSize
                
                
                

    def run(self):
        pass