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

testeReal = True


class Object(object): #classe generica para atribuição de atributos
    pass


class Player:
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
        self.sprite = pygame.image.load("sprites/player/playerIdle0.png")
        self.sprites = Object()
        self.sprites.idle = self.sprite
        self.sprites.walking = []
        self.sprites.walking.append(pygame.image.load("sprites/player/playerWalk0.png"))
        self.sprites.walking.append(pygame.image.load("sprites/player/playerWalk1.png"))
        self.sprites.walking.append(pygame.image.load("sprites/player/playerWalk2.png"))
        self.sprites.walking.append(pygame.image.load("sprites/player/playerWalk3.png"))
        self.sprites.walking.append(pygame.image.load("sprites/player/playerWalk4.png"))
        self.sprites.walking.append(pygame.image.load("sprites/player/playerWalk5.png"))
        self.sprites.jumping = pygame.image.load("sprites/player/playerJump0.png")
        self.sprites.falling = pygame.image.load("sprites/player/playerFall0.png")
        self.sprites.attacking = []
        self.sprites.attacking.append(pygame.image.load("sprites/player/playerAttack0.png"))
        self.sprites.attacking.append(pygame.image.load("sprites/player/playerAttack1.png"))
        self.sprites.attacking.append(pygame.image.load("sprites/player/playerAttack2.png"))
        self.sprites.attacking.append(pygame.image.load("sprites/player/playerAttack3.png"))
        self.sprites.attack = pygame.image.load("sprites/Attack.png")
        self.currentSprite = 0
        self.walkingSpeed = 0.25
        self.attackingSpeed = 0.25
        self.hurting = False
        self.attacking = False
        self.attackingTimer = 0
        self.init = pygame.time.get_ticks()
        self.end = self.init
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
    
    def flip(self):
        self.facingRight = not self.facingRight
        #self.sprite = pygame.transform.flip(self.sprite, True, False)

    def move(self):
        auxX = self.x
        auxY = self.y
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.walking = True
            auxX -= self.vel
            if self.facingRight:
                self.flip()
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.walking = True
            auxX += self.vel
            if not self.facingRight:
                self.flip()
        if keys[pygame.K_SPACE] or keys[pygame.K_z]:
            if self.jumpingTime < 20 and self.jump_count > 0:
                self.walking = False
                self.falling = False
                self.jumping = True
                auxY -= self.jump_height
                self.jumpingTime += 1
        elif self.jumping:
            self.jumping = False
            self.jump_count -= 1 if self.jump_count > 0 else 0
            self.jumpingTime = 0
        else:
            if not (keys[pygame.K_RIGHT] or keys[pygame.K_d] or keys[pygame.K_LEFT] or keys[pygame.K_a]):
                self.walking = False

        auxY += self.gravity
        auxYStair = self.y - 14
        flagStairX = False
        flagStairY = False
        temprectX = pygame.Rect(auxX, self.y, self.width, self.height)
        temprectY = pygame.Rect(self.x, auxY, self.width, self.height)
        temprectYStair = pygame.Rect(auxX, auxYStair,  self.width, self.height)
        flagX, flagY = True, True
        

        for temp in self.collisorlist:
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
                    self.jump_count = self.max_jump
                    if flagX == False:
                        break
        if flagX:    
            self.x = auxX
        if flagY:
                if auxY > self.y:
                    self.falling = True
                else:
                    self.falling = False
                self.y = auxY
        else:
            self.falling = False
        
        
        if flagStairX and flagStairY:
            self.x = auxX
            self.y = auxYStair
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        
        self.diff = pygame.time.get_ticks() - self.init
        if self.diff >= 3000:
            self.hurting = False

        if keys[pygame.K_x] or keys[pygame.K_k]:
            self.attacking = True
        elif self.attacking and self.attackingTimer <= 100:
            self.attackingTimer += 10
        elif self.attacking and self.attackingTimer > 100:
            self.attacking = False
            self.attackingTimer = 0

    def hurt(self):
        #diff = pygame.time.get_ticks() - self.init
        
        if not self.hurting:
            self.hurting = True
            self.life -= 1
            self.init = pygame.time.get_ticks()
        elif self.diff >= 3000:
            self.hurting = False
            
        
    
    def animationController(self):
        

        if self.attacking and self.attackingTimer < 50:
            self.currentSprite += self.attackingSpeed
            
            if self.currentSprite >= len(self.sprites.attacking):
                self.currentSprite = 0
            
            self.sprite = self.sprites.attacking[int(self.currentSprite)]

            right = 1 if self.facingRight else -1
            attackRect = pygame.Rect(self.x + right * (20 * self.currentSprite), self.y - 30 +  (13 * self.currentSprite), 38, 10)
            

            collide = attackRect.collidelistall(enemies)
            if  collide is not []:
                for index in collide:
                    enemies[index].hurt()

            
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


