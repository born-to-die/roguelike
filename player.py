from math import sqrt
from os import path
from pygame import image
from pygame import display

import random
import items
import config
import pygame

class Player:
    
    sprite = image.load(path.join('images','player.png'))
    cellSelect = image.load(path.join('images', 'cellSelect.png'))
    cellWeapon = image.load(path.join('images', 'cellWeapon.png'))

    inventIsOpen = False

    name = "Игрок епта"

    hand = 0
    maxItems = 12;
    items = []

    missClose = 3 # промах для обычного ближнего боя, чем больше тем больше промах

    numUseWeap = -1

    x = 1
    y = 8
    last_x = x
    last_y = y
    turn = True

    
    interactions = ["help", "grub", "harm"]
    interaction = "help"
    
    damage = 1

    health = 10

    def __init__(self):

        for i in range(12):
            self.items.append(0)

    def getFreeTile(self, x, y, listUnits):
        
        for i in range(len(listUnits)):
            if(listUnits[i].x == x and listUnits[i].y == y and listUnits[i].life == True):
               return i
        
        return -1
    
    # Рисует рамку используемого оружия в инвентаре 
    def drawUses(self, game):

        if(self.numUseWeap != -1):

            cursorY = self.numUseWeap // 4
            cursorX = self.numUseWeap % 4

            game.screen.blit(self.cellWeapon, (64 * cursorX + 640, 64 * cursorY + 128))
            game.screen.blit(game.surfGame, (0,0))
            pygame.display.update()   

    def getInvent(self, game):

        cursorX = 0
        cursorY = 0

        inventIsUse = True

        game.drawCharactersInfo()

        game.screen.blit(self.cellSelect, (64 * cursorX + 640, 64 * cursorY + 128))

        pygame.display.update()     

        while(inventIsUse):

            draw = False

            for event in pygame.event.get():
            
                if event.type == pygame.KEYDOWN:

                    print(self.damage)

                    if event.key == pygame.K_ESCAPE:

                        inventIsUse = False

                    elif event.key == pygame.K_d:

                        cursorX += 1

                    elif event.key == pygame.K_a:

                        cursorX -= 1

                    elif event.key == pygame.K_w:

                        cursorY -= 1

                    elif event.key == pygame.K_s:

                        cursorY += 1

                    elif event.key == pygame.K_f:

                        if(self.numUseWeap != cursorY * 4 + cursorX):

                            if(self.items[cursorY * 4 + cursorX] != 0):

                                if(self.items[cursorY * 4 + cursorX].typeItem == "closeweapon"):

                                    self.numUseWeap = cursorY * 4 + cursorX

                                    self.damage = self.items[cursorY * 4 + cursorX].damage;

                                    self.hand = self.items[cursorY * 4 + cursorX]

                                    game.RenderLandmap()
                                    game.RenderDecors()
                                    game.RenderItems()
                                    game.RenderUnits()
                                    self.Render(game, False)
                                    game.RenderDecorsOver()

                        else:

                            if(self.items[cursorY * 4 + cursorX].typeItem == "closeweapon"):
                                self.damage = 1

                            self.numUseWeap = -1

                            self.hand = 0

                            game.RenderLandmap()
                            game.RenderDecors()
                            game.RenderItems()
                            game.RenderUnits()
                            self.Render(game, False)
                            game.RenderDecorsOver()

                    elif event.key == pygame.K_x:

                        if(self.items[cursorY * 4 + cursorX] != 0):

                            if(self.items[cursorY * 4 + cursorX] != self.numUseWeap):

                                if(self.items[cursorY * 4 + cursorX].typeItem == "closeweapon"):
                                    self.damage = 1

                                self.numUseWeap = -1

                                self.hand = 0
                            
                            #print(self.items[cursorY * 4 + cursorX].delete)
                            self.items[cursorY * 4 + cursorX].setPosition(self.x, self.y)
                            self.items[cursorY * 4 + cursorX].delete = False
                            game.listItems.append(self.items[cursorY * 4 + cursorX])
                            self.items[cursorY * 4 + cursorX] = 0

                            for i in range(len(game.listItems)):
                                game.listItems[i].Render(game.surfGame)

                            for i in range(len(game.listUnits)):
                                if(not game.listUnits[i].life):
                                    game.listUnits[i].Render(game, False)

                            for i in range(len(game.listUnits)):
                                if(game.listUnits[i].life):
                                    game.listUnits[i].Render(game, False)
                            
                            game.RenderLandmap()
                            game.RenderDecors()
                            game.RenderItems()
                            game.RenderUnits()
                            self.Render(game, False)
                            game.RenderDecorsOver()

                    draw = True

            if(draw):

                game.drawCharactersInfo()

                self.drawUses(game)

                game.screen.blit(self.cellSelect, (64 * cursorX + 640, 64 * cursorY + 128))

                game.screen.blit(game.surfGame, (0,0))

                pygame.display.update()

        game.drawCharactersInfo()

        self.drawUses(game)

        pygame.display.update()

            

    def getTake(self, game):
        
        for i in range(len(game.listItems)):
            
            if(game.listItems[i].x == self.x and game.listItems[i].y == self.y):


                self.addItem(game.listItems[i])


                game.listItems[i].delete = True
                #self.hand = listItems.pop(i)
                game.drawCharactersInfo()
                self.drawUses(game)

    def addItem(self, item):

        for j in range(12):
            if(self.items[j] == 0):
                self.items[j] = item
                break
                
    def Render(self, game, runAnim):

        #game.RenderTile(self.last_x, self.last_y)

        if(self.turn):

            if(config.animationOn and runAnim):
                if(self.last_x != self.x or self.last_y != self.y):
                    self.playAnimation(game)
                    #self.last_x = self.x
                    #self.last_y = self.y

            
            game.surfGame.blit(self.sprite, (self.x * 64, self.y * 64))

            if(self.hand != 0 and self.health > 0):
                game.surfGame.blit(self.hand.spriteHand, (self.x * 64, self.y * 64))


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
            
                
            game.surfGame.blit(self.sprite, (cx, cy))
            
            if(self.hand != 0):
                game.surfGame.blit(self.hand.spriteHand, (cx, cy))

            game.RenderDecorsOver()
                
            game.screen.blit(game.surfGame, (0,0))
            pygame.display.update()

    def Attack(self, game, enemy):

        success = random.randint(0, 10)

        if(success > self.missClose):
            game.listUnits[enemy].getDamage(self.damage, game, self)
            game.writeEvent(u"Вы атаковали [" + game.listUnits[enemy].name + "]", (120, 80, 0))            
        else:
            game.writeEvent(u"Вы промахнулись по [" + game.listUnits[enemy].name + "]", (120, 0, 0))

        if (config.animationOn):
            
            self.last_x = self.x
            self.last_y = self.y

            self.x = game.listUnits[enemy].x
            self.y = game.listUnits[enemy].y

            self.Render(game, True)

            self.x = self.last_x
            self.y = self.last_y

            game.RenderLandmap()
            game.RenderDecors()
            game.RenderItems()
            game.RenderUnits()

            self.Render(game, False)

            game.RenderDecorsOver()
                    
            game.screen.blit(game.surfGame, (0,0))
            pygame.display.update()

    def Move(self, game, x, y):

        if(self.x + x < 10 and self.x + x > -1 and
           self.y + y < 10 and self.y + y > -1):

            if(game.assTileType[game.landmap[self.y + y][self.x + x]] == "floor"):

                self.y = self.y + y
                self.x = self.x + x

    def Action(self, game, action):

        self.turn = True

        self.last_x = self.x
        self.last_y = self.y
        
        if action == 0: # MOVE UP
            
            enemyIsClose = self.getFreeTile(self.x, self.y - 1, game.listUnits)
            
            if(self.getFreeTile(self.x, self.y - 1, game.listUnits) != -1):
                if(self.interaction == "harm"):
                    self.Attack(game, enemyIsClose)
                
            else:
                self.Move(game, 0, -1)         
                
        elif action == 1: # MOVE RIGHT
            
            enemyIsClose = self.getFreeTile(self.x + 1, self.y, game.listUnits)
            
            if(self.getFreeTile(self.x + 1, self.y, game.listUnits) != -1):
                if(self.interaction == "harm"):
                    self.Attack(game, enemyIsClose)
                    
            else:
                self.Move(game, 1, 0)
                
        elif action == 2: # MOVE DOWN
            
            enemyIsClose = self.getFreeTile(self.x, self.y + 1, game.listUnits)
            
            if(self.getFreeTile(self.x, self.y + 1, game.listUnits) != -1):
                if(self.interaction == "harm"):
                    self.Attack(game, enemyIsClose)
                
            else:
                self.Move(game, 0, 1)
                
        elif action == 3: # MOVE LEFT
            
            enemyIsClose = self.getFreeTile(self.x - 1, self.y, game.listUnits)
            
            if(self.getFreeTile(self.x - 1, self.y, game.listUnits) != -1):
                if(self.interaction == "harm"):
                    self.Attack(game, enemyIsClose)
                
            else:
                self.Move(game, -1, 0)

        elif action == 7: # MOVE TOP-RIGHT
            
            enemyIsClose = self.getFreeTile(self.x + 1, self.y - 1, game.listUnits)
            
            if(self.getFreeTile(self.x + 1, self.y - 1, game.listUnits) != -1):
                if(self.interaction == "harm"):
                    self.Attack(game, enemyIsClose)
                
            else:
                self.Move(game, 1, -1)

        elif action == 8: # MOVE TOP-LEFT
            
            enemyIsClose = self.getFreeTile(self.x - 1, self.y - 1, game.listUnits)
            
            if(self.getFreeTile(self.x - 1, self.y - 1, game.listUnits) != -1):
                if(self.interaction == "harm"):
                    self.Attack(game, enemyIsClose)
                
            else:
                self.Move(game, -1, -1)

        elif action == 9: # MOVE BOTTOM-LEFT
            
            enemyIsClose = self.getFreeTile(self.x - 1, self.y + 1, game.listUnits)
            
            if(self.getFreeTile(self.x - 1, self.y + 1, game.listUnits) != -1):
                if(self.interaction == "harm"):
                    self.Attack(game, enemyIsClose)
                
            else:
                self.Move(game, -1, 1)

        elif action == 10: # MOVE BOTTOM-RIGHT
            
            enemyIsClose = self.getFreeTile(self.x + 1, self.y + 1, game.listUnits)
            
            if(self.getFreeTile(self.x + 1, self.y + 1, game.listUnits) != -1):
                if(self.interaction == "harm"):
                    self.Attack(game, enemyIsClose)
                
            else:
                self.Move(game, 1, 1)

        elif action == 11: # MOVE BOTTOM-RIGHT
            
            if(self.interaction == self.interactions[-1]):
                self.interaction = self.interactions[0]
            else:
                self.interaction = self.interactions[self.interactions.index(
                                                    self.interaction) + 1]
                
            game.drawCharactersInfo()                                                           
                
        elif action == 4: # WAIT 1 TURN
            
            #self.turn = False
            self.x = self.x
            self.Render(game, False)

        elif action == 5: # TAKE ITEM

            self.getTake(game)

        elif action == 6: # OPEN INVENTORY

            self.getInvent(game)

    def setPosition(self, x, y):

        self.x = x
        self.y = y

    def getDamage(self, damage, game):
        
        self.health -= damage

        game.writeEvent(u"Вы потеряли " + str(damage) + " здоровья", (120, 0, 0))

        game.drawCharactersInfo()
        
        if(self.health <= 0):
            
            game.writeEvent(u"Смерть улыбнулась вам", (120, 0, 0))
            self.sprite = image.load(path.join('images','playerDead.png'))

            game.RenderLandmap()
            game.RenderDecors()
            game.RenderItems()
            game.RenderUnits()
            self.Render(game, False)
            game.RenderDecorsOver()
