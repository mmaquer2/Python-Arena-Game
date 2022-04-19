import pygame
import random
from settings import *
from os import walk
from pathlib import Path
from math import sin

class Enemy_B(pygame.sprite.Sprite):
    def __init__(self,pos,groups,obstacle_sprites,create_attack,destroy_attack, create_block, destroy_block, nav_grid):
        super().__init__(groups)
        self.id = '3'
        self.sprite_type = "cpu_ai"    
        
        # import starting sprite sheet
        idle_down_folder = Path('sprites/characters/cpu_b/down_idle/down_idle.png')
        self.image_import = pygame.image.load(idle_down_folder) # import image 
        self.image = pygame.transform.scale(self.image_import,(64,64));   # scale sprite sheet
        self.import_animations();  
        
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
        self.previous_direction = pygame.math.Vector2()
        self.obstacles_sprites = obstacle_sprites
        self.attacking = False
        
        self.attack_time = None
        self.attack_cooldown = 800  
        self.blocking = False
        self.block_cooldown = 800
        self.command = ""
        self.inCollision = False  # status in if in a collision or not
        self.target = None  # this is the current target unit of the AI
        
        # weapon assignment and selection
        self.create_attack = create_attack
        weaponRandomAssignment = random.randint(0,len(weapon_data) - 1)
        self.weapon_index = weaponRandomAssignment
        self.weapon = list(weapon_data.keys())[self.weapon_index]
        self.local_weapon_data= weapon_data.get(self.weapon)
        self.weapon_cool_down = self.local_weapon_data['cooldown']
        self.destroy_attack = destroy_attack
        
        
        # the ranage/raidus of which being able to detect or "see" other units
        self.view_radius = 200
        
        # the ranage in which being able to attack another unit
        self.attack_radius = 100
        
        # the radius at which it is acceptable to move from our ambush location and attack another character
        self.ambush_radius = 400

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
        idle_up_folder = 'sprites/characters/cpu_b/up_idle'
        idle_down_folder = 'sprites/characters/cpu_b/down_idle'
        idle_right_folder = 'sprites/characters/cpu_b/right_idle'
        idle_left_folder = 'sprites/characters/cpu_b/left_idle'
        
        move_down_folder = 'sprites/characters/cpu_b/down'
        move_up_folder = 'sprites/characters/cpu_b/up'
        move_right_folder = 'sprites/characters/cpu_b/right'
        move_left_folder = 'sprites/characters/cpu_b/left'

        attack_down_folder = 'sprites/characters/cpu_b/down_attack'
        attack_up_folder = 'sprites/characters/cpu_b/up_attack'
        attack_right_folder = 'sprites/characters/cpu_b/right_attack'
        attack_left_folder = 'sprites/characters/cpu_b/left_attack'
        
        block_down_folder = 'sprites/characters/cpu_b/down_block'
        block_up_folder = 'sprites/characters/cpu_b/up_block'
        block_right_folder = 'sprites/characters/cpu_b/right_block'
        block_left_folder = 'sprites/characters/cpu_b/left_block' 

        ai_death_folder = 'sprites/characters/cpu_b/death'
        
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

        
    def import_folder(self, path):
        items = []
        # get all images inside the given path
        for _,__,img_files in walk(path): # walk the given path
            for data in img_files:
                img_path = path + '/' + data # create full image path
                image_temp = pygame.image.load(img_path) # load file image 
                sacled_image = pygame.transform.scale(image_temp,(64,64));   #scale image to correct size
                items.append(sacled_image) # append surface image to the current item list
            
        return items
    
    
    def move(self, speed):
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize();
            if self.direction.x > self.direction.y:
                if self.direction.x > 0.5:
                    self.status = "right"
                else: 
                    self.status = "left"
            
            else: 
                if self.direction.y > 0.5:
                    self.status = "down"
                else:
                    self.status = "up"
            
        self.hitbox.x += self.direction.x * speed
        self.collision('horizontal')
        self.hitbox.y += self.direction.y * speed
        self.collision('vertical')
        self.rect.center = self.hitbox.center   # describes the hitbox for the character
    
    
    # plan action and set command for the ai to execute
    def action_controller(self):
        self.nearest_opp_dist, self.nearest_azimuth = self.find_nearest_enemy() # find nearest enemy
        self.direction = self.nearest_azimuth # move toward the nearest enemy location    
        self.target = self.is_enemy_within_visible_range() # see if a target is within range
        
        if self.target is not None: # if we can see a target, lock on and attack
            
            temp_dir = self.find_opponent_distance_direction(self.target)
            self.direction = temp_dir[1]
            
        if self.is_enemy_within_attack_range():
            self.use_weapon();
        
        
    #get the location of the nearest enemy character
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
                
        return self.find_opponent_distance_direction(nearest_target); # return the distance, direction of the nearest enemy
    
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
            self.temp_enemy = opp
            opponentVec = pygame.math.Vector2(opp.rect.center)
            temp_distance = (opponentVec - myVec).magnitude()
            if temp_distance < self.attack_radius:  # if the distance between ai and other character is within my visitable range return true
                if self.target is not None and self.temp_enemy.health > 0: # check if the target is still alive
                    return True
        
        return False
                
    def use_weapon(self):
        self.command = 'attack'
        
     # get damage total from an attacking weapon
    def get_damage(self,damage,weapon_owner_id):
        if self.blocking == False and weapon_owner_id != self.id:
            print("cpu b is taking damage", self.health)
            self.health = self.health - damage;
            self.damage_sound.play()   
            self.check_death()
            
    # check if health is 0 and character has died
    def check_death(self):
        if self.health <= 0:
            self.destroy_attack()
            self.kill()
    

    # change the status of the cpu AI to actually animate and execute the action
    def cpu_input(self):
     
        if self.command == 'attack' and not self.attacking:
            self.attack_time = pygame.time.get_ticks();
            print("cpu ai A is attacking")
            self.attacking = True;
            self.create_attack()
            self.weapon_sound.play()
        
        if self.command == 'block' and not self.blocking:
            self.block_time = pygame.time.get_ticks()
            print("cpu ai A is blocking")
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
                        #print("cpu in collision right")
                        self.inCollision = True
                    if self.direction.x < 0:
                        self.hitbox.left = sprite.hitbox.right
                        #print("cpu in collision left")
                        self.inCollision = True
                        
        # handle vertical collisions
        if direction == 'vertical':
            for sprite in self.obstacles_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.y > 0:
                        self.hitbox.bottom = sprite.hitbox.top
                        #print("in collision bot")
                        self.inCollision = True
                    if self.direction.y < 0:
                        self.hitbox.top = sprite.hitbox.bottom
                        #print("in collision bot")
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

    
    def flicker(self):
        alpha = self.flicker_value();
        self.image.set_alpha(alpha)
        
    
    def flicker_value(self):
        value = sin(pygame.time.get_ticks())
        if value >= 0:
            return 255;
        else:
            return 0;
    
        
    def update(self):
        self.action_controller(); # determine the next action for the CPU AI
        self.cpu_input(); # animate based on the command and change cpu status
        self.get_status()        
        self.cool_down();
        self.move(self.speed);
        self.animate();    
        self.command = '' # rest the command     
        self.previous_direction = self.direction # save the previous direction 
        