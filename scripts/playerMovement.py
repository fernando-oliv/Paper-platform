import pygame
import numpy as np
from pygame.locals import *
from scipy.signal import correlate
from PIL import Image
from tkinter import filedialog
from object import Object


def playerMovement(object):
    auxX = object.x
    auxY = object.y
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        object.walking = True
        auxX -= object.vel
        if object.facingRight:
            object.flip()
    elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        object.walking = True
        auxX += object.vel
        if not object.facingRight:
            object.flip()
    if keys[pygame.K_SPACE] or keys[pygame.K_z]:
        if object.jumpingTime < 20 and object.jump_count > 0:
            object.walking = False
            object.falling = False
            object.jumping = True
            auxY -= object.jump_height
            object.jumpingTime += 1
    elif object.jumping:
        object.jumping = False
        object.jump_count -= 1 if object.jump_count > 0 else 0
        object.jumpingTime = 0
    else:
        if not (keys[pygame.K_RIGHT] or keys[pygame.K_d] or keys[pygame.K_LEFT] or keys[pygame.K_a]):
            object.walking = False
    auxY += object.gravity
    auxYStair = object.y - 14
    flagStairX = False
    flagStairY = False
    temprectX = pygame.Rect(auxX, object.y, object.width, object.height)
    temprectY = pygame.Rect(object.x, auxY, object.width, object.height)
    temprectYStair = pygame.Rect(auxX, auxYStair,  object.width, object.height)
    flagX, flagY = True, True
    
    for temp in object.collisorlist:
        if flagX:
            if temprectX.colliderect(temp):
                flagX = False
                #verificação se passo de escada pode ser feito
                if keys[pygame.K_LEFT] or keys[pygame.K_a] or keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                    if temprectYStair.colliderect(temp) == False:
                        flagStairX = True
        if flagY:
            if flagStairX == True and keys[pygame.K_LEFT] or keys[pygame.K_a] or keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                if temprectYStair.colliderect(temp) == False:
                    flagStairY = True
                    
            if temprectY.colliderect(temp):
                flagY = False
                object.jump_count = object.max_jump
                if flagX == False:
                    break
    if flagX:    
        object.x = auxX
    if flagY:
            if auxY > object.y:
                object.falling = True
            else:
                object.falling = False
            object.y = auxY
    else:
        object.falling = False
    
    
    if flagStairX and flagStairY:
        object.x = auxX
        object.y = auxYStair
    return pygame.Rect(object.x, object.y, object.width, object.height)

    