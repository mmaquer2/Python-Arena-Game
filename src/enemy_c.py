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

# Class for CPU Character C
class Enemy_C(pygame.sprite.Sprite):
    def __init__(self,pos,groups,obstacle_sprites,create_attack,destroy_attack, create_block, destroy_block, nav_grid):
        super().__init__(groups)
        self.id = '4'
        self.sprite_type = "cpu_ai"    
        
        idle_down_folder = Path('sprites/characters/cpu_c/down_idle/idle_down.png')
        self.image_import = pygame.image.load(idle_down_folder) # import image 
        self.image = pygame.transform.scale(self.image_import,(64,64));   # scale sprite sheet
        self.rect = self.image.get_rect(center = (60,60))
        
        self.import_animations()  # load animations
        
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
        self.frame_index = 0
        self.animation_speed = 0.15
        self.direction = pygame.math.Vector2()
        self.obstacles_sprites = obstacle_sprites
        self.attacking = False
        self.is_weapon_destroyed = True
        self.is_block_destroyed = True
        self.attack_time = None
        self.attack_cooldown = 800 
        self.blocking = False
        self.block_cooldown = 800
        self.create_block = create_block
        self.destroy_block = destroy_block
        self.fleeing = False
        
        # declare the nav_grid for pathfinding
        self.nav_mesh = Grid(matrix = nav_grid)
        self.current_path = []
        self.converted_path = []
        self.goal_position = None
        self.previous_goal = None # holder to verify we aren't moving to our current location
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
        self.starting_health = self.health # record what the health was started at to judge when/if to flee an attack
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
            
    # import sprites from their respective file destinations
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

    # decide the next action for the cpu character
    def action_controller(self):
        self.target = self.is_enemy_within_visible_range()
        if self.target is not None and not self.fleeing:
            temp_dir = self.find_opponent_distance_direction(self.target)
            self.direction = temp_dir[1] # move towards the enemy 
            if self.is_enemy_within_attack_range():
                self.get_target_direction(); 
                self.use_weapon() # attack if you are in range 
            
        if not self.fleeing and self.is_enemy_within_attack_range():
            self.get_target_direction()
            self.use_weapon(); 
        
        # roll dice to see if the CPU should flee
        if not self.fleeing and self.roll_dice_to_flee() :
            self.fleeing = True
            self.make_path(); # init pathfinding sequence to flee to a random locaiton
            self.get_movement_direction();
        
        # if fleeing is in process check the current path
        if self.fleeing:
            self.check_goal_reached()  
            
    
        # roll a virtual die to determine to flee from an attack
    def roll_dice_to_flee(self):
        if self.health < self.starting_health // 2 :
            # roll a random die to decide whether to flee or not
            #rand_num = random.randint(0,30)
            # if rand_mum < 18:
            print(" cpu c fleeing from attack")
            return True
        else:
            return False
    
    
    # function to check where the current target is located around the CPU
    def get_target_direction(self):
        myVec = pygame.math.Vector2(self.rect.center)
        opponentVec = pygame.math.Vector2(self.target.rect.center)
        direction_to_face = (opponentVec - myVec).normalize()
        if (self.direction.x > -.5 and self.direction.y < .5) and (self.direction.x < .5 and self.direction.y < .5):
            self.status = "up"
               
        elif (self.direction.x > -0.5 and self.direction.y > -0.5) and ( self.direction.x < 0.5 and self.direction.y > -0.5):
            self.status = "down"
                
        elif (self.direction.x  < .5 and self.direction.y < .5) and (self.direction.x < .5 and self.direction.y > -.5):
            self.status = 'left'
            
        elif (self.direction.x > -0.5 and self.direction.y < 0.5 ) and (self.direction.x > -0.5 and self.direction.y > -0.5):
            self.status = 'right'
    
    # move character based on current direction and sped
    def move(self,speed):
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize();
        
        if (self.direction.x > -.5 and self.direction.y < .5) and (self.direction.x < .5 and self.direction.y < .5):
            self.status = "up"
            
        elif (self.direction.x > -0.5 and self.direction.y > -0.5) and ( self.direction.x < 0.5 and self.direction.y > -0.5):
            self.status = "down"
            
        elif (self.direction.x  < .5 and self.direction.y < .5) and (self.direction.x < .5 and self.direction.y > -.5):
            self.status = 'left'
        
        elif (self.direction.x > -0.5 and self.direction.y < 0.5 ) and (self.direction.x > -0.5 and self.direction.y > -0.5):
            self.status = 'right'
            
        self.hitbox.x += self.direction.x * speed # horizontal movement 
        self.collision('horizontal')
        self.hitbox.y += self.direction.y * speed # vertical movement
        self.collision('vertical')
        self.rect.center = self.hitbox.center;   # describes the hitbox for the character
        
    # get the location of the nearest enemy character
    def find_nearest_enemy(self):
        nearest_target_distance = 100000;
        nearest_target = ''
        # scan through all opponent players for the one with the shortest distance
        for opp in self.opponents:
            myVec = pygame.math.Vector2(self.rect.center)
            opponentVec = pygame.math.Vector2(opp.rect.center)  #calculate the vector between each opp and ai
            temp_distance = (opponentVec - myVec).magnitude()
            if temp_distance < nearest_target_distance:
                nearest_target = opp;
                
        return self.find_opponent_distance_direction(nearest_target);
        
    
    # iterate through enemy oppoenents and their locations
    def is_enemy_within_visible_range(self):
        myVec = pygame.math.Vector2(self.rect.center)
        for opp in self.opponents:
            opponentVec = pygame.math.Vector2(opp.rect.center)  #calculate the vector between each opp and ai
            temp_distance = (opponentVec - myVec).magnitude()
            if temp_distance < self.view_radius:  
                return opp  # if the distance between ai and other character is within my visitable range return true
        
            
  # determine if an enemy is within the attack range
    def is_enemy_within_attack_range(self):
        myVec = pygame.math.Vector2(self.rect.center)
        for opp in self.opponents:
            opponentVec = pygame.math.Vector2(opp.rect.center)
            temp_distance = (opponentVec - myVec).magnitude()
            if temp_distance < self.attack_radius:  # if the distance between ai and other character is within my visitable range return true
                if self.target is not None and self.target.health > 0: # check if the target is still alive
                    return True
            
        return False      
    
    # character to use its assigned weapon to attack
    def use_weapon(self):
            self.command = 'attack'
    
    
    def make_path(self):
            # get start and end destinations for a new path
            x = self.rect.centerx // 64 # divide location by map tile size of 64
            y = self.rect.centery // 64
            start_loc = [x,y]  
            end_loc = self.get_waypoint()
            self.plan_path(start_loc,end_loc) # plan a path to that destination
            self.create_surface_checkpoints() # convert the nav_mesh grid to surface coordinates
    
    
    # select a random waypoint to be used as a destination for the CPU 
    def get_waypoint(self):
        waypoints = [[2,3], [17,9], [17,9]]
        random_int = random.randint(0,2)
        return waypoints[random_int]
    
    # plan a path using the Astar package       
    def plan_path(self,start,end):
        self.current_path = [] # reset the current_path to empty
        start_x = start[0]   # convert game_space coordinates to nav_mesh coordinates
        start_y = start[1]   
        end_x = end[0] 
        end_y = end[1] 
        start_node = self.nav_mesh.node(start_x,start_y)
        end_node = self.nav_mesh.node( end_x,end_y)
        finder = AStarFinder() # calculate the actual path
        self.current_path, runs = finder.find_path(start_node,end_node,self.nav_mesh)  
        self.nav_mesh.cleanup(); # cleanup the previous path to calculate another path
    
    # convert the Astar generated path into a series of checkpoints on the map surface
    def create_surface_checkpoints(self):
        if self.current_path:
            self.converted_path = []
            for coor in self.current_path:   
                new_x = (coor[0] * 64) + 32
                new_y = (coor[1] * 64) + 32
                new_rect = pygame.Rect((new_x - 4 , new_y - 4 ),( 32,32 ))  # create a large enough checkpoint rect to colide with
                self.converted_path.append(new_rect)
    
    
    # check if the character has reached a current goal     
    def check_goal_reached(self):
        if self.converted_path:
            for rect in self.converted_path:
                if rect.collidepoint(self.rect.center):
                    del self.converted_path[0]
                    
    
    # get the next goal location and direction for the path planning    
    def get_movement_direction(self):
        if self.converted_path:
            start = pygame.math.Vector2(self.rect.center)
            end = pygame.math.Vector2(self.converted_path[0].center)
            self.direction = (end - start).normalize()
        else:
            self.fleeing = False # set to action controller state that the character is no longer in a fleeing mode
            self.current_path = []
            self.converted_path = []
            self.direction = pygame.math.Vector2(0,0)
            
 
    # get damage total from an attacking weapon
    def get_damage(self,damage,weapon_owner_id):
        if self.blocking == False and weapon_owner_id != self.id:
            print("cpu c is taking damage", self.health)
            self.health = self.health - damage;
            
            #if self.roll_dice_to_block():
            #    self.command = 'block'
            
            self.damage_sound.play();  
            self.check_death()
            
    # roll a virtual die to decide whether or not to block from a current attack
    # 32 percent chance to block an attack from an opponent
    def roll_dice_to_block(self):
        rand_num = random.randint(0,30)
        if(rand_num < 12):
            return True;
        else:
            return False
    

        
    
    # select a random waypoint to be used as a destination to flee from an attack
    def get_waypoint(self):
        waypoints = [[2,1], [2,34], [32,34],[34,1],[17,9]]
        random_int = random.randint(0,4)
        #print(" random location is: ",waypoints[random_int])
        goal = waypoints[random_int]
        goal_x = goal[0] * 32
        goal_y = goal[1] * 32
        
        return [goal_x, goal_y]
    
    
    # check if health is 0 and character has died
    def check_death(self):
        if self.health <= 0:
            self.destroy_attack() # remove any sprites from the previous command before dying
            self.destroy_block()
            self.kill()
    

    # change the status of the cpu AI to actually animate and execute the action
    def cpu_input(self):
     
        if self.command == 'attack' and not self.attacking and not self.blocking:
            self.attack_time = pygame.time.get_ticks();
            print("cpu ai C is attacking")
            self.attacking = True;
            self.create_attack()
            self.weapon_sound.play()
        
        if self.command == 'block' and not self.blocking and not self.attacking:
            self.block_time = pygame.time.get_ticks()
            print("cpu ai C is blocking")
            self.blocking = True;
            self.create_block();
             
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
    
    
    
    # calculate the total damage of a weapon based on player strength and weapon type
    def get_weapon_damage(self):
        total_damage = self.ai_stats['attack'] + weapon_data[self.weapon]['damage']
        return total_damage
    
    
    def get_status(self):   
        # handle move to idle
        if self.direction.x == 0 and self.direction.y == 0:
            if not 'idle' in self.status and not 'attack' in self.status and not 'block' in self.status:
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
        
        
        # handle block to idle transition
        if self.blocking:
            self.direction.x = 0;
            self.direction.y = 0;
            if not 'block' in self.status:
                if 'idle' in self.status:
                    self.status = self.status.replace('_idle', '_block')
                    
                else:
                    self.status = self.status + "_block"
        
        else:
            if 'block' in self.status:
                self.status = self.status.replace('_block', '')
        
    def collision(self,direction):
         # handle horizontal collisions
        if direction == 'horizontal':
            for sprite in self.obstacles_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.x > 0:
                        self.hitbox.right = sprite.hitbox.left
                        self.inCollision = True
                    if self.direction.x < 0:
                        self.hitbox.left = sprite.hitbox.right
                        self.inCollision = True
                        
        # handle vertical collisions
        if direction == 'vertical':
            for sprite in self.obstacles_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.y > 0:
                        self.hitbox.bottom = sprite.hitbox.top
                        self.inCollision = True
                    if self.direction.y < 0:
                        self.hitbox.top = sprite.hitbox.bottom
                        self.inCollision = True
                         
    def animate(self):
        animation = self.animations[self.status];
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation): # get the len of the number of the items in the sprite sub folder
            self.frame_index = 0;
        self.image = animation[int(self.frame_index)]; # set curent image
        self.rect = self.image.get_rect(center = self.hitbox.center); # update hitbox based on sprite change
        
    def cool_down(self):
        current_time = pygame.time.get_ticks();
        if self.attacking:
            if current_time - self.attack_time >= self.attack_cooldown + self.weapon_cool_down: 
                self.attacking = False;
                self.destroy_attack()
                
        if self.blocking:
            if current_time - self.block_time >= self.block_cooldown:
                self.destroy_block();
                self.blocking = False;
    
        
    def update(self):
        self.action_controller(); # determine the next action for the CPU AI
        self.cpu_input(); # animate based on the command and change cpu status
        self.get_status()        
        self.cool_down();
        self.command = '' # reset command after every tick
        self.move(self.speed);
        self.animate();        
        #print("cpu c: ",self.status)
    
    
    
    
    
    