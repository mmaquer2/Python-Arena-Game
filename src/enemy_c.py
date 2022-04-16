import pygame
import random
from settings import *
from os import walk
from pathlib import Path
from math import sin
import pathfinding
from pathfinding.core.diagonal_movement import DiagonalMovement
from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder

class Enemy_C(pygame.sprite.Sprite):
    def __init__(self,pos,groups,obstacle_sprites,create_attack,destroy_attack, create_block, destroy_block, nav_grid):
        
        self.id = '4'
        self.sprite_type = "cpu_ai"    
        
        idle_down_folder = Path('sprites/characters/cpu_c/down_idle/idle_down.png')
        self.image_import = pygame.image.load(idle_down_folder) # import image 
        self.image = pygame.transform.scale(self.image_import,(64,64));   # scale sprite sheet
        
        
        
        # load attack sound
        weapon_sound_file = Path('music/slash.wav')
        self.weapon_sound = pygame.mixer.Sound(weapon_sound_file)
        self.weapon_sound.set_volume(0.1)
  
        # load damage sound
        damage_sound_file = Path('music/hit.wav')
        self.damage_sound = pygame.mixer.Sound(damage_sound_file)
        self.damage_sound.set_volume(0.05)
        
        
        
        # direction and status vars
        self.status = 'down'
        self.frame_index = 0;
        self.animation_speed = 0.15;
        self.direction = pygame.math.Vector2()
        self.previous_direction = pygame.math.Vector2()
        self.obstacles_sprites = obstacle_sprites
        self.attacking = False;
        self.is_weapon_destroyed = True
        self.is_block_destroyed = True
        
        self.attack_time = None;
        self.attack_cooldown = 800;  
        
        self.blocking = False;
        self.block_cooldown = 800;
        
        self.create_block = create_block
        self.destroy_block = destroy_block
        
        # declare the nav_grid for pathfinding
        self.nav_mesh = Grid(matrix = nav_grid)
        self.current_path = []
        self.converted_path = []
        self.goal_position = None
        self.previous_goal = None # holder to verify we aren't moving to our current location
        
        
        # action_planning and behavior tree
        strategies = ['ambush','wander','beserk'] # list of possible strategies
        strat_ind = random.randint(0, len(strategies)-1)
        random_strat = strategies[strat_ind]
        
        #set the current strategy of the cpu AI
        self.goal = "wander"  # have the enemy cpu ai
        #self.goal = "beserk" # this  currently works, find the nearest enemy and attack 
        #self.goal = "ambush"
        
        self.command = ""
        self.inCollision = False; # status in if in a collision or not
        self.target = None; # this is the current target unit of the AI
        
        # weapon assignment and selection
        self.create_attack = create_attack;
        weaponRandomAssignment = random.randint(0,len(weapon_data) - 1);
        self.weapon_index = weaponRandomAssignment;
        self.weapon = list(weapon_data.keys())[self.weapon_index];
        self.local_weapon_data= weapon_data.get(self.weapon)
        self.weapon_cool_down = self.local_weapon_data['cooldown'];
        self.destroy_attack = destroy_attack;
        
        # the ranage in which being able to attack another unit
        self.attack_radius = self.local_weapon_data['attack_radius'];
        
        # the ranage/raidus of which being able to detect or "see" other units
        self.view_radius = 200;
        
        # the radius at which it is acceptable to move from our ambush location and attack another character
        self.ambush_radius = 400;
        
        self.ai_stats = {'health': 5000, 'energy': 100, 'attack': 2, 'magic': 5, "speed": 5 }
        self.health = self.ai_stats['health']
        #print("cpu a starting health:" , self.health)
        self.speed = self.ai_stats['speed'];
    
    
    
    def set_location(self,pos):
        self.rect = self.image.get_rect(topleft = pos)
        self.hitbox = self.rect.inflate(0,-5);
        
    def set_opponents(self,opponents):
        self.opponents = opponents;
        
    def import_animations(self):
    
        # the locations of the player sprites
        idle_up_folder = 'sprites/characters/cpu_c/up_idle'
        idle_down_folder = 'sprites/characters/cpu_c/down_idle'
        idle_right_folder = 'sprites/characters/cpu_c/right_idle'
        idle_left_folder = 'sprites/characters/cpu_c/left_idle'
        
        move_down_folder = 'sprites/characters/cpu_c/down'
        move_up_folder = 'sprites/characters/cpu_c/up'
        move_right_folder = 'sprites/characters/cpu_c/right'
        move_left_folder = 'sprites/characters/cpu_c/left'

        attack_down_folder = 'sprites/characters/cpu_c/down_attack'
        attack_up_folder = 'sprites/characters/cpu_c/up_attack'
        attack_right_folder = 'sprites/characters/cpu_c/right_attack'
        attack_left_folder = 'sprites/characters/cpu_c/left_attack'
        
        block_down_folder = 'sprites/characters/cpu_c/down_block'
        block_up_folder = 'sprites/characters/cpu_c/up_block'
        block_right_folder = 'sprites/characters/cpu_c/right_block'
        block_left_folder = 'sprites/characters/cpu_c/left_block' 

        ai_death_folder = 'sprites/characters/cpu_c/death'
        
        self.animations = {
            'up': move_up_folder, 'down': move_down_folder, 'left': move_left_folder, 'right': move_right_folder, 
            'up_idle': idle_up_folder, 'down_idle': idle_down_folder, 'left_idle': idle_left_folder, 'right_idle': idle_right_folder, 
            'up_block': block_up_folder, 'down_block':block_down_folder , 'left_block': block_left_folder, 'right_block': block_right_folder, 
            'up_attack': attack_up_folder, 'down_attack': attack_down_folder, 'left_attack': attack_left_folder, 'right_attack': attack_right_folder, 
            'death': ai_death_folder
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

    
    
    
    def action_controller(self):
                  
        self.target = self.is_enemy_within_visible_range()
        if self.target is not None:
            temp_dir = self.find_opponent_distance_direction(self.target)
            self.direction = temp_dir[1] # move towards the enemy 
            self.is_enemy_within_attack_range()  # attack if you are in range 
            
        else:
            self.direction = self.previous_direction;
            
        return
    
    
    
    
    
    
    
    
    def update(self):
        pass
    
    
    
    