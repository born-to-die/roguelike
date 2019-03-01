import random
import pygame
import config
from math import sqrt
from os import path

class Unit:

    sprite = pygame.image.load(path.join('images', 'unknown.png'))

    # CHARS
    name = ""
    damage = 1          #
    meleeClose = 0      # промах ближнего боя, чем больше тем больше промах
    stringMeleeAttack = "Существо атаковало вас в ближнем бою!"
    stringRangedAttack = "Существо атаковало вас в дальнем бою!"
    stringMiss = "Существо промахнулось по вам"

    # SPECS
    life = True         #
    delete = False      # определяет есть ли после смерти труп, нет - удалить 
    animate = False     # флаг анимации в текущий момент
    animation = True    # флаг анимации
    x = 0               #
    y = 0               #
    last_x = x          # нужно для анимации из last в текущее
    last_y = y          # нужно для анимации из last в текущее
    move_x = None       # двигаться в x
    move_y = None       # двигаться в y
    behavior = None     # текущее поведение
    attacker = None     # последний атаковавший

    def __init__(self):
        pass

    def Action(self, game):
        pass

    def init(self, game):

        pos = random.randint(0, len(game.free_tiles) / 2) * 2

        for i in range(0, len(game.free_tiles), 2):
            print(str(game.free_tiles[i]) + " "
                  + str(game.free_tiles[i + 1])
                  )

        print(str(len(game.free_tiles)) + " "
              + str(len(game.free_tiles) / 2)
              + " "
              + str(pos))
        
        self.x = game.free_tiles[pos]
        self.y = game.free_tiles[pos + 1]

        print(self.name + " spawn in "
              + str(self.x) + ":" + str(self.y))

    def setPosition(self, x, y):

        self.x = x
        self.y = y

    def Render(self, game, runAnim):
        
        if(config.animationOn and self.animation and runAnim):

            isAnimGo = False

            for i in range(len(game.listUnits)):
                
                    if(game.listUnits[i].animate):
                        isAnimGo = True

            if(not isAnimGo):
                self.animate = True
            
            if((self.last_x != self.x or self.last_y != self.y) and
               self.life == True and self.animate):
                self.playAnimation(game)
            
            self.animate = False

        game.surfGame.blit(self.sprite, (self.x * 64, self.y * 64))

    def playAnimation(self, game):

        speed = config.speedAnimation
        
        if(self.last_y > self.y and self.last_x == self.x):
            dx = 0
            dy = -speed
        elif(self.last_y > self.y and self.last_x < self.x):
            dx = speed
            dy = -speed
        elif(self.last_y == self.y and self.last_x < self.x):
            dx = speed
            dy = 0
        elif(self.last_y < self.y and self.last_x < self.x):
            dx = speed
            dy = speed
        elif(self.last_y < self.y and self.last_x == self.x):
            dx = 0
            dy = speed
        elif(self.last_y < self.y and self.last_x > self.x):
            dx = -speed
            dy = speed
        elif(self.last_y == self.y and self.last_x > self.x):
            dx = -speed
            dy = 0
        elif(self.last_y > self.y and self.last_x > self.x):
            dx = -speed
            dy = -speed
            
        cx = self.last_x * 64
        cy = self.last_y * 64

        while(cy != self.y * 64 or cx != self.x * 64):

            game.clock.tick(30) # 30 FPS
            
            cx += dx
            cy += dy
            
            game.RenderLandmap()
            game.RenderDecors()
            game.RenderItems()
            game.RenderUnits()
            game.RenderPlayer()
            
            game.surfGame.blit(self.sprite, (cx, cy))
            game.RenderDecorsOver()    
            game.screen.blit(game.surfGame, (0,0))
            pygame.display.update()
        
    def getFreeTile(self, x, y, game):

        if(game.player.x == x and game.player.y == y):
            return False
        
        for i in range(len(game.listUnits)):
            if(game.listUnits[i].x == x and game.listUnits[i].y == y and
               game.listUnits[i].life):
               return False
        return True

    def getDamage(self, damage, game, attacker):
        
        self.attacker = attacker
        self.health -= damage
        
        if(self.health < 1):
            self.life = False
            
    def playerIsClose(self, player):
        if(sqrt(pow(player.x - self.x, 2) + pow(player.y - self.y, 2)) <= 1.5):
            return True
        else:
            return False

    def getPlayerDirect(self, player):
        if(player.x == self.x and player.y == self.y - 1):
            return 0
        elif(player.x == self.x + 1 and player.y == self.y - 1):
            return 1
        elif(player.x == self.x + 1 and player.y == self.y):
            return 2
        elif(player.x == self.x + 1 and player.y == self.y + 1):
            return 3
        elif(player.x == self.x and player.y == self.y + 1):
            return 4
        elif(player.x == self.x - 1 and player.y == self.y + 1):
            return 5
        elif(player.x == self.x - 1 and player.y == self.y):
            return 6
        elif(player.x == self.x - 1 and player.y == self.y - 1):
            return 7

    def moveSimpleDirect(self, game, dx, dy):
        if(dx == self.x and dy < self.y): # top
            if(game.assTileType[game.landmap[self.y - 1][self.x]] == "floor" and
               self.getFreeTile(self.x, self.y - 1, game)):
                self.y -= 1
            elif(game.assTileType[game.landmap[self.y - 1][self.x + 1]] == "floor" and
                 self.getFreeTile(self.x + 1, self.y - 1, game)):
                self.y -= 1
                self.x += 1
            elif(game.assTileType[game.landmap[self.y - 1][self.x - 1]] == "floor" and
                 self.getFreeTile(self.x - 1, self.y - 1, game)):
                self.x -= 1
                self.y -= 1
        elif(dx > self.x and dy < self.y): # top - right
            if(game.assTileType[game.landmap[self.y - 1][self.x + 1]] == "floor" and
               self.getFreeTile(self.x + 1, self.y - 1, game)):
                self.x += 1
                self.y -= 1
            elif(game.assTileType[game.landmap[self.y - 1][self.x]] == "floor" and
                 self.getFreeTile(self.x, self.y - 1, game)):
                self.y -= 1
            elif(game.assTileType[game.landmap[self.y][self.x + 1]] == "floor" and
                 self.getFreeTile(self.x + 1, self.y, game)):
                self.x += 1
        elif(dx > self.x and dy == self.y): # right
            if(game.assTileType[game.landmap[self.y][self.x + 1]] == "floor" and
               self.getFreeTile(self.x + 1, self.y, game)):
                self.x += 1
            elif(game.assTileType[game.landmap[self.y + 1][self.x + 1]] == "floor" and
                 self.getFreeTile(self.x + 1, self.y + 1, game)):
                self.y += 1
                self.x += 1
            elif(game.assTileType[game.landmap[self.y - 1][self.x + 1]] == "floor" and
                 self.getFreeTile(self.x + 1, self.y - 1, game)):
                self.x += 1
                self.y -= 1
        elif(dx > self.x and dy > self.y): # down - right
            if(game.assTileType[game.landmap[self.y + 1][self.x + 1]] == "floor" and
               self.getFreeTile(self.x + 1, self.y + 1, game)):
                self.x += 1
                self.y += 1
            elif(game.assTileType[game.landmap[self.y][self.x + 1]] == "floor" and
                 self.getFreeTile(self.x + 1, self.y, game)):
                self.x += 1
            elif(game.assTileType[game.landmap[self.y + 1][self.x]] == "floor" and
                 self.getFreeTile(self.x, self.y + 1, game)):
                self.y += 1
        elif(dx == self.x and dy > self.y): # down
            if(game.assTileType[game.landmap[self.y + 1][self.x]] == "floor" and
               self.getFreeTile(self.x, self.y + 1, game)):
                self.y += 1
            elif(game.assTileType[game.landmap[self.y + 1][self.x + 1]] == "floor" and
                 self.getFreeTile(self.x + 1, self.y + 1, game)):
                self.y += 1
                self.x += 1
            elif(game.assTileType[game.landmap[self.y + 1][self.x - 1]] == "floor" and
                 self.getFreeTile(self.x - 1, self.y + 1 , game)):
                self.x -= 1
                self.y += 1
        elif(dx < self.x and dy > self.y): # down - left
            if(game.assTileType[game.landmap[self.y + 1][self.x - 1]] == "floor" and
               self.getFreeTile(self.x - 1, self.y + 1, game)):
                self.x -= 1
                self.y += 1
            elif(game.assTileType[game.landmap[self.y][self.x - 1]] == "floor" and
                 self.getFreeTile(self.x - 1, self.y, game)):
                self.x -= 1
            elif(game.assTileType[game.landmap[self.y + 1][self.x]] == "floor" and
                 self.getFreeTile(self.x, self.y + 1, game)):
                self.y += 1
        elif(dx < self.x and dy == self.y): # left
            if(game.assTileType[game.landmap[self.y][self.x - 1]] == "floor" and
               self.getFreeTile(self.x - 1, self.y, game)):
                self.x -= 1
            elif(game.assTileType[game.landmap[self.y - 1][self.x - 1]] == "floor" and
                 self.getFreeTile(self.x - 1, self.y - 1, game)):
                self.y -= 1
                self.x -= 1
            elif(game.assTileType[game.landmap[self.y + 1][self.x - 1]] == "floor" and
                 self.getFreeTile(self.x - 1, self.y + 1, game)):
                self.x -= 1
                self.y += 1
        elif(dx < self.x and dy < self.y): # top - left
            if(game.assTileType[game.landmap[self.y - 1][self.x - 1]] == "floor" and
               self.getFreeTile(self.x - 1, self.y - 1, game)):
                self.x -= 1
                self.y -= 1
            elif(game.assTileType[game.landmap[self.y - 1][self.x]] == "floor" and
                 self.getFreeTile(self.x, self.y - 1, game)):
                self.y -= 1
            elif(game.assTileType[game.landmap[self.y][self.x - 1]] == "floor" and
                 self.getFreeTile(self.x - 1, self.y, game)):
                self.x -= 1

    def getMeleeAttack(self, game):

        if (config.animationOn):
            self.last_x = self.x
            self.last_y = self.y

            # ANIMA getMeleeAttack
            self.x = game.player.x
            self.y = game.player.y
            
            self.Render(game, True)
            
            self.x = self.last_x
            self.y = self.last_y
            
            game.RenderLandmap()
            game.RenderDecors()
            game.RenderItems()
            game.RenderUnits()
            game.RenderPlayer()
            game.RenderDecorsOver()
            game.RenderDecorsOver()        
            game.screen.blit(game.surfGame, (0,0))
            pygame.display.update()

        success = random.randint(0, 10)

        if(success > self.meleeClose):
            game.writeEvent(self.stringMeleeAttack, (110, 0, 0))
            game.player.getDamage(self.damage, game)
        else:
            game.writeEvent(self.stringMiss, (110, 0, 0))
        
    def spawnOnArea(self, sx, sy, fx, fy):

        self.x = random.randint(sx, fx)
        self.y = random.randint(sy, fy)
        
    def moveDirect(self, game, directx, directy):

        try:            
            
            if(game.assTileType[game.landmap[self.y + directy][self.x + directx]] == "floor" and
            self.x + directx >= 0 and self.x + directx <= 9 and 
            self.y + directy >= 0 and self.y + directy <= 9):
            
                self.x += directx
                self.y += directy

                return True
            
            else:

                return False

        except:
            print("%")
            return False
        
    def moveStagger(self, game):
    
        directx = random.randint(-1, 1)
        directy = random.randint(-1, 1)
        
        self.moveDirect(game, directx, directy)
                
