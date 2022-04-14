import pygame
from settings import *

class Arrow(pygame.sprite.Sprite):
    def __init__(self,groups, player, direction, position):
        super().__init__(groups)
    
        self.direction = direction
        
        #self.image 
        
    
    
    def update(self):
        if self.direction == 'left': 
            self.rect.x -= 5;
            
        if self.direction == 'right': 
            self.rect.x += 5;
        
        if self.direction == 'down': 
            self.rect.y += 5;
        
        if self.direction == 'up': 
            self.rect.y -= 5;
        
        
        # update veloicty direction and direction
        if self.rect.x >= window_height + 100:
            self.kill()
        
        
        elif self.rect.x >= window_width + 100:
            self.kill();
        
            
        elif self.rect.x >= window_width + 100:
            self.kill();