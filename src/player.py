
import pygame, sys
import random
from pathlib import Path
from settings import *
from os import walk

# class to represent the human controller player
class Player(pygame.sprite.Sprite):
    
      # init human controlled player      
    def __init__(self,pos,groups,obstacle_sprites,create_attack, destroy_attack):   
        super().__init__(groups) 
        
        # load starting player sprite sheet
        idle_down_folder = Path('sprites/characters/player/down_idle/idle_down.png')
        self.image_import = pygame.image.load(idle_down_folder) # import image 
        self.image = pygame.transform.scale(self.image_import,(64,64));   # scale sprite sheet
        self.rect = self.image.get_rect(topleft = pos)
        self.hitbox = self.rect.inflate(0,-5);
        
        # load the remaining player animations 
        self.import_player_animations()
        
        # player status 
        self.status = 'down'
        self.frame_index = 0;
        self.animation_speed = 0.15;
        
        # movement and attack vars
        self.direction = pygame.math.Vector2();
        
        # weapon handling
        self.create_attack = create_attack; # pass the function pointer of create attack to the player class
        weaponRandomAssignment = random.randint(0,len(weapon_data) - 1)  # assign a random weapon to the player 
        self.weapon_index = weaponRandomAssignment
        self.weapon = list(weapon_data.keys())[self.weapon_index]; # assign the random weapon to the player
        self.destroy_attack = destroy_attack; # pass the function pointer of destroy attack
            
        # attacking and blocking cooldown status vars
        self.attacking = False;
        self.attack_cooldown = 400;
        self.attack_time = None;
        self.block_cooldown = 400;
        self.obstacles_sprites = obstacle_sprites

        # balence the given weapon types with a certain class or range of weapons to create pros and cons of having different equipment
        
        # randomize player stats
        random_health = random.randint(80,100);   
        random_speed = random.randint(3,10);
        random_energy = random.randint(80,100);   

        
        # base player stats
        player_stats = {'health': 100, 'energy': 100, 'attack': 5, 'magic': 5, "speed": 5 }
        self.health = player_stats['health']
        self.speed = player_stats['speed'];
    
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
        
        player_death = []
        
        self.animations = {
            'up': move_up_folder, 'down': move_down_folder, 'left': move_left_folder, 'right': move_right_folder, 
            'up_idle': idle_up_folder, 'down_idle': idle_down_folder, 'left_idle': idle_left_folder, 'right_idle': idle_right_folder, 
            'up_block': block_up_folder, 'down_block':block_down_folder , 'left_block': block_left_folder, 'right_block': block_right_folder, 
            'up_attack': attack_up_folder, 'down_attack': attack_down_folder, 'left_attack': attack_left_folder, 'right_attack': attack_right_folder, 
            
        }
        
        
        for animation in self.animations.keys():
            currentPath = self.animations[animation]
            self.animations[animation] = self.import_folder(currentPath)


        # print final result to see if animation paths were loaded correctly
        print(self.animations)
    
    
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
            self.create_attack()
            print("player is attacking w/ prim")
            
        #if keys[pygame.K_LSHIFT] and not self.attacking:
        #    self.attack_time = pygame.time.get_ticks();
        #    self.secondary_attack = True;
        #    self.attacking = True
        #    self.create_attack()
        #    print("Player is attacking w/ sec")
            
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
            if current_time - self.attack_time >= self.attack_cooldown:
                self.attacking = False;
                self.destroy_attack()
            
        
    
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
        
        
        # set curent image
        self.image = animation[int(self.frame_index)];
        self.rect = self.image.get_rect(center = self.hitbox.center); # update hitbox based on sprite change
        
                     
    def update(self):
        self.get_status(); # get the current status of the player
        self.animate()
        self.input();
        self.cool_down();
        self.move(self.speed)
            
        
    


