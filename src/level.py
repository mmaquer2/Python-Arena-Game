
import pygame,sys
import random
from settings import *
from wall import Wall
from player import Player
from enemy_a import Enemy_A
from weapon import Weapon

# class to handle running the level for the game state
class Level:
    
    def __init__(self):
        
        #init visual surfaces
        self.display_surface = pygame.display.get_surface();  # create game sprites
        self.visible_sprites = CameraGroup()  # create the camera view to focus on the player 
        self.obstacle_sprites = pygame.sprite.Group(); # create sprite group for obstacles
    
        # attack sprites
        self.current_attack_player = None;
        self.attack_sprites = pygame.sprite.Group(); # create sprite group for attcking objects
        self.attackable_sprites = pygame.sprite.Group();
        
        self.createMap(); # init map starting locations for obstacles and players 
        
        
    def createMap(self):
        # select game map by randomizing what map is being selected from the world maps in the settings 
        mapNum = random.randint(0, 2)
        if(mapNum == 0):
            levelMap = WORLD_MAP_ONE
        if(mapNum == 1):
            levelMap = WORLD_MAP_TWO
        if(mapNum == 2):
            levelMap = WORLD_MAP_THREE
        
        # Create and place traps on 
        # append trap to level map, such as t = bear trap, f = flame 
         
        # Randomize starting locations, there are 4 possible starting points on each map
        players = ["p","a","b","c"]
        random.shuffle(players) # shuffle players for different locations
        
        # players[0] = p
        #  
        
        for row_ind,row in enumerate(WORLD_MAP_ONE):
            for col_ind, col in enumerate(row):
                x = col_ind * tileSize;
                y = row_ind * tileSize
                
        # set what each tile will represent on the world map
                # create the wall obstacles on the map
                if col == 'x':
                    Wall((x,y),[self.visible_sprites,self.obstacle_sprites])
                
                #create the player on the map
                if col == 'p':
                    self.player = Player((x,y), [self.visible_sprites,self.attackable_sprites], self.obstacle_sprites, self.create_attack, self.destroy_attack)
                    
        # place npc characters on the map
                if col=='a':
                    self.cpu_a = Enemy_A((x,y), [self.visible_sprites,self.attackable_sprites],self.obstacle_sprites, self.create_attack, self.destroy_attack)
                
                #if col=='b':
                # self.cpu_b = Enemy_B((x,y), [self.visible_sprites],self.obstacle_sprites, self.create_attack, self.destroy_attack)
                
                #if col=='c':
                # self.cpu_c = Enemy_C((x,y), [self.visible_sprites],self.obstacle_sprites, self.create_attack, self.destroy_attack)
    
    # handles drawing the weapon sprite of a player or cpu AI
    def create_attack(self):
       self.current_attack_player = Weapon(self.player,[self.visible_sprites,self.attack_sprites])
    
    # removes a weapon from the game, once an attack is complete
    def destroy_attack(self):
        if self.current_attack_player:
            self.current_attack_player.kill()
        
    
    # handles logic for checking collisions between weapons and players 
    def attack_logic(self):
        if self.attack_sprites:
            for attack_sprite in self.attack_sprites:
               collision_sprites =  pygame.sprite.spritecollide(attack_sprite,self.attackable_sprites,False) # get collisions between sprites and weapons
               if collision_sprites:
                   for target_sprite in collision_sprites:
                       
                       # handle what happens when a collision occurs
                       
                       # target_sprite.get_damage(self.player,attack_sprite)
                       
                       # how to handle the current health of the player and enemy AI?
                       target_sprite.kill() # kill the target?
    
    # check the status of the players, is the game over?             
    def isGameOver(self):
        
        # check statues of players
        
        
        # if people are still alive
        
        
        return False;
        
    
    # loop to update and draw the game           
    def run(self):
        self.visible_sprites.custom_draw(self.player)
        self.visible_sprites.update();
    
# small class to create a camera view focused on the player     
class CameraGroup(pygame.sprite.Group):
    def __init__(self):
        
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.half_width = self.display_surface.get_size()[0] // 2;
        self.half_height = self.display_surface.get_size()[1] // 2 ;
        self.offset = pygame.math.Vector2();
        
        
    def custom_draw(self,player):
        
        self.offset.x = player.rect.centerx - self.half_width;
        self.offset.y = player.rect.centery - self.half_height;
        
        for sprite in sorted(self.sprites(),key = lambda sprite: sprite.rect.centery):
            offset_pos = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image,offset_pos)
            
            