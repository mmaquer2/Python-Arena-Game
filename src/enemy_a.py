import pygame
import random
from settings import *


class Enemy_A(pygame.sprite.Sprite):
    def __init__(self,pos,groups,obstacle_sprites,create_attack,destroy_attack):
        super().__init__(groups)
        
        self.import_animations();
        
        # direction and status vars
        self.status = 'down'
        self.frame_index = 0;
        self.animation_speed = 0.15;
        self.direction = pygame.math.Vector2()

        
        self.create_attack = create_attack;
        weaponRandomAssignment = random.randint(0,len(weapon_data) - 1);
        self.weapon_index = weaponRandomAssignment;
        self.weapon = list(weapon_data.keys())[self.weapon_index];
        self.destroy_attack = destroy_attack;
            
    
    
    def import_animations(self):
        pass
    
    
    
    
    def move(self):
        pass
    
    
    def get_status(self):
        pass
    
    def collision(self):
        pass
    
    # make some sort of decision based on the game AI behavior Tree
    def decide(self):
        pass
    
    def animate(self):
        pass
    
    
    def cool_down(self):
        pass

        
    def update(self):
        
        self.get_status()
        self.animate();
        
        self.decide();
        
        self.cool_down();
        self.move();
    