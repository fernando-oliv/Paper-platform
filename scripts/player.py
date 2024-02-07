import pygame
import numpy as np
import matplotlib.pyplot as plt
from pygame.locals import *
from scipy.signal import correlate
import cv2
from PIL import Image
import math
import tkinter
from tkinter import filedialog
from object import Object
from playerMovement import playerMovement
from LivingBeings import LivingBeings

class Player(LivingBeings):
    def __init__(self):
        self.width = 31  # Set the player width and height
        self.height = 45
        self.x = 50    # Set the player positions 
        self.y = 200
        self.vel = 5
        self.life = 4
        self.max_jump = 1
        self.jump_height = 18
        self.jump_count = self.max_jump
        self.collisorlist = []
        self.gravity = 7
        self.jumpingTime = 0
        self.jumping = False
        self.walking = False
        self.falling = True
        self.facingRight = True
        self.sprite = pygame.image.load("../sprites/player/playerIdle0.png")
        self.sprites = Object()
        self.sprites.idle = self.sprite
        self.sprites.walking = []
        self.sprites.walking.append(pygame.image.load("../sprites/player/playerWalk0.png"))
        self.sprites.walking.append(pygame.image.load("../sprites/player/playerWalk1.png"))
        self.sprites.walking.append(pygame.image.load("../sprites/player/playerWalk2.png"))
        self.sprites.walking.append(pygame.image.load("../sprites/player/playerWalk3.png"))
        self.sprites.walking.append(pygame.image.load("../sprites/player/playerWalk4.png"))
        self.sprites.walking.append(pygame.image.load("../sprites/player/playerWalk5.png"))
        self.sprites.jumping = pygame.image.load("../sprites/player/playerJump0.png")
        self.sprites.falling = pygame.image.load("../sprites/player/playerFall0.png")
        self.sprites.attacking = []
        self.sprites.attacking.append(pygame.image.load("../sprites/player/playerAttack0.png"))
        self.sprites.attacking.append(pygame.image.load("../sprites/player/playerAttack1.png"))
        self.sprites.attacking.append(pygame.image.load("../sprites/player/playerAttack2.png"))
        self.sprites.attacking.append(pygame.image.load("../sprites/player/playerAttack3.png"))
        self.sprites.attack = pygame.image.load("../sprites/Attack.png")
        self.currentSprite = 0
        self.walkingSpeed = 0.25
        self.attackingSpeed = 0.25
        self.hurting = False
        self.attacking = False
        self.attackingTimer = 0
        self.init = pygame.time.get_ticks()
        self.end = self.init
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.attackRect = None
        self.attackSprite = -1
    
    def flip(self):
        self.facingRight = not self.facingRight
        #self.sprite = pygame.transform.flip(self.sprite, True, False)
        
    def move(self):
        self.rect = playerMovement(self)
        self.diff = pygame.time.get_ticks() - self.init

    def hurt(self):
        
        
        if not self.hurting:
            
            self.hurting = True
            self.life -= 1
            self.init = pygame.time.get_ticks()
        elif self.diff >= 3000:
            self.hurting = False

    def attack(self):
        if self.attacking == False:
            self.attacking = True
            self.attackSprite = 0.0

        '''
        elif self.attacking and self.attackingTimer <= 50:
            print(self.attackingTimer)
            self.attackingTimer += 10
            right = 1 if self.facingRight else -1
            self.attackRect = pygame.Rect(self.x + right * (20 * self.currentSprite), self.y - 30 +  (13 * self.currentSprite), 38, 10)
    
        elif self.attacking and self.attackingTimer > 100:
            self.attacking = False
            self.attackRect = None
            self.attackingTimer = 0
            self.attackRect = None
        '''
        
            
        
    
    def animationController(self):
        

        if self.attacking:
            if self.attackSprite >= int(len(self.sprites.attacking)):
                self.attackingTimer = -1
                self.attacking = False 
                self.attackRect = None

            elif self.attackSprite > -1:
                self.sprite = self.sprites.attacking[int(self.attackSprite)]
                right = 1 if self.facingRight else -1
                self.attackRect = pygame.Rect(self.x + right * (20 * self.currentSprite), self.y - 30 +  (13 * self.currentSprite), 38, 10)
                self.attackSprite += self.attackingSpeed

        elif self.hurting:
            if self.diff >= 3000:
                self.hurting = False
            
            
        elif self.jumping:
            self.currentSprite = 0
            self.sprite = self.sprites.jumping
        elif self.falling:
            self.currentSprite = 0
            self.sprite = self.sprites.falling
        elif self.walking == True:
            self.currentSprite += self.walkingSpeed
            
            if self.currentSprite >= len(self.sprites.walking):
                self.currentSprite = 0
            
            self.sprite = self.sprites.walking[int(self.currentSprite)]
        else:
            self.currentSprite = 0
            self.sprite = self.sprites.idle
        if not self.facingRight:
            self.sprite = pygame.transform.flip(self.sprite, True, False)

        