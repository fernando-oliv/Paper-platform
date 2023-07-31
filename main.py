import pygame
from pygame.locals import *
 
class Player:
    def __init__(self):
        self.width = 40  # Set the player width and height
        self.height = 60
        self.x = 50    # Set the player positions 
        self.y = 200
        self.vel = 5
        self.max_jump = 1
        self.jump_height = 12
        self.jump_count = self.max_jump
        self.collisorlist = []
        self.gravity = 5
        self.jumpingTime = 0
        self.jumping = False

    def move(self):
        auxX = self.x
        auxY = self.y
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            auxX -= self.vel
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            auxX += self.vel
        if keys[pygame.K_SPACE]:
            if self.jumpingTime < 20 and self.jump_count > 0:
                self.jumping = True
                auxY -= self.jump_height
                self.jumpingTime += 1
        elif self.jumping:
            self.jumping = False
            self.jump_count -= 1 if self.jump_count > 0 else 0
            self.jumpingTime = 0

        auxY += self.gravity
        temprectX = pygame.Rect(auxX, self.y, self.width, self.height)
        temprectY = pygame.Rect(self.x, auxY, self.width, self.height)
        flagX, flagY = True, True
        for temp in self.collisorlist:
            if flagX:
                if temprectX.colliderect(temp):
                    flagX = False
            if flagY:
                if temprectY.colliderect(temp):
                    flagY = False
                    self.jump_count = self.max_jump
                    if flagX == False:
                        break
        if flagX:    
            self.x = auxX
        if flagY:
            self.y = auxY
        
    


class App:
    def __init__(self):
        self._running = True
        self.size = self.weight, self.height = 640, 400
        pygame.init()
        self.display = pygame.display.set_mode([self.weight, self.height])
        self.player = Player()
        borders = []
        borders.append(pygame.Rect(-1, 0, 1, self.height))
        borders.append(pygame.Rect(0, -1, self.weight, 1))
        borders.append(pygame.Rect(self.weight+1, 0, 1, self.height))
        borders.append(pygame.Rect(0, self.height+1, self.weight+1, 1))
        self.player.collisorlist = borders
        self.allrect = []
        
  
    def on_event(self, event):
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
        pygame.quit()

    def draw_window(self):
        self.display.fill((255,255,255))
        pygame.draw.rect(self.display, (255, 0, 0), (self.player.x, self.player.y, self.player.width, self.player.height), 3)
        for temp in self.allrect:
            pygame.draw.rect(self.display, (0, 255, 0), temp, 3)
        
        pygame.display.update()

    def on_execute(self):
 
        if( self._running ):
            for event in pygame.event.get():
                self.on_event(event)

            self.player.move()
            self.draw_window()            
            return True
        else:
            self.on_cleanup()
            return False
 

if __name__ == "__main__" :
    theApp = App()
    FPS = 60
    teste = True
    clock = pygame.time.Clock()
    plat1 = pygame.Rect(10, theApp.height*3/4, theApp.weight-20, 40)

    theApp.allrect.append(plat1)
    theApp.player.collisorlist.append(plat1)
    while(teste):
        clock.tick(FPS)
        teste = theApp.on_execute()
    theApp.on_quit()