class Human(Unit):

    # DRAW
    sprite = pygame.image.load(path.join('images','1.png'))

    # CHARS
    name = "Человек"
    damage = 3
    health = 3
    meleeClose = 3
    stringMeleeAttack = "Человек атаковал"
    stringMiss = "Человек промахнулся"
    delete = True

    def __init__(self):
        self.x = 0
        self.y = 0
        self.last_x = self.x
        self.last_y = self.y

    def init(self, args):
        pass

    

    def Action(self, game):        
        
        if(self.life):
            
            self.last_x = self.x
            self.last_y = self.y

            if(self.attacker != None):

                if(self.attacker.health <= 0):
                    self.attacker = None
                else:
                    if(self.playerIsClose(game.player)):
                        self.getMeleeAttack(game)
                    else:
                        self.moveSimpleDirect(game, game.player.x,
                                              game.player.y)
            else:
                if(self.behavior == "move"):
                    self.moveSimpleDirect(game, self.move_x, self.move_y)
                
class Snake(Unit):

    # DRAW
    sprite = pygame.image.load(path.join('images','enemySnake.png'))

    # CHARS
    name = "Змея"
    damage = 3
    health = 3
    meleeClose = 3
    stringMeleeAttack = "Змея укусила вас!"
    stringMiss = "Змея промахнулась по вам"

    # SPECS
    delete = True

    def getDamage(self, damage, game, attacker):
        self.health -= damage
        if(self.health < 1):
            self.life = False
            game.writeEvent(u"Змея больше не двигается...", (120, 0, 0))
            self.sprite = pygame.image.load(path.join('images','lightcondaDead.png'))

    def __init__(self):
        self.x = 0
        self.y = 0
        self.last_x = self.x
        self.last_y = self.y

    def init(self, args):
        pass
            

    def Action(self, game):
        if(self.life):
            self.last_x = self.x
            self.last_y = self.y
            if(self.playerIsClose(game.player)):
                self.getMeleeAttack(game)
            else:
                self.moveStagger(game)

