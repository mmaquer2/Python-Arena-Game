import pygame
from settings import *

class Arrow(pygame.sprite.Sprite):
    def __init__(self,groups, player, direction):
        super().__init__(groups)
    
        self.direction = direction
        self.player = player
        
        arrow_path = f'sprites/weapons/arrow/{direction}.png' # path to the graphic of the weapon
        self.image = pygame.image.load(arrow_path).convert_alpha()
        
        if self.direction == "right":
            self.rect = self.image.get_rect(midleft = self.player.rect.midright + pygame.math.Vector2(0,16))
        
        elif self.direction == "left":
            self.rect = self.image.get_rect(midright = player.rect.midleft + pygame.math.Vector2(0,16)) 
        
        elif direction == 'down':
            self.rect = self.image.get_rect(midtop = player.rect.midbottom + pygame.math.Vector2(-10,0)) 
        
        elif direction == 'up': 
            self.rect = self.image.get_rect(midbottom = player.rect.midtop + pygame.math.Vector2(0,16)) 
            
    def update(self):
        
        # update veloicty direction and direction
        if self.direction == 'left': 
            self.rect.x -= 5;
            
        if self.direction == 'right': 
            self.rect.x += 5;
        
        if self.direction == 'down': 
            self.rect.y += 5;
        
        if self.direction == 'up': 
            self.rect.y -= 5;
        
        
        # once the arrow moves far outside of the 
        if self.rect.x >= window_height + 100:
            self.kill()
        
        elif self.rect.x >= window_width + 100:
            self.kill()
        
            
        elif self.rect.x >= window_width + 100:
            self.kill()