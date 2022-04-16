
import pygame
import random
from settings import *
from wall import Wall
from player import Player
from enemy_a import Enemy_A
from enemy_b import Enemy_B
from enemy_c import Enemy_C
from weapon import Weapon
from shield import Shield
import pathfinding
from pathfinding.core.diagonal_movement import DiagonalMovement
from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder

# class to handle running the level for the game state
class Level:
    def __init__(self):
        #init visual surfaces
        self.display_surface = pygame.display.get_surface()  # create game sprites
        self.visible_sprites = CameraGroup()  # create the camera view to focus on the player 
        self.obstacle_sprites = pygame.sprite.Group()   # create sprite group for obstacles
    
        # attack sprites
        self.current_attack_player = None;
        self.cpu_a_attack = None;
        self.cpu_b_attack = None;
        self.cpu_c_attack = None;
        
        # block and shield attack_sprites
        self.current_block_player = None;
        self.cpu_a_block = None;
        self.cpu_b_block = None;
        self.cpu_c_block = None;
        
        #stores the nav_grid for pathfinding
        
        
        self.attack_sprites = pygame.sprite.Group() # create sprite group for attcking objects
        self.attackable_sprites = pygame.sprite.Group()
        self.createMap() # init map starting locations for obstacles and players 
        
    def createMap(self):
        # select game map by randomizing what map is being selected from the world maps in the settings 
        mapNum = random.randint(0, 1)
        
        self.levelMap = WORLD_MAP_ONE
        self.nav_grid = NAV_GRID_ONE
        
        #if(mapNum == 1):
        #    self.levelMap = WORLD_MAP_TWO
        #    self.nav_grid = NAV_GRID_TWO
        
        #if(mapNum == 2):
            #self.levelMap = WORLD_MAP_THREE
        #if(mapNum == 3):
            #self.levelMap = WORLD_MAP_FOUR
    
        # create nav mesh grid
        self.nav_mesh_grid = Grid(matrix = self.nav_grid)
        
        # init player and CPU_AI: 
        self.player = Player((1,1), [self.visible_sprites,self.attackable_sprites], self.obstacle_sprites, self.create_attack, self.destroy_attack_player, self.create_block_player, self.destroy_block_player)    
        self.cpu_a = Enemy_A((2,2), [self.visible_sprites,self.attackable_sprites],self.obstacle_sprites, self.create_attack_cpu_a, self.destroy_attack_cpu_a, self.create_block_cpu_a, self.destroy_block_cpu_a, self.nav_grid )
        self.cpu_b = Enemy_B((3,3), [self.visible_sprites,self.attackable_sprites],self.obstacle_sprites, self.create_attack_cpu_b, self.destroy_attack_cpu_b, self.create_block_cpu_b, self.destroy_block_cpu_b, self.nav_grid)
        self.cpu_c = Enemy_C((4,4), [self.visible_sprites,self.attackable_sprites],self.obstacle_sprites, self.create_attack_cpu_c, self.destroy_attack_cpu_c, self.create_block_cpu_c, self.destroy_block_cpu_c, self.nav_grid)
        
        # create holder variables for the health of each player, these will be checked to determine when the game is over
        self.health_player = self.player.health
        self.health_cpu_a = self.cpu_a.health
        self.health_cpu_b = self.cpu_b.health
        self.health_cpu_c = self.cpu_c.health
        
    # place objects on the world map   
        for row_ind, row in enumerate(self.levelMap): 
            for col_ind, col in enumerate(row):
                x = col_ind * tileSize;
                y = row_ind * tileSize
                 
        # create the wall obstacles on the map
                if col == 'x':
                    Wall((x,y),[self.visible_sprites,self.obstacle_sprites])
                              
        #set the player starting location on the map
                if col == 'p':
                    self.player.set_location((x,y))
                    
        # place npc characters on the map
                if col=='a':
                    self.cpu_a.set_location((x, y)) # set location 
                    enemy_list = [self.player,self.cpu_c, self.cpu_b] #, 
                    self.cpu_a.set_opponents(enemy_list) # set list of enemy characters
                
                if col=='b':
                    self.cpu_b.set_location((x, y))
                    enemy_list = [self.player, self.cpu_a, self.cpu_c] # 
                    self.cpu_b.set_opponents(enemy_list)
                
                if col=='c':
                    self.cpu_c.set_location((x,y));
                    enemy_list = [self.player, self.cpu_a,self.cpu_b]
                    self.cpu_c.set_opponents(enemy_list)


    # handling creating the animations for the game
    def create_block_player(self):
        self.current_block_player = Shield(self.player, [self.visible_sprites, self.attack_sprites])
    
    def create_block_cpu_a(self):
        self.cpu_a_block = Shield(self.cpu_a,[self.visible_sprites, self.attack_sprites]);
        
    def create_block_cpu_b(self):
        self.cpu_b_block = Shield(self.cpu_b,[self.visible_sprites, self.attack_sprites]);
    
    def create_block_cpu_c(self):
        self.cpu_c_block = Shield(self.cpu_c,[self.visible_sprites, self.attack_sprites]);
    
    def destroy_block_player(self):
        if self.current_block_player:
            self.current_block_player.kill()
            self.player.is_block_destroyed = True;
            
    def destroy_block_cpu_a(self):
        if self.cpu_a_block:
            self.cpu_a_block.kill()
            self.cpu_a.is_block_destroyed = True;
            
    
    def destroy_block_cpu_b(self):
        if self.cpu_b_block:
            self.cpu_b_block.kill()
            self.cpu_b.is_block_destroyed = True;
    
    def destroy_block_cpu_c(self):
        if self.cpu_c_block:
            self.cpu_c_block.kill()
            self.cpu_c.is_block_destroyed = True;
    
    
    
    # handles drawing the weapon sprite of a player or cpu AI
    def create_attack(self):
       self.current_attack_player = Weapon(self.player, [self.visible_sprites, self.attack_sprites], self.player.id)
    
    def create_attack_cpu_a(self):
        self.cpu_a_attack = Weapon(self.cpu_a, [self.visible_sprites,self.attack_sprites],self.cpu_a.id)
        
    
    def create_attack_cpu_b(self):
        self.cpu_b_attack = Weapon(self.cpu_b,[self.visible_sprites,self.attack_sprites],self.cpu_b.id)
        
    
    def create_attack_cpu_c(self):
        self.cpu_c_attack = Weapon(self.cpu_c,[self.visible_sprites,self.attack_sprites],self.cpu_c.id)
        
    
    # removes a weapon animation from the game, once an attack is complete
    def destroy_attack_player(self):
        if self.current_attack_player:
            self.current_attack_player.kill()
            self.player.is_weapon_destroyed = True;
            self.current_attack_player = None;
    
    def destroy_attack_cpu_a(self):
        if self.cpu_a_attack:
            self.cpu_a_attack.kill()
            self.cpu_a_attack = None;
            self.cpu_a.is_weapon_destroyed = True;
          
            
    def destroy_attack_cpu_b(self):      
        if self.cpu_b_attack:
                self.cpu_b_attack.kill()
                self.cpu_b_attack = None;
                self.cpu_b.is_weapon_destroyed = True;
                
    
    def destroy_attack_cpu_c(self):       
        if self.cpu_c_attack:
                self.cpu_c_attack.kill()
                self.cpu_c_attack = None;
                self.cpu_c.is_weapon_destroyed = True;
                
    # handles logic for checking collisions between weapons and players 
    def attack_logic(self):
        if self.attack_sprites:
            for attack_sprite in self.attack_sprites:
               collision_sprites =  pygame.sprite.spritecollide(attack_sprite,self.attackable_sprites,False) # get collisions between sprites and weapons
               if collision_sprites:
                   for target_sprite in collision_sprites:
                       if target_sprite.sprite_type == 'cpu_ai':
                           
                           if self.current_attack_player != None: # only proceed if there is a valid weapon attack
                            if self.current_attack_player.weapon_owner_id != target_sprite.id:
                                damage = self.player.get_weapon_damage() # get the damage from the current weapon
                                target_sprite.get_damage(damage, self.current_attack_player.weapon_owner_id)  # pass the damage from
                                self.player.is_weapon_destroyed = False;
                            
                                      
    # handlers cpu_ai attacks 
    def cpu_a_attack_logic(self):
        
        if self.attack_sprites:
            for attack_sprite in self.attack_sprites:
                collision_sprites =  pygame.sprite.spritecollide(attack_sprite,self.attackable_sprites,False) # get collisions between sprites and weapons
                
                if collision_sprites:
                   for target_sprite in collision_sprites:
                       if target_sprite.sprite_type == 'cpu_ai' or 'player':
                          
                           if self.cpu_a_attack != None: # only proceed if there is a valid weapon attack
                            
                            if self.cpu_a_attack.weapon_owner_id == self.cpu_a.id:
                                if self.cpu_a_attack.weapon_owner_id != target_sprite.id:  # check that the owner of a weapon isnt taking damange for its own weapon sprite 
                                    damage = self.cpu_a.get_weapon_damage() # get the damage from the current weapon
                                    
                                    target_sprite.get_damage(damage, self.cpu_a_attack.weapon_owner_id)  # pass the damage from
                                    self.cpu_a.is_weapon_destroyed = False;
                                
    
    def cpu_b_attack_logic(self):
       if self.attack_sprites:
            for attack_sprite in self.attack_sprites:
                collision_sprites =  pygame.sprite.spritecollide(attack_sprite,self.attackable_sprites,False) # get collisions between sprites and weapons
                
                if collision_sprites:
                   for target_sprite in collision_sprites:
                       if target_sprite.sprite_type == 'cpu_ai' or 'player':
                          
                           if self.cpu_a_attack != None: # only proceed if there is a valid weapon attack
                            
                            if self.cpu_a_attack.weapon_owner_id == self.cpu_a.id:
                                if self.cpu_a_attack.weapon_owner_id != target_sprite.id:  # check that the owner of a weapon isnt taking damange for its own weapon sprite 
                                    damage = self.cpu_a.get_weapon_damage() # get the damage from the current weapon
                                    
                                    target_sprite.get_damage(damage, self.cpu_a_attack.weapon_owner_id)  # pass the damage from
                                    self.cpu_a.is_weapon_destroyed = False;
    
    
    def cpu_c_attack_logic(self):
        if self.attack_sprites:
            for attack_sprite in self.attack_sprites:
                collision_sprites =  pygame.sprite.spritecollide(attack_sprite,self.attackable_sprites,False) # get collisions between sprites and weapons
                
                if collision_sprites:
                   for target_sprite in collision_sprites:
                       if target_sprite.sprite_type == 'cpu_ai' or 'player':
                          
                           if self.cpu_a_attack != None: # only proceed if there is a valid weapon attack
                            
                            if self.cpu_a_attack.weapon_owner_id == self.cpu_a.id:
                                if self.cpu_a_attack.weapon_owner_id != target_sprite.id:  # check that the owner of a weapon isnt taking damange for its own weapon sprite 
                                    damage = self.cpu_a.get_weapon_damage() # get the damage from the current weapon
                                    
                                    target_sprite.get_damage(damage, self.cpu_a_attack.weapon_owner_id)  # pass the damage from
                                    self.cpu_a.is_weapon_destroyed = False;
    
    
    # check the status of the players, is the game over?             
    def isGameOver(self):
        pass
        
    
    # function for testing to show the stats of the current character weapons
    def show_weapon_owners(self):
        
        if self.current_attack_player != None: # only proceed if there is a valid weapon attack
            print("player weapon owner: ", self.current_attack_player.weapon_owner_id)
        
        if self.cpu_a_attack != None:
            print("cpu a weapon owner: ", self.cpu_a_attack.weapon_owner_id)
        
    
    # loop to update and draw the game           
    def run(self):
        
        self.visible_sprites.custom_draw(self.player)
        # handle the attack logic and animations for all characters
        
        if self.current_attack_player:
            self.attack_logic()
        
        # only run attack logic if a cpu player is still alive..
        if self.cpu_a_attack != None and self.health_cpu_a > 0:
                self.cpu_a_attack_logic()
        
        if self.cpu_b_attack != None and self.health_cpu_b > 0:
                self.cpu_b_attack_logic()
          
        if self.cpu_c_attack != None and self.health_cpu_c > 0:
                self.cpu_c_attack_logic()
        
        
        self.visible_sprites.update();
    
    
# class to create a camera view focused on the player     
class CameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.half_width = self.display_surface.get_size()[0] // 2;
        self.half_height = self.display_surface.get_size()[1] // 2 ;
        self.offset = pygame.math.Vector2();
        
    # draw the player in relation to the camera view
    def custom_draw(self,player):
        self.offset.x = player.rect.centerx - self.half_width;
        self.offset.y = player.rect.centery - self.half_height;
        for sprite in sorted(self.sprites(),key = lambda sprite: sprite.rect.centery):
            offset_pos = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image,offset_pos)
            
