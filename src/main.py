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
        game_window = (1280, 736)
        self.screen = pygame.display.set_mode(game_window)
        self.background = pygame.Surface(game_window)
        self.screen.blit(self.background, (0,0))
          
        # set game icon on window tab 
        icon_path = Path('sprites/characters/player/down_idle/idle_down.png') 
        icon = pygame.image.load(icon_path)
        pygame.display.set_icon(icon)
        self.clock = pygame.time.Clock()
               
        # load music 
        main_music = Path('music/battle_music.wav')
        main_sound = pygame.mixer.Sound(main_music) # play music   
        main_sound.set_volume(0.1)
        main_sound.play(loops = -1) # keep looping the music
  
        # init game level and map   
        self.level = Level()
    
    # primary game loop
    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                    
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        print("Escape Key Pressed Quitting Game...")
                        pygame.quit()
                        sys.exit()
       
            self.screen.fill('light green') # background color
            
            self.level.run();   # update the level at each tick
            pygame.display.update()
            self.clock.tick(FPS)
                

# Calls the game start and loop
if __name__ == '__main__':
    game = Game();
    
    # run the game
    game.run()
