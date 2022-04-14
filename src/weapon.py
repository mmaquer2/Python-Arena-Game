import pygame

from arrow import Arrow

# class to handle the dirction and animations for the different weapon types
class Weapon(pygame.sprite.Sprite):
    def __init__(self,player,groups,weapon_owner):
        super().__init__(groups)
        
       
        self.sprite_type = 'weapon'
        self.weapon_owner_id = weapon_owner  # set the original owner of the weapon, so the owner cannot be hit by their own weapon
        
        # remove idle type to obtain only player direction 
        direction = player.status.split('_')[0]  # get the current direction of the player to point weapon in correct direction
        
        # src\sprites\weapons\axe example of folder path to weapon sprite
        weapon_path = f'sprites/weapons/{player.weapon}/{direction}.png' # path to the graphic of the weapon
        self.image = pygame.image.load(weapon_path).convert_alpha()
        
        # create the weapon sprite based on the current direction
        if direction == 'right':
            self.rect = self.image.get_rect(midleft = player.rect.midright + pygame.math.Vector2(0,16)) # move weapon image down to players hand
        
        elif direction == 'left':
            self.rect = self.image.get_rect(midright = player.rect.midleft + pygame.math.Vector2(0,16)) 
        
        elif direction == 'down':
            self.rect = self.image.get_rect(midtop = player.rect.midbottom + pygame.math.Vector2(-10,0)) 
        
        elif direction == 'up':
                self.rect = self.image.get_rect(midbottom = player.rect.midtop + pygame.math.Vector2(0,16)) 
        

        # if the weapon is a bow, create an arrow
        if player.weapon == "bow":
            
            x,y = player.get_location()
            if direction == "right":
                print("fire right")
                Arrow(groups,player,"right")
                
            
            if direction == "left":
                print("fire left")
                Arrow(groups,player,'left')
                
            
            if direction == "down":
                print("fire down")
                Arrow(groups,player,'down')
            
            if direction == "up":
                print("fire up")
                Arrow(groups,player,"up")
            
            
            
            
        
        
        