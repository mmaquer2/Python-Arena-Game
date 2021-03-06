import pygame
import random
from pathlib import Path
from settings import *
from os import walk
from math import sin

# class to represent the human controller player
class Player(pygame.sprite.Sprite):
    # init human controlled player      
    def __init__(self,pos,groups, obstacle_sprites,create_attack, destroy_attack, create_block, destroy_block):   
        super().__init__(groups) 
        self.id = '1'
        self.sprite_type = 'player'
        
        # load starting player sprite sheet and attack sound
        idle_down_folder = Path('sprites/characters/player/down_idle/idle_down.png')
        self.image_import = pygame.image.load(idle_down_folder) # import image 
        self.image = pygame.transform.scale(self.image_import,(64,64))  # scale sprite sheet
        self.rect = self.image.get_rect( topleft = pos)
        self.hitbox = self.rect.inflate(0, -5)
    
        # load attack sound
        weapon_sound_file = Path('music/sword.wav')
        self.weapon_sound = pygame.mixer.Sound(weapon_sound_file)
        self.weapon_sound.set_volume(0.1)
  
        # load damage sound #
        damage_sound_file = Path('music/hit.wav')
        self.damage_sound = pygame.mixer.Sound(damage_sound_file)
        self.damage_sound.set_volume(0.1)
        
        
        # load the remaining player animations # 
        self.import_player_animations()
        
        # player status #
        self.status = 'down'
        self.frame_index = 0
        self.animation_speed = 0.15
        
        # movement and attack vars
        self.direction = pygame.math.Vector2()
        
        # weapon handling
        self.create_attack = create_attack  # pass the function pointer of create attack to the player class
        self.destroy_attack = destroy_attack  # pass the function pointer of destroy attack
        self.is_weapon_destroyed = True
        self.opponents = []
        self.create_block = create_block
        self.destory_block = destroy_block
        
        
        # weapon random assignment and stats
        weaponRandomAssignment = random.randint(0,len(weapon_data) - 1)  # assign a random weapon to the player 
        self.weapon_index = weaponRandomAssignment
        self.weapon = list(weapon_data.keys())[self.weapon_index] # assign the random weapon to the player
        self.local_weapon_data= weapon_data.get(self.weapon)
        self.weapon_cool_down = self.local_weapon_data['cooldown']
        
        # uncomment to test the bow 
        #self.weapon = 'bow'
        #self.weapon_cool_down = 100
        
        # attacking and blocking cooldown status vars
        self.attacking = False
        self.blocking = False
        self.attack_cooldown = 800
        self.attack_time = None
        self.block_cooldown = 800
        self.obstacles_sprites = obstacle_sprites
       
        # base player stats
        self.player_stats = {'health': 50000, 'energy': 100, 'attack': 5, 'magic': 5, "speed": 5 }
        self.health = self.player_stats['health']
        self.speed = self.player_stats['speed']
    
    # function to set the characters location
    def set_location(self, pos):
        self.rect = self.image.get_rect(topleft = pos)
        self.hitbox = self.rect.inflate(0,-5)
        
    # function to get the characters x and y coordinate
    def get_location(self):
        print(self.rect.x, self.rect.y);
        return self.rect.x , self.rect.y
    
    
    def set_opponents(self,opponents):
        self.opponents = opponents
    
    
    # function to import player animation resources
    def import_player_animations(self):
        
        # the locations of the player sprites
        idle_up_folder = 'sprites/characters/player/up_idle'
        idle_down_folder = 'sprites/characters/player/down_idle'
        idle_right_folder = 'sprites/characters/player/right_idle'
        idle_left_folder = 'sprites/characters/player/left_idle'
        
        move_down_folder = 'sprites/characters/player/down'
        move_up_folder = 'sprites/characters/player/up'
        move_right_folder = 'sprites/characters/player/right'
        move_left_folder = 'sprites/characters/player/left'
        
        attack_down_folder = 'sprites/characters/player/down_attack'
        attack_up_folder = 'sprites/characters/player/up_attack'
        attack_right_folder = 'sprites/characters/player/right_attack'
        attack_left_folder = 'sprites/characters/player/left_attack'
        
        block_down_folder = 'sprites/characters/player/down_block'
        block_up_folder = 'sprites/characters/player/up_block'
        block_right_folder = 'sprites/characters/player/right_block'
        block_left_folder = 'sprites/characters/player/left_block'  
        
        player_death_folder = 'sprites/characters/player/death'  
        
        self.animations = {
            'up': move_up_folder, 'down': move_down_folder, 'left': move_left_folder, 'right': move_right_folder, 
            'up_idle': idle_up_folder, 'down_idle': idle_down_folder, 'left_idle': idle_left_folder, 'right_idle': idle_right_folder, 
            'up_block': block_up_folder, 'down_block':block_down_folder , 'left_block': block_left_folder, 'right_block': block_right_folder, 
            'up_attack': attack_up_folder, 'down_attack': attack_down_folder, 'left_attack': attack_left_folder, 'right_attack': attack_right_folder,
            'death': player_death_folder
        }
        
        
        
        for animation in self.animations.keys():
            currentPath = self.animations[animation]
            self.animations[animation] = self.import_folder(currentPath)

    # function to iterate through animation sub folders
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
          
    # handle user input with the arrow keys
    def input(self):
        keys = pygame.key.get_pressed()
    
        if not self.attacking and not self.blocking:   # this line prevents player from moving and blocking at the same time
            # y axis
            #moving up
            if keys[pygame.K_UP] and not self.attacking:
                self.direction.y = -1
                self.status = 'up'
                
            #moving down
            elif keys[pygame.K_DOWN] and not self.attacking:
                self.direction.y = 1
                self.status = 'down'
            
            # no movement
            else:
                self.direction.y = 0
            
            # x axis 
            #moving right:
            if keys[pygame.K_RIGHT] and not self.attacking:
                self.direction.x = 1
                self.status = 'right'
                
            # moving left:    
            elif keys[pygame.K_LEFT] and not self.attacking:
                self.direction.x = -1
                self.status = 'left'
            # no movement    
            else:
                self.direction.x = 0;
                
            # using items 
            if keys[pygame.K_i]:
                self.use_item = True
            
            # attacks      
            if keys[pygame.K_SPACE] and not self.attacking:
                self.attack_time = pygame.time.get_ticks();
                self.primary_attack = True;
                self.attacking = True;
                self.weapon_sound.play()
                self.create_attack()   
                # play attack sound
             
        
            # blocking    
            if keys[pygame.K_b] and not self.blocking:
                self.block_time = pygame.time.get_ticks();
                print("player is blocking")
                self.blocking = True;
                self.create_block()
           
        
    def get_status(self):
              
        # handle idle animation 
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
                
        # handle blocking action
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
            
        
    def cool_down(self):
        current_time = pygame.time.get_ticks();
        if self.attacking:
            if current_time - self.attack_time >= self.attack_cooldown + self.weapon_cool_down: 
                self.destroy_attack()
                self.attacking = False;

        
        if self.blocking:
            if current_time - self.block_time >= self.block_cooldown:
                self.destory_block();
                self.blocking = False;
        
    # handling player movement across the map including physics
    def move(self,speed):
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize();
        
        #self.char_collision('vertical')
        #self.char_collision('horizontal')
        self.hitbox.x += self.direction.x * speed
        self.collision('horizontal')
        self.hitbox.y += self.direction.y * speed
        self.collision('vertical')
     
        self.rect.center = self.hitbox.center;
        
        
        
            
    # collision handling for obstacles           
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
                        
    # collision handling for other characters             
    def char_collision(self,direction):
        # handle horizontal collisions
        if direction == 'horizontal':
            for opp in self.opponents:
                if opp.hitbox.colliderect(self.hitbox):
                    if self.direction.x > 0:
                        self.hitbox.right = opp.hitbox.left
                    if self.direction.x < 0:
                        self.hitbox.left = opp.hitbox.right
                        
        # handle vertical collisions
        if direction == 'vertical':
            for opp in self.opponents:
                if opp.hitbox.colliderect(self.hitbox):
                    if self.direction.y > 0:
                        self.hitbox.bottom = opp.hitbox.top
                    if self.direction.y < 0:
                        self.hitbox.top = opp.hitbox.bottom
    
    # iterate through the animation index to obtain the correct character animation
    def animate(self):
        animation = self.animations[self.status];
        self.frame_index += self.animation_speed
        # get the frame index to select the current animation
        if self.frame_index >= len(animation): # get the len of the number of the items in the sprite sub folder
            self.frame_index = 0;
        # set curent image
        self.image = animation[int(self.frame_index)];
        self.rect = self.image.get_rect(center = self.hitbox.center); # update hitbox based on sprite change
        
    # calculate the total damage of a weapon based on player strength and weapon type
    def get_weapon_damage(self):
        total_damage = self.player_stats['attack'] + weapon_data[self.weapon]['damage']

        return total_damage
    
    # get the current health of the player
    def get_health_stats(self):
        return self.health
    
    # recieve damage from other units/ obstacles on the map
    def get_damage(self,damage_amount, weapon_owner_id):
              
        if self.blocking == False and weapon_owner_id != self.id:    # check if were blocking and the weapon sprite isn't ours
            print("human player is taking damage", self.health)
            self.health = self.health - damage_amount;
            self.damage_sound.play()
            self.check_death()
        
    
    # function to check if the players health has reached zero
    def check_death(self):
         if(self.health <= 0):
                self.kill()
                print("game over you have no health remaining!")
                quit()
    
    # flicker the sprite to show the character is taking damage
    def flicker(self):
        alpha = self.flicker_value();
        self.image.set_alpha(alpha)
        
    # create a noise value for the flicker function
    def flicker_value(self):
        value = sin(pygame.time.get_ticks())
        if value >= 0:
            return 255;
        else:
            return 0;
    
    def update(self):
        self.get_status(); # get the current status of the player
        self.input();
        self.animate()
        self.cool_down();
        self.move(self.speed)
        #print(self.rect.x // 32, self.rect.y// 32)
            
        
    


