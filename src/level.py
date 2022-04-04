
import pygame,sys
import random
from settings import *
from wall import Wall
from floor import Floor
from player import Player

# class to handle running the level for the game state
class Level:
    
    def __init__(self):

        # create game sprites
        self.display_surface = pygame.display.get_surface();
        
        # create the camera view to focus on the player 
        self.visible_sprites = CameraGroup()
        self.obstacle_sprites = pygame.sprite.Group();
        
        self.createMap(); # init map starting locations for obstacles and players 
    
    def createMap(self):
        
        # Select Map
        # randomize what map is being selected from the world maps in the settings 
        mapNum = random.randint(0, 2)
        if(mapNum == 0):
            levelMap = WORLD_MAP_ONE
        if(mapNum == 1):
            levelMap = WORLD_MAP_TWO
        if(mapNum == 2):
            levelMap = WORLD_MAP_THREE
        
        # Create random Traps
        
        # append trap to level map, such as t = bear trap, f = flame 
         
    
        # TODO: make the x,p into a list, and push what the items will be to account for the 
        # selected number of players 
        
        for row_ind,row in enumerate(WORLD_MAP_THREE):
            for col_ind, col in enumerate(row):
                x = col_ind * tileSize;
                y = row_ind * tileSize
                # set what each tile will represent on the world map
                # create the wall obstacles on the map
                if col == 'x':
                    Wall((x,y),[self.visible_sprites,self.obstacle_sprites])

                #create the player on the map
                if col == 'p':
                    self.player = Player((x,y), [self.visible_sprites], self.obstacle_sprites)
                
    
    # loop to update and draw the game           
    def run(self):
        self.visible_sprites.custom_draw(self.player)
        self.visible_sprites.update();
    
    
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
            
            