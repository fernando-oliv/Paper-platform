from LivingBeings import LivingBeings
import pygame.time

class Enemy(LivingBeings):
    def __init__(self):
        self.life = 1
        self.movSpeed = 3
        self.damage = 1
        self.x = 0
        self.y = 0
    
    #inimigos não tem o bonus de invicibilidade quando são atingidos
    def hurt(self):
        self.life -= 1