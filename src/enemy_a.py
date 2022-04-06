import pygame
import random
from settings import *
from os import walk
from pathlib import Path

class Enemy_A(pygame.sprite.Sprite):
    def __init__(self,pos,groups,obstacle_sprites,create_attack,destroy_attack):
        super().__init__(groups)
        
        self.id = '2'
        
        # import starting sprite
        idle_down_folder = Path('sprites/characters/cpu_a/down_idle/idle_down.png')
        self.image_import = pygame.image.load(idle_down_folder) # import image 
        self.image = pygame.transform.scale(self.image_import,(64,64));   # scale sprite sheet
        
      
        
        self.import_animations();  
        
        # direction and status vars
        self.status = 'down'
        self.frame_index = 0;
        self.animation_speed = 0.15;
        self.direction = pygame.math.Vector2()
        self.obstacles_sprites = obstacle_sprites
        
        
        # action_planning and behavior tree
        # what is the current goal of the AI?
        self.goal = "wander"
        self.command = "move_left"
        
        self.create_attack = create_attack;
        weaponRandomAssignment = random.randint(0,len(weapon_data) - 1);
        self.weapon_index = weaponRandomAssignment;
        self.weapon = list(weapon_data.keys())[self.weapon_index];
        self.destroy_attack = destroy_attack;
        
        # setting the distance which one may see or attack other units
        # attack_radius': 80, 'notice_radius': 360}, example attack and notice radius data
        self.notice_radius = 50;
        self.attack_radius = 360;
        
        
        # randomize stats
        random_health = random.randint(80,100);   
        random_energy = random.randint(80,100); 
        random_attack = random.randint(2,10); 
        random_magic = random.randint(80,100); 
        random_speed = random.randint(3,10);
          

        self.ai_stats = {'health': 100, 'energy': 100, 'attack': 5, 'magic': 5, "speed": 5 }
        self.health = self.ai_stats['health']
        self.speed = self.ai_stats['speed'];
    
    
    def set_location(self,pos):
        self.rect = self.image.get_rect(topleft = pos)
        self.hitbox = self.rect.inflate(0,-5);
      
    
    def set_opponents(self,opponents):
        self.opponents = opponents;
    
    
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
    
    
    def move(self,speed):
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize();
        
        self.hitbox.x += self.direction.x * speed
        self.collision('horizontal')
        self.hitbox.y += self.direction.y * speed
        self.collision('vertical')
        self.rect.center = self.hitbox.center;
    
    
    
    # plan action
    def plan_action(self):
        
        if self.goal == "ambush":
            if self.see_enemy():
                
                
                pass
      
            # move towards enemey
         
        #self.iterate_enemy() # iterate through enemy locations
       
        if self.goal == 'wander':
            new_movement = self.get_waypoint();    # plan path to a new waypoint
            # move to this waypoint
            # what direction do I need to move to go here?

        
        if self.goal == 'hide':
            pass
    
    
    # iterate through enemy oppoenents and their locations
    def see_enemy(self):
        for opp in self.opponents:
            # print(opp.rect[0], opp.rect[1]) # get the x,y coordinates of an opponent
            pass
    
    def get_waypoint(self):
            # plan path to this new waypoint
        waypoint = 1;
        return waypoint;
    
    
    def plan_path(self):
        pass
    
    
    def plan_movement(self):
        pass
        # get the difference between the previous and next direction
    
    
    # check if an opponent is within visible range
    def is_Opponent_Within_Range(self):
        pass;
    
    

    # change the status of the cpu AI to actually animate and execute the action
    def cpu_input(self):
        
        if self.command == "move_up":
            self.direction.y = -1;
            self.status = "up"
        
        if self.command == "move_down":
            self.direction.y = 1;
            self.status = "down"
        
        if self.command == "move_left":
            self.direction.x = -1;
            self.status = 'left'
        
        if self.command == "move_right":
            self.direction.x = 1
            self.status = 'right'
        
        if self.command == 'attack' and not self.attacking:
            self.attacking = True;
        
        if self.command == 'block' and not self.blocking:
            self.blocking = True;
        
        if self.command == "idle":
            pass
        
             
   
    
    # get the distance and direction for an opponent
    def find_opponent_distance_direction(self,enemy):
        myVec = pygame.math.Vector2(self.rect.center)
        opponentVec = pygame.math.Vector2(enemy.rect.center)
        
        distance = (opponentVec - myVec).magnitude()
        
        if distance > 0:
            direction = (opponentVec - myVec).normalize();
        else:
            direction = pygame.math.Vector2()
        
        return (distance, direction)
    
    
    def rotate(self):
        misc_dirs = ['left','right','up','down']
        random_dir = random.randint(0,3);
        self.status = misc_dirs[random_dir]
    
    
    def get_status(self):
        
        distance = 0;
        
        
        #if distance <= self.attack_radius:
        #    self.status = 'attack'
        
        #if distance <= self.notice_radius:
        #    self.status = 'move'
        
        # else:
        #    self.status = 'idle'

        if self.direction.x == 0 and self.direction.y == 0:
            if not 'idle' in self.status and not 'attack' in self.status:
                self.status = self.status + '_idle'
    
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
    
    # make some sort of decision based on the game AI behavior Tree
    def decide(self):
        pass
    
        # general seek and destory strategy: 
        
        # can i see an enemy unit? 
            # move towards enemy and attack 
        
        # if not pick a reachable point and move to it
        
    
    
    def animate(self):
        animation = self.animations[self.status];
        self.frame_index += self.animation_speed
        # get the frame index to select the current animation
        if self.frame_index >= len(animation): # get the len of the number of the items in the sprite sub folder
            self.frame_index = 0;
        
        # set curent image
        self.image = animation[int(self.frame_index)];
        self.rect = self.image.get_rect(center = self.hitbox.center); # update hitbox based on sprite change
        

    
    def cool_down(self):
        pass

        
    def update(self):
        self.get_status()
        self.animate();
        self.plan_action(); # determine the next action for the CPU AI
        self.cpu_input(); # 
        self.cool_down();
        self.move(self.speed);
    