import pygame, sys

# import game support classes
from settings import *
from level import *
from entity import *

# main game loop class
class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption('Arena Game by Mike Maquera')
        self.screen = pygame.display.set_mode((window_width, window_height))
        self.clock = pygame.time.Clock()
    
    #create players 
    def createPlayers(self):
        print("creating players... ")
    
    # create map
    def createMap(self):
        print("creating map... ")
    
    # primary game loop
    def run(self):
        
        while True:
            for event in pygame.event.get():
                
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                #user actions
                    
            self.screen.fill('black')
            #run level and levelMap
            
            # opponent actions
            
            
            pygame.display.update()
            self.clock.tick(FPS)



# this calls the main game start and loop
if __name__ == '__main__':
    game = Game();
    
    # create players 
    #game.createPlayers();
    
    # create the map
    #game.createMap();
    
    # run the game
    game.run();
