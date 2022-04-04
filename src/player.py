
import pygame
from settings import *

# class to represent the human controller player
class Player(pygame.sprite.Sprite):
    def __init__(self,pos,groups,obstacle_sprites):
        super().__init__(groups) 
        
        # init human controlled player      
        # load sprite sheet
        self.image = pygame.image.load('src/sprites/player.png')
        self.rect = self.image.get_rect(topleft = pos)
        self.hitbox = self.rect.inflate(0,-26)
        
        self.direction = pygame.math.Vector2();
        self.speed = 5;
        
        self.obstacles_sprites = obstacle_sprites
        
    # handle user input with the arrow keys
    def input(self):
        keys = pygame.key.get_pressed()
        
        # y axis
        #moving up
        if keys[pygame.K_UP]:
            self.direction.y = -1;
            self.image = pygame.image.load('src/sprites/wooden.png')
            
        #moving down
        elif keys[pygame.K_DOWN]:
            self.direction.y = 1;
            self.image = pygame.image.load('src/sprites/player.png')
        
        # no movement
        else:
            self.direction.y = 0;
        
        # x axis 
        #moving right:
        if keys[pygame.K_RIGHT]:
            self.direction.x = 1;
               
        # moving left:    
        elif keys[pygame.K_LEFT]:
            self.direction.x = -1;
            
        # no movement    
        else:
            self.direction.x = 0;
            
        # using items 
        if keys[pygame.K_i]:
            self.use_item = True
        
        # attacks
        
        # TODO: how to handle which direction the player is attacking?
        # TODO: what if this is a ranged attack?
        # changing animations based on movement direction
        
        
        if keys[pygame.K_SPACE]:
            self.primary_attack = True;
            
        if keys[pygame.K_LSHIFT]:
            self.secondary_attack = True;
        
        
    # handling player movement across the map including physics
    def move(self,speed):
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize();
        
        self.hitbox.x += self.direction.x * speed
        self.collision('horizontal')
        self.hitbox.y += self.direction.y * speed
        self.collision('vertical')
        self.rect.center = self.hitbox.center;
        
            
    # collision handling             
    def collision(self,direction):
        # handle horizontal collisions
        if direction == 'horizontal':
            for sprite in self.obstacles_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.x > 0:
                        self.hitbox.right = sprite.hitbox.left
                    if self.direction.x < 0:
                        self.hitbox.left = sprite.hitbox.right
                        
        # handle vertical collisions
        if direction == 'vertical':
            for sprite in self.obstacles_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.y > 0:
                        self.hitbox.bottom = sprite.hitbox.top
                    if self.direction.y < 0:
                        self.hitbox.top = sprite.hitbox.bottom
                                   
    def update(self):
        self.input();
        self.move(self.speed)
            
        
    


