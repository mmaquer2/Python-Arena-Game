import pygame

# class to create the shield to block enemy attacks during the game
class Shield(pygame.sprite.Sprite):
    def __init__(self,player,groups):
        super().__init__(groups)
        
        self.sprite_type = 'shield'
        self.shield_owner_id = player.id        
           
        direction = player.status.split('_')[0]
        direction = player.status.split('_')[0] 
        print(direction)
        
        #block_path = f'sprites/weapons/shield/{direction}.png' # path to the graphic of the weapon
        block_path = f'sprites/shield/{direction}.png'
        
        self.image_import = pygame.image.load(block_path) # import image 
        self.image = pygame.transform.scale(self.image_import,(40,40))
     
        
        # in order to make the sheild an obstacle that blocks attacks need to create a hitbox as well 
        #self.hitbox = self.rect.inflate(0,-10)
        
        # what does hitbox do?
        
        if direction == 'right':
            print("blocking right")    
            self.rect = self.image.get_rect(midleft = player.rect.midright)
        
        elif direction == 'left':
            print("blocking left")    
            self.rect = self.image.get_rect(midright = player.rect.midleft )
            
        elif direction == 'down':
            
            print("blocking down")    
            self.rect = self.image.get_rect(midtop = player.rect.midbottom + pygame.math.Vector2(-10,0)) 
        
        elif direction == 'up':
            print("blocking up")
            self.rect = self.image.get_rect(midbottom = player.rect.midtop + pygame.math.Vector2(0,16))