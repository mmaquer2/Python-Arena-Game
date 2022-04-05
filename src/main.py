import pygame, sys
from pathlib import Path
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
        
        # load music
        main_music = Path("src/music/main.wav")
        
        # play music
        #main_sound = pygame.mixer.Sound('music')
        #main_sound.set_volume(0.5)
        #main_sound.play(loops = -1);
  
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
            
            # starting screen and level count down...
             
            self.level.run();
            pygame.display.update()
            self.clock.tick(FPS)


# Calls the main game start and loop
if __name__ == '__main__':
    game = Game();
    
    # run the game
    game.run();
