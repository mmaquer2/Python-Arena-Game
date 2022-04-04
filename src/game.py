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
        
        # get the number of AI players from the player
        #numOfPlayers = int(input("how many cpu players would you like to play? 1- 3 " ))
        
        # init game level and map
        self.level = Level();
    
   
    # primary game loop
    def run(self):
        
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
            self.screen.fill('light green') # background color 
            self.level.run();
            pygame.display.update()
            self.clock.tick(FPS)



# this calls the main game start and loop
if __name__ == '__main__':
    game = Game();
    
    # run the game
    game.run();
