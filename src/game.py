import pygame, sys
from settings import *

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((window_width, window_height))
        self.clock = pygame.time.Clock()
    
    def create(self):
        print("how many characters? ")
    # get user input for # of characters
    
    # create the map
    #createMap(); 
    
    # create the characters 
    # createChars();
    
    # primary game loop
    def run(self):
        
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.screen.fill('black')
            
            pygame.display.update()
            self.clock.tick(FPS)

if __name__ == '__main__':
    game = Game();
    game.run();
