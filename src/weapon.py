import pygame

# class to handle the dirction and animations for the different weapon types
class Weapon(pygame.sprite.Sprite):
    def __init__(self,player,groups):
        super().__init__(groups)
        
        # remove idle type to obtain only player direction 
        direction = player.status.split('_')[0]; # get the current direction of the player to point weapon in correct direction
        print(direction)
        
        self.image = pygame.Surface((40,40))
        
        if direction == 'right':
            self.rect = self.image.get_rect(midleft = player.rect.midright + pygame.math.Vector2(0,16)) # move weapon image down to players hand
        
        elif direction == 'left':
            self.rect = self.image.get_rect(midright = player.rect.midleft + pygame.math.Vector2(0,16)) 
        
        elif direction == 'down':
            self.rect = self.image.get_rect(midtop = player.rect.midbottom + pygame.math.Vector2(-10,0)) 
        
        elif direction == 'up':
                self.rect = self.image.get_rect(midbottom = player.rect.midtop + pygame.math.Vector2(0,16)) 
        
      
        
        
        