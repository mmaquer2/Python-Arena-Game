import pygame

# class to create the shield to block enemy attacks during the game
class Shield(pygame.sprite.Sprite):
    def __init__(self,player,groups):
        super().__init__(groups)
        
        direction = player.status.split('_')[0]
        
        block_path = f'sprites/weapons/{player.weapon}/{direction}.png' # path to the graphic of the weapon
        self.image = pygame.image.load(block_path).convert_alpha()
        
        
        # in order to make the sheild an obstacle that blocks attacks need to create a hitbox as well 
        #self.hitbox = self.rect.inflate(0,-10)
        
        # what does hitbox do?