class Deadhelmet(Unit):

    # CHARS
    name = "Паук"
    damage = 3
    health = 3
    meleeClose = 3
    stringMeleeAttack = "Паук укусил вас!"
    stringMiss = "Паук промахнулся по вам"
    sprite = pygame.image.load(path.join('images', 'deadhelmet.png'))

    # SPECS
    delete = False
    directx = 1
    directy = 1
    playerIs = False

    def getDamage(self, damage, game, attacker):
        self.health -= damage
        if(self.health < 1):
            self.life = False
            game.writeEvent(u"Паук больше не двигается...", (120, 0, 0))
            self.sprite = pygame.image.load(path.join('images','spiderDead.png'))

    def init(self, game):

        self.x = 0
        self.y = 0
            
        while(game.assTileType[game.landmap[self.y][self.x]] != "floor"):

            self.x = random.randint(0, 9)
            self.y = random.randint(0, 9)
                
        self.last_x = self.x
        self.last_y = self.y
            

    def Action(self, game):

        print(str(self.x) + " " + str(self.y) + ' ')

        if(self.life):
            self.last_x = self.x
            self.last_y = self.y
            if(self.playerIsClose(game.player)):
                self.playerIs = True
                self.getMeleeAttack(game)
                print('#')
            elif(self.playerIs == True):
                self.moveSimpleDirect(game, game.player.x, game.player.y)
                print('%' + str(game.player.x) + ' ' + str(game.player.y))
            else:
                print("@")
                while(self.moveDirect(game, self.directx, self.directy) == False):                    
                    self.directx = random.randint(-1, 1)
                    self.directy = random.randint(-1, 1)
                    while(self.directx == 0 and self.directy == 0):
                        self.directx = random.randint(-1, 1)
                        self.directy = random.randint(-1, 1)
