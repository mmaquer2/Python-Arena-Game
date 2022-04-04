import pygame, sys

# import game support classes
from settings import *
from level import Level 


# main game loop class
class Game:
    def __init__(self):
        
        # set up game window and object 
        pygame.init()
        pygame.display.set_caption('Arena Game by Mike Maquera')
        self.screen = pygame.display.set_mode((window_width, window_height))
        self.clock = pygame.time.Clock()
        
        # init game level and map
        self.level = Level();
    
    #create players 
    def createPlayers(self, numOfPlayers):
        print("creating players... ", numOfPlayers)
        
        
    
    # primary game loop
    def run(self):
        
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
            #run level and levelMap
            self.screen.fill('black')
            self.level.run();
            pygame.display.update()
            self.clock.tick(FPS)



# this calls the main game start and loop
if __name__ == '__main__':
    game = Game();

    # create players 
    # numOfPlayers = input("how many cpu players would you like to play?" )
    #game.createPlayers(numOfPlayers);

    # run the game
    game.run();
