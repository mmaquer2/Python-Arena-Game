
import pygame
from settings import *

# class to represent the human controller player
class Player(pygame.spirte.Sprite):
    def __init__(self,pos,groups,obstacles):
        super().__init__(groups) 
        
        # load the tile map for the player here
        # to do add multiple directions for the player 
        
        self.image = pygame.image.load('player.png')
        self.rect = self.image.get_rect(topleft = pos)
        self.hitbox = self.rect.inflate(0,-26)
        
        self.direction = pygame.math.Vector2();
        self.speed = 4;
        
        self.obstacles = obstacles 
        
    # handle user input with the arrow keys
        def userInput(self):
            keys = pygame.key.get_pressed()
            if keys[pygame.K_UP]:
                self.direction.y = -1;
            elif keys[pygame.K_DOWN]:
                self.direction.y = 1;
            else:
                self.direction.y = 0;
            
            if keys[pygame.K_RIGHT]:
                self.direction.x = 1;
            elif keys[pygame.K_LEFT]:
                self.direction.x = -1;
            else:
                self.direction.x = 0;

    # handling player movement across the map including physics
        def move(self,speed):
            if self.direction.magnitude() != 0:
                self.direction = self.direction.normalize();
            
            self.hitbox.x += self.direction.x * speed
            
            
             
    
    # collision handling             
        def collision(self,direction):
            if direction == 'hor'
        
        
        def update(self):
            self.input();
            self.move(self.speed)
            
        
    