enemies = []
score = 0
highscore = score

class Enemy:
    def __init__(self, index):
        self.life = 1
        self.movSpeed = 3
        self.damage = 1
        self.x = 0
        self.y = 0
        self.hurting = False
        self.init = 0
        self.index = index
    
    def hurt(self):
        diff = pygame.time.get_ticks() - self.init
        if not self.hurting:
            self.hurting = True
            self.life -= 1
            self.init = pygame.time.get_ticks()
        elif diff >= 100:
            self.hurting = False
    
class FlyingEnemy(Enemy):
    def __init__(self, player, x, y, index):
        super().__init__(index)
        self.x = x
        self.y = y
        self.player = player
        self.rect = pygame.Rect(self.x, self.y, self.player.width, self.player.height)
        self.sprites = Object()
        self.sprites.flying = []
        self.sprites.flying.append(pygame.image.load("sprites/inimigo/enemy0.png"))
        self.sprites.flying.append(pygame.image.load("sprites/inimigo/enemy1.png"))
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
        #print('new ', newposition)

        

        
        if self.rect.colliderect(self.player.rect):
            self.player.hurt()
        if self.life == 0:
            global score
            score += 100
            enemies.remove(self)

        

        

class App:
    def __init__(self, dir):
        self._running = True
        if testeReal:
            self.size = self.weight, self.height = 800, 600
        else:
            self.size = self.weight, self.height = 640, 400
        pygame.init()
        pygame.font.get_init()
        self.TEXT_FONT = pygame.font.Font("font.otf")
        self.display = pygame.display.set_mode([self.weight, self.height])
        self.player = Player()
        borders = []
        borders.append(pygame.Rect(-1, 0, 1, self.height))
        borders.append(pygame.Rect(0, -1, self.weight, 1))
        borders.append(pygame.Rect(self.weight+1, 0, 1, self.height))
        borders.append(pygame.Rect(0, self.height+1, self.weight+1, 1))
        self.player.collisorlist = borders
        self.allrect = []
        self.img = pygame.image.load(dir)
        self.heart = pygame.image.load("sprites/Heart.png")
        self.waves = 3
        self.currentWave = 1
        self.delay = self.currentWave
        self.init = pygame.time.get_ticks()
        self.timer = 5
        pygame.time.set_timer(pygame.USEREVENT, 500)

        
        '''
        for wave in range(self.waves):
            for i in range(0, wave+1):
                enemies.append(FlyingEnemy(self.player, 0, 0, i))
                enemies.append(FlyingEnemy(self.player, self.weight, 0, i+1))
        '''
        
        
        
  
    def on_event(self, event):
        if event.type == pygame.USEREVENT:
            self.timer -= 1
        if event.type == pygame.QUIT:
            self._running = False

    def on_load(self):
        #load new level
        pass

    def on_cleanup(self):
        #clears previously loaded levels
        pass

    def on_quit(self):
        #close the aplication
        pass

    def on_win(self):
        pass

    def draw_window(self):
        self.display.blit(self.img, (0,0))
        score_text = self.TEXT_FONT.render(f'SCORE {score}', False, (0, 0, 0))
        wave_text = self.TEXT_FONT.render(f'WAVE {self.currentWave}', False, (0, 0, 0))
        #highscore_text = self.TEXT_FONT.render(f'HIGHSCORE {highscore}', False, (0, 0, 0))
        self.display.blit(score_text, (self.weight - score_text.get_width() - 20, 15))

        self.display.blit(wave_text, (self.weight /2, 15))

        #self.display.blit(highscore_text, (self.weight - score_text.get_width() - 20, 35))
        #pygame.draw.rect(self.display, (255, 0, 0), (self.player.x, self.player.y, self.player.width, self.player.height), 3)
        if self.player.hurting and (pygame.time.get_ticks() - self.player.init ) % 100 > 50:
            pass
        else:
            self.display.blit(self.player.sprite, (self.player.x, self.player.y))

        if self.player.attacking:
            right = 1
            temp = self.player.sprites.attack
            if not self.player.facingRight:
                temp = pygame.transform.flip(temp, True, False)
                right = -1
            rotatedImage = pygame.transform.rotate(temp, right * -30 * self.player.currentSprite)
            self.display.blit(rotatedImage, (self.player.x + right * (20 * self.player.currentSprite), self.player.y - 30 +  (13 * self.player.currentSprite)))

        for enemy in enemies:
            #pygame.draw.rect(self.display, (255, 0, 0), (enemy.x, enemy.y, self.player.width, self.player.height), 3)
            self.display.blit(enemy.sprite, (enemy.x, enemy.y))
        if not testeReal:
            for temp in self.allrect:
                pygame.draw.rect(self.display, (0, 255, 0), temp, 3)
            
        for i in range(self.player.life):
            self.display.blit(self.heart, (i*35, 0))
        
        pygame.display.update()

    def updateWave(self):
        #print(self.delay, enemies)
        if self.delay == 0 and enemies == []:
            self.currentWave += 1
            self.player.life += 1 if self.player.life <= 3 else 0
            self.timer = 5
            self.delay = self.currentWave
        
        if self.timer == 0 and self.delay > 0:
            enemies.append(FlyingEnemy(self.player, 0, 0, i))
            enemies[0].movSpeed = 3 + 0.25*self.currentWave
            enemies.append(FlyingEnemy(self.player, self.weight, 0, i+1))
            self.timer = self.delay
            pygame.time.set_timer(pygame.USEREVENT, 500)
            self.delay -= 1


    def on_execute(self):
        
        if( self._running ):
            for event in pygame.event.get():
                self.on_event(event)

            self.player.move()
            for enemy in enemies:
                enemy.move()
            self.player.animationController()
            self.updateWave()
            self.draw_window()
            if self.player.life == 0:
                self._running = False
            return True
        else:

            return False
 


