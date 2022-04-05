import pygame
import random
from settings import *
from os import walk
from pathlib import Path

class Enemy_A(pygame.sprite.Sprite):
    def __init__(self,pos,groups,obstacle_sprites,create_attack,destroy_attack):
        super().__init__(groups)
        
        # import starting sprite
        idle_down_folder = Path('sprites/characters/cpu_a/down_idle/idle_down.png')
        self.image_import = pygame.image.load(idle_down_folder) # import image 
        self.image = pygame.transform.scale(self.image_import,(64,64));   # scale sprite sheet
        
        # set hitbox
        self.rect = self.image.get_rect(topleft = pos)
        self.hitbox = self.rect.inflate(0,-5);
        
        #self.import_animations();  
        
        # direction and status vars
        self.status = 'down'
        self.frame_index = 0;
        self.animation_speed = 0.15;
        self.direction = pygame.math.Vector2()

        
        self.create_attack = create_attack;
        weaponRandomAssignment = random.randint(0,len(weapon_data) - 1);
        self.weapon_index = weaponRandomAssignment;
        self.weapon = list(weapon_data.keys())[self.weapon_index];
        self.destroy_attack = destroy_attack;
            
    
    
    def import_animations(self):

        # the locations of the player sprites
        idle_up_folder = 'sprites/characters/cpu_a/up_idle'
        idle_down_folder = 'sprites/characters/cpu_a/down_idle'
        idle_right_folder = 'sprites/characters/cpu_a/right_idle'
        idle_left_folder = 'sprites/characters/cpu_a/left_idle'
        
        move_down_folder = 'sprites/characters/cpu_a/down'
        move_up_folder = 'sprites/characters/cpu_a/up'
        move_right_folder = 'sprites/characters/cpu_a/right'
        move_left_folder = 'sprites/characters/cpu_a/left'

        attack_down_folder = 'sprites/characters/cpu_a/down_attack'
        attack_up_folder = 'sprites/characters/cpu_a/up_attack'
        attack_right_folder = 'sprites/characters/cpu_a/right_attack'
        attack_left_folder = 'sprites/characters/cpu_a/left_attack'
        
        block_down_folder = 'sprites/characters/cpu_a/down_block'
        block_up_folder = 'sprites/characters/cpu_a/up_block'
        block_right_folder = 'sprites/characters/cpu_a/right_block'
        block_left_folder = 'sprites/characters/cpu_a/left_block' 

        death = []
        
        self.animations = {
            'up': move_up_folder, 'down': move_down_folder, 'left': move_left_folder, 'right': move_right_folder, 
            'up_idle': idle_up_folder, 'down_idle': idle_down_folder, 'left_idle': idle_left_folder, 'right_idle': idle_right_folder, 
            'up_block': block_up_folder, 'down_block':block_down_folder , 'left_block': block_left_folder, 'right_block': block_right_folder, 
            'up_attack': attack_up_folder, 'down_attack': attack_down_folder, 'left_attack': attack_left_folder, 'right_attack': attack_right_folder, 
            
        } 
        
        for animation in self.animations.keys():
            currentPath = self.animations[animation]
            self.animations[animation] = self.import_folder(currentPath)  

        
        def import_folder(self,path):
            items = []
            # get all images inside the given path
            for _,__,img_files in walk(path): # walk the given path
                for data in img_files:
                    img_path = path + '/' + data # create full image path
                    image_temp = pygame.image.load(img_path) # load file image 
                    sacled_image = pygame.transform.scale(image_temp,(64,64));   #scale image to correct size
                    items.append(sacled_image) # append surface image to the current item list
                
            return items
        
    
    def move(self):
        pass
    
    
    def get_status(self):
        pass
    
    def collision(self):
        pass
    
    # make some sort of decision based on the game AI behavior Tree
    def decide(self):
        pass
    
    def animate(self):
        pass
    
    
    def cool_down(self):
        pass

        
    def update(self):
        pass
        #self.get_status()
        #self.animate();
        
        #self.decide();
        
        #self.cool_down();
        #self.move();
    