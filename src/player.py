
import pygame, sys
from pathlib import Path
from settings import *

# class to represent the human controller player
class Player(pygame.sprite.Sprite):
    
      # init human controlled player      
    def __init__(self,pos,groups,obstacle_sprites):
        
        super().__init__(groups) 
        
        # load player sprite sheet
       
        idle_down_folder = Path('sprites/characters/player/down_idle/idle_down.png')
        
        # import image 
        self.image_import = pygame.image.load(idle_down_folder)
        
        # scale sprite sheet
        self.image = pygame.transform.scale(self.image_import,(64,64));   
        self.rect = self.image.get_rect(topleft = pos)
        self.hitbox = self.rect.inflate(0,-5);
        
        # import sprite sheets for different actions
        
        idle_up_folder = Path('sprites/characters/player/up_idle')
        idle_down_folder = Path('sprites/characters/player/down_idle')
        idle_right_folder = Path('sprites/characters/player/right_idle')
        idle_left_folder = Path('sprites/characters/player/left_idle')
        
        
        move_down_folder = Path('sprites/characters/player/down')
        move_up_folder = Path('sprites/characters/player/up')
        move_right_folder = Path('sprites/characters/player/right')
        move_left_folder = Path('sprites/characters/player/left')
        
        attack_down_folder = Path('sprites/characters/player/down_attack')
        attack_up_folder = Path('sprites/characters/player/up_attack')
        attack_right_folder = Path('sprites/characters/player/right_attack')
        attack_left_folder = Path('sprites/characters/player/left_attack')
        
        block_down_folder = Path('sprites/characters/player/block_down')
        block_up_folder = Path('sprites/characters/player/block_up.png')
        block_right_folder = Path('sprites/characters/player/block_right')
        block_left_folder = Path('sprites/characters/player/block_left')
        
        idleRight = []
        idleLeft = []
        idleUp = []
        idleDown = []
        
        walkRight = []
        walkLeft = []
        walkUp = []
        walkDown = []
        
        attackUp = []
        attackDown = []
        attackRight = []
        attackLeft = []
        
        blockUp = []
        blockDown = []
        blockRight = []
        blockLeft = []
        
        player_death = []
        
        
        self.animations = {
            'up': [], 'down': [], 'left': [], 'right': [], 
            'up_idle': [], 'down_idle': [], 'left_idle': [], 'right_idle': [], 
            'up_block': [], 'down_block': [], 'left_block': [], 'right_block': [], 
            'up_attack': [], 'down_attack': [], 'left_attack': [], 'right_attack': [], 
            
        }
        
        # player status 
        self.status = 'down'
        self.frame_index = 0;
        self.animation_speed = 0.15;
        
        
        # movement and attack vars
        self.direction = pygame.math.Vector2();
        self.speed = 5;
        
        # attacking and blocking
        self.attacking = False;
        self.attack_cooldown = 400;
        self.block_cooldown = 400;
        self.attack_time = None;
        
        self.obstacles_sprites = obstacle_sprites
            
    # handle user input with the arrow keys
    def input(self):
        keys = pygame.key.get_pressed()
        
        # y axis
        #moving up
        if keys[pygame.K_UP]:
            self.direction.y = -1;
            self.status = 'up'
            
        #moving down
        elif keys[pygame.K_DOWN]:
            self.direction.y = 1;
            self.status = 'down'
        
        # no movement
        else:
            self.direction.y = 0;
        
        # x axis 
        #moving right:
        if keys[pygame.K_RIGHT]:
            self.direction.x = 1;
            self.status = 'right'
               
        # moving left:    
        elif keys[pygame.K_LEFT]:
            self.direction.x = -1;
            self.status = 'left'
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
        
        
        if keys[pygame.K_SPACE] and not self.attacking:
            self.attack_time = pygame.time.get_ticks();
            self.primary_attack = True;
            self.attacking = True;
            print("player is attacking w/ prim")
            
        if keys[pygame.K_LSHIFT] and not self.attacking:
            self.attack_time = pygame.time.get_ticks();
            print("Player is attacking w/ sec")
            self.secondary_attack = True;
            self.attacking = True
            
        if keys[pygame.K_b] and not self.attacking:
            print("player is blocking")
            self.blocking = True;
        
    
    def get_status(self):
        
        # handle idle animation 
        if self.direction.x == 0 and self.direction.y == 0:
            if not 'idle' in self.status and not 'attack' in self.status:
                self.status = self.status + '_idle'
        
        # handle attack then idle transition
        if self.attacking:
            self.direction.x = 0;
            self.direction.y = 0;
            if not 'attack' in self.status:
                if 'idle' in self.status:
                    self.status = self.status.replace('_idle', '_attack')
                
                else:    
                    self.status = self.status + "_attack"

        else:
            if 'attack' in self.status:
                self.status = self.status.replace('_attack', '')
    
    def cool_down(self):
        current_time = pygame.time.get_ticks();
        
        if self.attacking:
            current_time - self.attack_time >= self.attack_cooldown 
            self.attacking = False;
            
        
    
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
    
    # iterate through the animation index to obtain the correct character animation
    
    def animate(self):
        animation = self.animations[self.status];
        
        
        self.frame_index += self.animation_speed
        
        # get the frame index to select the current animation
        
        if self.frame_index >= len(animation): # get the len of the number of the items in the sprite sub folder
            self.frame_index = 0;
        
        print(self.frame_index)
        
        # set curent image
        #self.temp_image = animation[int(self.frame_index)];
        #print(animation[int(self.frame_index)])
        
        #self.rect = self.image.get_rect(center = self.hitbox.center); # update hitbox based on sprite change
        
        # scale sprite sheet
        #self.image = pygame.transform.scale(self.temp_image,(64,64));   
        
                         
    def update(self):
        #self.get_status(); # get the current status of the player
        print(self.status)
        
        self.animate()
        
        self.input();
        self.cool_down();
        
        self.move(self.speed)
            
        
    