def process_frame(img2, app):
    img2 = cv2.resize(img2, (800, 600))
    app.img2 = img2
    img3 = cv2.cvtColor(img2, cv2.COLOR_BGR2RGB)
    im1 = Image.fromarray(img3)
    im1.save('temp.png')
    app.img = pygame.image.load("temp.png")
    global score
    global highscore
    if score > highscore:
        highscore = score
    lower_color = np.array([80, 25, 30])
    upper_color = np.array([130, 255, 255])
    img_hsv = cv2.cvtColor(img2, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(img_hsv, lower_color, upper_color)
    '''
    cv2.imshow('mask', mask)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    '''
    ind_x, ind_y = np.where(mask == 255)
    i = 0
    app.allrect = []
    app.player.collisorlist = []
    app.player.life = 4
    app.player.x = 50
    app.player.y = 200
    lower_color = np.array([138, 30, 20])
    upper_color = np.array([179, 255, 255])
    mask1 = cv2.inRange(img_hsv, lower_color, upper_color)

    lower_color = np.array([0, 30, 20])
    upper_color = np.array([10, 255, 255])
    mask2 = cv2.inRange(img_hsv, lower_color, upper_color)
    mask1 = np.add(mask1, mask2)
    

    spawny, spawnx = np.where(mask1 == 255)
    '''
    if spawnx is not ([] or None) and len(spawnx) > 0:
        theApp.player.x = spawnx[0] + 10
        theApp.player.y = spawny[0]
        #print(theApp.player.x)
        #print(theApp.player.y)
    '''
    for ind in ind_x:
        temp = pygame.Rect(ind_y[i], ind, 1, 1)
        app.allrect.append(temp)
        app.player.collisorlist.append(temp)
        i += 1

    global enemies
    enemies = []
    app.delay = 0
    app.currentWave = 0

def prompt_file():
    """Create a Tk file dialog and cleanup when finished"""
    top = tkinter.Tk()
    top.withdraw()  # hide window
    file_name = tkinter.filedialog.askopenfilename(parent=top)
    top.destroy()
    return file_name

if __name__ == "__main__" :


    dir = "testeRealresized3.jpg"

    
    if testeReal:
        img2 = cv2.imread(dir)
        lower_color = np.array([100, 25, 30])
        upper_color = np.array([120, 255, 255])
    
    else: 
        img2 = cv2.imread("retangulo2.png")
        lower_color = np.array([0, 0, 0])
        upper_color = np.array([0, 0, 0])
    
    img_hsv = cv2.cvtColor(img2, cv2.COLOR_BGR2HSV)
    img_rgb = cv2.cvtColor(img_hsv, cv2.COLOR_HSV2RGB)


    
    
    
    #retorna uma imagem binaria onde os valores encontrados 
    #estão dentro dos limtes de lower_color e upper_color
    mask = cv2.inRange(img_hsv, lower_color, upper_color)


    img = cv2.imread("sprites/tutorial.png")
    img = cv2.resize(img, (int(1280 * 3 / 4), int(720 * 3 /4)))
    cv2.imshow('tutorial', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    #testando o canny edge detection   
    #edge = cv2.Canny(img2, 230, 240)
 
    
    #outro modo de calcular os pixels, usando o filtro de sobel para detecção de bordas
    #mas é necessário suavizar a imagem para remover o ruído
    #problema : a suavização está perdendo muitos detalhes
    #teste : não utilizar a suavização, GRANDE RISCO

    '''
    img2 = cv2.imread(dir)
    img3 = cv2.GaussianBlur(img2, (3, 3), cv2.BORDER_DEFAULT)
    #img3rgb = cv2.cvtColor(img3, cv2.COLOR_BGR2RGB)

    img3 = cv2.cvtColor(img3, cv2.COLOR_BGR2GRAY)
    grad_x = cv2.Sobel(img3, cv2.CV_16S, 1, 0, ksize=3, scale=1, delta=0, borderType=cv2.BORDER_DEFAULT)
    grad_y = cv2.Sobel(img3, cv2.CV_16S, 0, 1, ksize=3, scale=1, delta=0, borderType=cv2.BORDER_DEFAULT)

    abs_grad_x = cv2.convertScaleAbs(grad_x)
    abs_grad_y = cv2.convertScaleAbs(grad_y)
    
    
    grad = cv2.addWeighted(abs_grad_x, 0.5, abs_grad_y, 0.5, 0)
    _, grad = cv2.threshold(grad, 50, 255, cv2.THRESH_BINARY)
    
    cv2.imshow('sobel', grad)
    cv2.imshow('color', mask)
    cv2.imshow('canny', edge)

    cv2.waitKey(0) 
    cv2.destroyAllWindows() 
    '''

    #agora reconhecer o spawn point
    lower_color = np.array([138, 30, 20])
    upper_color = np.array([179, 255, 255])
    mask1 = cv2.inRange(img_hsv, lower_color, upper_color)

    lower_color = np.array([0, 30, 20])
    upper_color = np.array([10, 255, 255])
    mask2 = cv2.inRange(img_hsv, lower_color, upper_color)
    mask1 = np.add(mask1, mask2)
    

    spawny, spawnx = np.where(mask1 == 255)

    #grad = cv2.subtract(grad, mask1)
    
    ind_x, ind_y = np.where(mask == 255)


    theApp = App(dir)
    FPS = 60
    teste = True
    clock = pygame.time.Clock()
    #plat1 = pygame.Rect(10, theApp.height*3/4, theApp.weight-20, 40)
    if spawnx is not ([] or None) and len(spawnx) > 0:
        theApp.player.x = spawnx[0] + 10
        theApp.player.y = spawny[0]
        #print(theApp.player.x)
        #print(theApp.player.y)
    i = 0
    for ind in ind_x:
        temp = pygame.Rect(ind_y[i], ind, 1, 1)
        theApp.allrect.append(temp)
        theApp.player.collisorlist.append(temp)
        i += 1


    k = 0
    while(teste):
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_c]:
            vcap = cv2.VideoCapture(1)
            ret, curr_frame = vcap.read()
            if ret:
                process_frame(curr_frame, theApp)
            vcap.release()
        elif keys[pygame.K_r]:
            dir = prompt_file()
            if dir != "" and dir != None and type(dir) != tuple:
                print('--------------')
                print(type(dir))
                print('-----------------')
                new_img = cv2.imread(dir)
                process_frame(new_img, theApp)
            
        clock.tick(FPS)
        teste = theApp.on_execute()

    theApp.display.fill((255,255,255))
    game_text = theApp.TEXT_FONT.render(f'GAME OVER', False, (0, 0, 0))
    score_text = theApp.TEXT_FONT.render(f'SCORE {score}', False, (0, 0, 0))
    game_text = pygame.transform.scale(game_text, (game_text.get_width() * 3,game_text.get_height() * 3)) 
    score_text = pygame.transform.scale(score_text, (score_text.get_width() * 3,score_text.get_height() * 3)) 
    theApp.display.blit(game_text, ((theApp.weight / 2) - score_text.get_width()/2 - 5, theApp.height / 2 - 50))
    theApp.display.blit(score_text, ((theApp.weight / 2) - score_text.get_width()/2, theApp.height / 2))
    pygame.display.update()
    for i in range (9999999):
        x = i * i - 1
    print(score)