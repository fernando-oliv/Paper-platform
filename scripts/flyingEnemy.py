import pygame.image
from enemy import Enemy
from object import Object
import math

class FlyingEnemy(Enemy):
    def __init__(self, player, x, y):
        super().__init__()
        self.x = x
        self.y = y
        self.player = player
        self.rect = pygame.Rect(self.x, self.y, self.player.width, self.player.height)
        self.sprites = Object()
        self.sprites.flying = []
        self.sprites.flying.append(pygame.image.load("../sprites/inimigo/enemy0.png"))
        self.sprites.flying.append(pygame.image.load("../sprites/inimigo/enemy1.png"))
        self.sprite = self.sprites.flying[0]
        self.facingRight = True
        self.currentSprite = 0
        self.spriteSpeed = 0.25

    def move(self):
        
        module =  math.sqrt( (self.x - self.player.x)**2 + (self.y - self.player.y)**2 )
        if module == 0 or module is None:
            return

        #print('module ', module)
        newposition = (int((self.player.x - self.x)/module * self.movSpeed) , int((self.player.y - self.y)/module * self.movSpeed))
        #print('old ', (self.x, self.y))
        if newposition[0] >= 0:
            self.facingRight = True
        else:
            self.facingRight = False
        self.x += newposition[0]
        self.y += newposition[1]

        self.currentSprite += self.spriteSpeed
        if self.currentSprite >= len(self.sprites.flying):
                self.currentSprite = 0
        self.sprite = self.sprites.flying[int(self.currentSprite)]
        if not self.facingRight:
            self.sprite = pygame.transform.flip(self.sprite, True, False)


        self.rect = pygame.Rect(self.x, self.y, 39, 36)

        return self.rect
        