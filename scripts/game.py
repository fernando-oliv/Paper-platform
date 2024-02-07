import pygame
from player import Player
from flyingEnemy import FlyingEnemy
from cv2 import waitKey

class App:
    def __init__(self, dir):
        self._running = True
        self.size = self.weight, self.height = 800, 600
        pygame.init()
        pygame.font.get_init()
        self.TEXT_FONT = pygame.font.Font("../font.otf")
        self.display = pygame.display.set_mode((self.weight, self.height))
        self.player = Player()
        borders = []
        borders.append(pygame.Rect(-1, 0, 1, self.height))
        borders.append(pygame.Rect(0, -1, self.weight, 1))
        borders.append(pygame.Rect(self.weight+1, 0, 1, self.height))
        borders.append(pygame.Rect(0, self.height+1, self.weight+1, 1))
        self.player.collisorlist = borders
        self.allrect = []
        self.img = pygame.image.load(dir)
        self.heart = pygame.image.load("../sprites/Heart.png")
        self.waves = 3
        self.currentWave = 1
        self.spawnDelay = 2
        self.init = pygame.time.get_ticks()
        self.timer = 5
        self.remainingDuoEnemies = 0
        self.enemies = []
        self.enemiesRects = []
        pygame.time.set_timer(pygame.USEREVENT, 500)
        self.score = 0
           
  
    def on_event(self, event):
        if event.type == pygame.USEREVENT:
            self.timer = True
        if event.type == pygame.QUIT:
            self._running = False

        if event.type == pygame.KEYDOWN:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_x]:
                self.player.attack()


    def on_load(self):
        #load new level
        pass

    def on_cleanup(self):
        #clears previously loaded levels
        pass

    def on_quit(self):
        self.display.fill((255,255,255))
        game_text = self.TEXT_FONT.render(f'GAME OVER', False, (0, 0, 0))
        score_text = self.TEXT_FONT.render(f'SCORE {self.score}', False, (0, 0, 0))
        end_text = self.TEXT_FONT.render(f'aperte qualquer tecla para sair', False, (0, 0, 0))
        game_text = pygame.transform.scale(game_text, (game_text.get_width() * 3,game_text.get_height() * 3)) 
        score_text = pygame.transform.scale(score_text, (score_text.get_width() * 3,score_text.get_height() * 3)) 
        end_text = pygame.transform.scale(end_text, (end_text.get_width() * 1, end_text.get_height() * 1))
        self.display.blit(game_text, ((self.weight / 2) - score_text.get_width()/2 - 5, self.height / 2 - 50))
        self.display.blit(score_text, ((self.weight / 2) - score_text.get_width()/2, self.height / 2))
        self.display.blit(end_text, ( (self.weight - end_text.get_width())/2 ,  (self.height - 50)))
        
        pygame.display.update()
        self.init = pygame.time.get_ticks()
        
        while True:
            self.diff = pygame.time.get_ticks() - self.init
            if self.diff > 10000:
                return
            for event in pygame.event.get():
                if event.type == pygame.QUIT or event.type == pygame.KEYDOWN:
                    return

        

    def on_win(self):
        pass

    def draw_window(self):
        self.display.blit(self.img, (0,0))
        score_text = self.TEXT_FONT.render(f'SCORE {self.score}', False, (0, 0, 0))
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
            rotatedImage = pygame.transform.rotate(temp, right * -30 * self.player.attackSprite)
            self.display.blit(rotatedImage, (self.player.x + right * (20 * self.player.attackSprite), self.player.y - 30 +  (7 * self.player.attackSprite)))


        for enemy in self.enemies:
            #pygame.draw.rect(self.display, (255, 0, 0), (enemy.x, enemy.y, self.player.width, self.player.height), 3)
            self.display.blit(enemy.sprite, (enemy.x, enemy.y))
            
        for i in range(self.player.life):
            self.display.blit(self.heart, (i*35, 0))
        
        pygame.display.update()

    def updateWave(self):
        #wave não criada
        if self.remainingDuoEnemies == 0 and self.enemies == []:
            self.currentWave += 1
            self.player.life += 1 if self.player.life <= 3 else 0
            self.timer = True
            self.remainingDuoEnemies = self.currentWave
        
        #se ainda tiver inimigos para spawnar, spawne com um timer de espaço
        elif self.timer == True and self.remainingDuoEnemies > 0:

            #cria os inimigos
            self.enemies.append(FlyingEnemy(self.player, 0, 0))
            self.enemies.append(FlyingEnemy(self.player, self.weight, 0))

            #cria seus collisors
            self.enemiesRects.append(self.enemies[-2].rect)
            self.enemiesRects.append(self.enemies[-1].rect)

            #velocidade aumenta com as waves
            self.enemies[-2].movSpeed = 3 + 0.25*self.currentWave 
            self.enemies[-1].movSpeed = 3 + 0.25*self.currentWave

            #set um timer de delay entre os spawns
            pygame.time.set_timer(pygame.USEREVENT, 500)

            #reduz o contador
            self.timer = False
            self.remainingDuoEnemies -= 1

    def killEnemy(self, index):
        del self.enemies[index]
        del self.enemiesRects[index]
        self.score += 100

    def checkCollisions(self):
        #checar o ataque do player
        if self.player.attackRect != None:
            indexlist = self.player.attackRect.collidelistall(self.enemiesRects)
            if  indexlist is not []:
                indexlist.reverse() #necessário para não mudar a ordem se algum for removido
                for index in indexlist:
                    self.enemies[index].hurt()
                    if self.enemies[index].life == 0:
                        self.killEnemy(index)

        #checar se os inimigos colidiram com o player, pegue a 1ª colisão apenas
        index = self.player.rect.collidelist(self.enemiesRects)
        if  index >= 0 :
            self.player.hurt()

    def on_execute(self):
        
        if( self._running ):
            for event in pygame.event.get():
                self.on_event(event)

            self.player.move()
            for index in range(len(self.enemies)):
                tmp = self.enemies[index].move()
                if tmp != None:
                    self.enemiesRects[index] = tmp
                
            self.player.animationController()
            self.updateWave()
            self.checkCollisions()
            self.draw_window()
            if self.player.life == 0:
                self._running = False
            return True
        else:
            keys = pygame.key.get_pressed()
            self.on_quit()
            return False