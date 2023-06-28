import pygame
from pygame.locals import *
 
class Player:
    def __init__(self):
        self.width = 40  # Set the player width and height
        self.height = 60
        self.x = 50    # Set the player positions 
        self.y = 300
        self.vel = 5
        self.max_jump = 1
        self.jump_count = self.max_jump

    def move(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.x -= self.vel
        if keys[pygame.K_RIGHT]:
            self.x += self.vel
        if keys[pygame.K_UP]:
            self.y -= self.vel
        if keys[pygame.K_DOWN]:
            self.y += self.vel


class App:
    def __init__(self):
        self._running = True
        self.size = self.weight, self.height = 640, 400
        pygame.init()
        self.display = pygame.display.set_mode([self.weight, self.height])
        self.player = Player()
  
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
    while(teste):
        clock.tick(FPS)
        teste = theApp.on_execute()
    theApp.on_quit()