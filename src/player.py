
import pygame
from settings import *

# class to represent the human controller player
class Player(pygame.sprite.Sprite):
    def __init__(self,pos,groups,obstacle_sprites):
        super().__init__(groups) 
        
        # load the tile map for the player here
        # to do add multiple directions for the player 
        
        self.image = pygame.image.load('player.png')
        self.rect = self.image.get_rect(topleft = pos)
        self.hitbox = self.rect.inflate(0,-26)
        
        self.direction = pygame.math.Vector2();
        self.speed = 4;
        
        self.obstacles_sprites = obstacle_sprites
        
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
            self.collision('horz')
            self.hitbox.y += self.direction.y * speed
            self.collision('vert')
            self.rect.center = self.hitbox.center;
            
            
             
    
    # collision handling             
        def collision(self,direction):
            # handle horizontal collisions
            if direction == 'horz':
                for spirte in self.obstacles_sprites:
                    if spirte.hitbox.colliderect(self.hitbox):
                        if self.direction.x > 0:
                            self.hitbox.right = sprite.hitbox.left
                        if self.direction.x < 0:
                            self.hitbox.left = sprite.hitbox.right
                            
            # handle vertical collisions
            if direction == 'vert':
                for sprite in self.obstacles_sprites:
                    if sprite.hitbox.colliderect(self.hitbox):
                        if self.direction.y > 0:
                            self.hitbox.bottom = sprite.hitbox.top
                        if self.direction.y < 0:
                            self.hitbox.top = sprite.hitbox.bottom
                        
                        
        def update(self):
            self.input();
            self.move(self.speed)
            
        
    


