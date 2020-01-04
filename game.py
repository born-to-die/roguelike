import math
import random
import pygame, sys, os
from pygame.locals import *

import config
import units
import items
import player
import decors
import copy

# enemies
import enemy_mushrooms
import spider

pygame.init()

class Game:

    life = True
    
    # WINDOW
    windowWidth = 900
    windowHeight = 640
    windowTitle = "G4"
    windowBgDefault = (0, 0, 0)

    # LIST OBJECTS
    player = [player.Player()]
    listUnits = []
    listItems = []
    listDecors = []

    # DICT ITEMS
    allListItems = {}
    allListItems['crowbar'] = items.Crowbar(0, 0)
    allListItems['shotgun'] = items.Shotgun(0, 0)

    # DICT ENEMIES
    allListUnits = {}
    allListUnits['snake'] = units.Snake()
    allListUnits['spider'] = spider.Spider()
    allListUnits['deadhelmet'] = units.Deadhelmet()
    allListUnits['human'] = units.Human()
    allListUnits['mushrooms'] = enemy_mushrooms.Mushrooms()

    # NEXTMAPS
    listNextmaps = []
    alistNextmaps = {}

    # SCREEN & DISPLAY
    screen = pygame.display.set_mode((windowWidth, windowHeight), 0, 32)
    surfGame = pygame.Surface((640, 640))       
    surfMessages = pygame.Surface((260, 320))
    surfCharacter = pygame.Surface((260, 320))

    # FONT
    fontDefaultSize = 20
    fontDefault = pygame.font.SysFont("None", fontDefaultSize)
    fontDefaultColor = (100, 100, 100)
    fontDefaultBackColor = (0, 0, 0)

    # CLOCK
    clock = pygame.time.Clock()

    # TEXT AREA
    currentLineWrite = 0

    # MAP
    currentMap = "intro"

    landmap = [
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    ]

    free_tiles = []
    
    nextMap = None
    assTiles = {}
    assTileType = {}

    cellSprite = pygame.image.load(os.path.join('images', 'cell.png'))

    active_player = 0
    
    # TEST
    CONST_PI  = 3.1415926535
    cosinus = []
    sinus = []  
    
    def __init__(self):
        
        pygame.display.set_caption(self.windowTitle)

        if not pygame.image.get_extended():
            raise SystemExit( 'Sorry, extended image module required')

    def initGame(self):

        for i in range(72):
            self.cosinus.append(math.cos(i * 5 * self.CONST_PI / 180))
        
        for i in range(72):
            self.sinus.append(math.sin(i * 5 * self.CONST_PI / 180))

        self.surfMessages.fill((25, 25, 25))
        self.screen.blit(self.surfMessages, (640, 320))

        self.surfCharacter.fill((25, 25, 25))
        self.screen.blit(self.surfCharacter, (640, 0))
    
    def drawCharactersInfo(self):

        self.surfCharacter.fill((25, 25, 25))
        self.screen.blit(self.surfCharacter, (640, 0))
        
        textSprite = self.fontDefault.render(self.player[game.active_player].name, 0, (0, 100, 0))
        self.screen.blit(textSprite, (650, 5))

        textHealth = self.fontDefault.render(u"Здоровье: " + str(self.player[game.active_player].health), 0, (0, 100, 0))
        self.screen.blit(textHealth, (650, 15))

        textHealth = self.fontDefault.render(u"Режим: " + self.player[game.active_player].interaction, 0, (0, 100, 0))
        self.screen.blit(textHealth, (760, 15))

        textMissClose = self.fontDefault.render(u"Навык владения ближним боем: " + str(10 - self.player[game.active_player].missClose), 0, (0, 100, 0))
        self.screen.blit(textMissClose, (650, 25))
        

        # DRAW PLAYERS ITEMS
        
        for i in range(3):
            for j in range(4):
                
                self.screen.blit(self.cellSprite, (j * 64 + 640, i * 64 + 128))
                
                if(self.player[game.active_player].items[i * 4 + j] != 0):
                    self.screen.blit(self.player[game.active_player].items[i * 4 + j].sprite, (j * 64 + 640, i * 64 + 128))
                

    def writeEvent(self, text, color):
        
        if(self.currentLineWrite > 24):
            
            self.surfMessages.set_alpha(200)    
            self.surfMessages.fill((25, 25, 25))
            self.screen.blit(self.surfMessages, (640, 320))
            self.currentLineWrite = 0
            
        textSprite = self.fontDefault.render(text, 0, (color))
        self.screen.blit(textSprite, (650, 320 + self.currentLineWrite * 12))
        self.currentLineWrite += 1

    def getNextMap(self):

        self.player = player.Player()
        self.listUnits = []
        self.listItems = []
        self.listDecors = []
        self.currentMap = self.nextMap
        self.loadMap()
        self.RenderAll()

    def loadMap(self):

        file = open(self.currentMap + '.map', 'r')

        bMapLoad = False
        bReadCmd = True
        mapLine = 0
        mapx = 0
        mapy = 0

        for line in file:

            words = line.split()

            currentWord = 0

            for word in words:

                if(bMapLoad):

                    self.landmap[mapy][mapx] = int(word)

                    self.assTileType[int(word)] = "floor"

                    mapx += 1

                    if(mapx == 10):
                        mapx = 0
                        mapy += 1

                    if(mapy == 10):
                        bMapLoad = False
                        bReadCmd = True
                        mapx = 0
                        mapy = 0
                    

                if(bReadCmd):
                    if(word == "@next"):

                        self.nextMap = words[currentWord + 1]

                        self.listNextmaps.append(words[currentWord + 1])

                        self.alistNextmaps[words[currentWord + 1]] = [int(words[currentWord + 2]), int(words[currentWord + 3]), pygame.image.load(os.path.join('images', words[currentWord + 4] + '.png'))]
                        
                        break

                    elif(word == "@player"):
                        
                        if(words[currentWord + 2] == "position"):
                            
                            self.player[int(words[currentWord + 1])].setPosition(int(words[currentWord + 3]), int(words[currentWord + 4]))
                            break

                        if(words[currentWord + 1] == "hp"):
                            
                            self.player[game.active_player].health = int(words[currentWord + 2])
                            break

                        if(words[currentWord + 1] == "area"):
                            
                            self.player[game.active_player].x = random.randint(int(words[currentWord + 2]), int(words[currentWord + 4]))
                            self.player[game.active_player].y = random.randint(int(words[currentWord + 3]), int(words[currentWord + 5]))           
                            break

                        if(words[currentWord + 1] == "item"):
                            
                            self.player.addItem(copy.copy(self.allListItems[words[currentWord + 2]]))
                            break

                    elif(word == "@spawn"):

                        if(words[currentWord + 1] == "unit"):

                            self.listUnits.append(copy.copy(self.allListUnits[words[currentWord + 2]]))                            

                        elif(words[currentWord + 1] == "item"):

                            if(words[currentWord + 3] == "area"):

                                self.listItems.append(copy.copy(self.allListItems[words[currentWord + 2]]))
                                self.listItems[-1].spawnOnArea(int(words[currentWord + 4]),
                                                               int(words[currentWord + 5]),
                                                               int(words[currentWord + 6]),
                                                               int(words[currentWord + 7]))
                                break

                            else:
                                
                                self.listItems.append(copy.copy(self.allListItems[words[currentWord + 2]]))
                                self.listItems[-1].setPosition(int(words[currentWord + 2]), int(words[currentWord + 4]))
                                break

                    elif(word == "@test"):

                        for i in range(len(words)):
                            print(words[i])

                    elif(word == "@amap"):

                        bReadCmd = False
                        bMapLoad = True
                            

                    elif(word == "@map"):

                        if(words[currentWord + 1] == "fill"):

                            fromX = 0
                            fromY = 0
                            dX = 0
                            dY = 0
                            endFillX = 10
                            endFillY = 10
                            nY = 1
                            nX = 1
        
                            for i in range(len(words)):
                                if(words[i] == "-s"):
                                    fromX = int(words[i + 1])
                                    fromY = int(words[i + 2])
                                elif(words[i] == "-d"):
                                    dX = int(words[i + 1])
                                    nX = int(words[i + 2])
                                    dY = int(words[i + 3])
                                    nY = int(words[i + 4])

                            for y in range(endFillY):
                                for x in range(endFillX):
                                    try:
                                        self.landmap[(fromY + y) * nY + dY][(fromX + x) * nX + dX] = int(words[currentWord + 2])                                  
                                    except:
                                        pass
                                    

                        elif(words[currentWord + 1] == "clear"):
                        
                            self.landmap = [
                                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
                            ]
                            break

                        elif(words[currentWord + 1] == "waypoint"):

                            self.mapWay(int(words[currentWord + 2]),
                                        int(words[currentWord + 3]),
                                        int(words[currentWord + 4]),
                                        int(words[currentWord + 5]),
                                        int(words[currentWord + 6]),
                                        int(words[currentWord + 7]))
                            break

                        elif(words[currentWord + 1] == "downdecors"):
                            
                            self.listDecors.append(
                                decors.staticDecor(
                                    pygame.image.load(os.path.join('images', words[currentWord + 2] + '.png')),
                                    False, int(words[currentWord + 3]),
                                    int(words[currentWord + 4]),
                                    int(words[currentWord + 5]),
                                    int(words[currentWord + 6])
                                )
                            )
                            
                            break

                        elif(words[currentWord + 1] == "updecors"):

                            self.listDecors.append(decors.staticDecor(pygame.image.load(os.path.join('images', words[currentWord + 2] + '.png')), True, int(words[currentWord + 3]), int(words[currentWord + 4]), int(words[currentWord + 5]), int(words[currentWord + 6])))
                            break

                        elif(words[currentWord + 1] == "counts"):

                            self.countFloor = int(words[currentWord + 2])
                            self.countWalls = int(words[currentWord + 3])
                            self.countTraps = int(words[currentWord + 4])
                            break

                        elif(words[currentWord + 1] == "tile"):
                    
                            self.assTiles[int(words[currentWord + 2])] = pygame.image.load(os.path.join('images', words[currentWord + 3] + '.png'))

                            break

                        elif(words[currentWord + 1] == "tile-type"):
                    
                            self.assTileType[int(words[currentWord + 2])] = words[currentWord + 3]

                            break

                        elif(words[currentWord + 1] == "drop"):
                            if(words[currentWord + 2] == "floor"):
                                for i in range(int(words[currentWord + 4])):
                                    self.floormap[random.randint(0, 9)][random.randint(0, 9)] = int(words[currentWord + 3])
                                break

                        elif(words[currentWord + 1] == "set"):

                            self.landmap[int(words[currentWord + 4])][int(words[currentWord + 3])] = int(words[currentWord + 2])

                    currentWord += 1

        for i in range(10):
            for j in range(10):
                if(self.assTileType[self.landmap[i][j]] == "floor"):
                    self.free_tiles.append(i)
                    self.free_tiles.append(j)

    def fillMap(self, fill):

        for i in range(10):
            for j in range(10):
                self.landmap[i][j] = fill

    def mapWay(self, fromX, fromY, toX, toY, points, tile):

        wayX = fromX
        wayY = fromY

        self.landmap[wayY][wayX] = tile

        while(points != 0):

            x = random.randint(0, 9)
            y = random.randint(0, 9)

            # self.listDecors.append(decors.testBeacon(x, y))
            
            while(wayX != x or wayY != y):

                if(wayX == x and wayY > y): # UP
                    wayY -= 1
                elif(wayX < x and wayY > y): # UP-RIGHT
                    wayX += 1
                    wayY -= 1
                elif(wayX < x and wayY == y): # RIGHT
                    wayX += 1
                elif(wayX < x and wayY < y): # DOWN-RIGHT
                    wayX += 1
                    wayY += 1
                elif(wayX == x and wayY < y): # DOWN
                    wayY += 1
                elif(wayX > x and wayY < y): # DOWN-LEFT
                    wayX -= 1
                    wayY += 1
                elif(wayX > x and wayY == y): # LEFT
                    wayX -= 1
                elif(wayX > x and wayY > y): # UP-LEFT
                    wayX -= 1
                    wayY -= 1

                self.landmap[wayY][wayX] = tile
                
            points -= 1

        while(wayX != toX or wayY != toY):
            if(wayX == toX and wayY > toY): # UP
                wayY -= 1
            elif(wayX < toX and wayY > toY): # UP-RIGHT
                wayX += 1
                wayY -= 1
            elif(wayX < toX and wayY == toY): # RIGHT
                wayX += 1
            elif(wayX < toX and wayY < toY): # DOWN-RIGHT
                wayX += 1
                wayY += 1
            elif(wayX == toX and wayY < toY): # DOWN
                wayY += 1
            elif(wayX > toX and wayY < toY): # DOWN-LEFT
                wayX -= 1
                wayY += 1
            elif(wayX > toX and wayY == toY): # LEFT
                wayX -= 1
            elif(wayX > toX and wayY > toY): # UP-LEFT
                wayX -= 1
                wayY -= 1
                
            self.landmap[wayY][wayX] = tile

        #self.listDecors.append(decors.testBeacon(wayX, wayY))
    
    def genMap(self):
        
        if self.currentMap == "test":
        
            
            
            #self.listUnits.clear()
            #self.listUnits.append(units.Snake())
            #self.listUnits.append(units.Snake())
            #self.listUnits.append(units.Snake())

            self.listItems.append(items.Crowbar(5, 5))
            self.listItems.append(items.Crowbar(6, 6))
            
            self.player.x = 1
            self.player.y = 8

            #for i in range(0, 50):
                #self.landmap[random.randint(0, 9)][random.randint(0, 9)] = 1;

            # Прокладывание пути к выходу
                
            self.coordstairSprites = (8, 1)

            self.writeEvent(u"Гуляя в поле вы провалились...", (120, 120, 120))

    def CastRay(self, x, y, r, angle):

        coords = [0, 0]

        coords[0] = round(x + r * self.cosinus[round(angle / 5)])
        coords[1] = round(y - r * self.sinus[round(angle / 5)])

        return coords

    def Sgn(self, x):

        if(x == 0):
            return 0
        if(x > 0):
            return 1
        if(x < 0):
            return -1

    def Los(self, x1, y1, x2, y2):

        i = 0
        j = 0
        dx = 0
        dy = 0
        sdx = 0
        sdy = 0
        dxabs = 0
        dyabs = 0
        x = 0
        y = 0
        px = 0
        py = 0

        dx = x2 - x1
        dy = y2 - y1
        dxabs = abs(dx);
        dyabs=abs(dy);
        sdx=self.Sgn(dx);
        sdy=self.Sgn(dy);
        x=round(dyabs/2, 1);
        y=round(dxabs/2, 1);
        px=x1;
        py=y1;

        if(dxabs >= dyabs):
            for i in range(dxabs):
                y = y + dyabs
                if(y >= dxabs):
                    y = y - dxabs
                    py = py + sdy
                px = px + sdx
                try:
                    if(self.assTileType[self.landmap[py][px]] == "floor"):
                        self.surfGame.blit(self.assTiles[self.landmap[py][px]], (64 * px, 64 * py))
                    elif(self.assTileType[self.landmap[py][px]] == "wall"):
                        self.surfGame.blit(self.assTiles[self.landmap[py][px]], (64 * px, 64 * py))
                        return
                except:
                    pass
        else:
            for i in range(dyabs):
                x = x + dxabs
                if(x >= dyabs):
                    x = x - dyabs
                    px = px + sdx
                py = py + sdy
                try:
                    if(self.assTileType[self.landmap[py][px]] == "floor"):
                        self.surfGame.blit(self.assTiles[self.landmap[py][px]], (64 * px, 64 * py))
                    elif(self.assTileType[self.landmap[py][px]] == "wall"):
                        self.surfGame.blit(self.assTiles[self.landmap[py][px]], (64 * px, 64 * py))
                        return
                except:
                    pass
                                                                                
    def Render(self):
        
        #for i in range(10):
            
            #for j in range(10):
        self.surfGame.fill((0, 0, 0))

        self.surfGame.blit(self.assTiles[self.landmap[self.player[game.active_player].y][self.player[game.active_player].x]], (64 * self.player[game.active_player].x, 64 * self.player[game.active_player].y))

        for i in range(72):
                
            c = self.CastRay(self.player[game.active_player].x, self.player[game.active_player].y, 5, i * 5)
            self.Los(self.player[game.active_player].x, self.player[game.active_player].y, c[0], c[1])
                    
        #self.surfGame.blit(self.holeSprite, (self.coordstairSprites[0] * 64,
                                        #self.coordstairSprites[1] * 64))

    def RenderTile(self, x, y):
        
        if(self.landmap[x][y] == 0):
            self.surfGame.blit(self.floorSprite, (x * 64, y * 64))

    def readLine(self, width, height, text):
        
        readLineWidth = width
        readLineHeight = height
        
        readWindow = pygame.Surface((readLineWidth, readLineHeight))
        
        readLineStr = "";
        enterIsDown = False
        
        while(not enterIsDown):

            for event in pygame.event.get():
                
                if event.type == KEYDOWN:
                    
                    key = event.key
                    
                    if key == K_RETURN:
                        enterIsDown = True;
                    elif key == K_SPACE:
                        readLineStr += ' '
                    elif key == K_BACKSPACE:
                        readLineStr = readLineStr[0:len(readLineStr) - 1]
                    else:
                        readLineStr += pygame.key.name(key)
                        
            readWindow.set_alpha(50)
            readWindow.fill((50, 50, 50))
            readWindow.set_alpha(25)
            
            textSprite = self.fontDefault.render(text, 0, (150, 150, 150))
            readSprite = self.fontDefault.render(readLineStr, 0, (0, 0, 0))
            
            self.screen.blit(readWindow,
                             ((self.windowWidth - readLineWidth) / 2,
                              (self.windowHeight - readLineHeight) / 2))
            
            self.screen.blit(textSprite,
                             ((self.windowWidth - readLineWidth) / 2 + 10,
                              (self.windowHeight - readLineHeight) / 2 + 10 ))
            
            self.screen.blit(readSprite,
                             ((self.windowWidth - readLineWidth) / 2 + 10,
                              (self.windowHeight - readLineHeight) / 2 + 30 ))

            pygame.display.update()

        return readLineStr

    def RenderItems(self):

        for i in range(len(self.listItems)):
            self.listItems[i].Render(self.surfGame)

    def RenderUnits(self):

        for i in range(len(self.listUnits)):
            if(not self.listUnits[i].life):
                self.listUnits[i].Render(self, False)

        for i in range(len(self.listUnits)):
            if(self.listUnits[i].life):
                if(not self.listUnits[i].animate):
                    self.listUnits[i].Render(self, False)

    def RenderDecors(self):

        for i in range(len(self.listDecors)):
            if(not self.listDecors[i].over):
                self.listDecors[i].Render(self.surfGame)

    def RenderDecorsOver(self):

        for i in range(len(self.listDecors)):
            if(self.listDecors[i].over):
                self.listDecors[i].Render(self.surfGame)

    def RenderLandmap(self):

        self.Render()
        
        # RENDER EXISTS
        for i in range(len(self.listNextmaps)):
            self.surfGame.blit(self.alistNextmaps[self.listNextmaps[i]][2], (int(self.alistNextmaps[self.listNextmaps[i]][0]) * 64, int(self.alistNextmaps[self.listNextmaps[i]][1]) * 64))

    def RenderPlayer(self):

        self.player[game.active_player].Render(self, False)

    def RenderAll(self):

        # DELETE ITEMS
        for i in range(len(self.listItems) - 1, -1, -1):
            if(self.listItems[i].delete):
                del self.listItems[i]
                    
        # DELETE ENEMIES
        for i in range(len(self.listUnits) - 1, -1, -1):
            if(self.listUnits[i].health < 1 and self.listUnits[i].delete):
                del self.listUnits[i]
                            
        for i in range(len(self.player)):
            if(i != self.active_player):
                self.player[i].Render(self, True)
                print("@")

        # RENDER LANDMAP
        self.Render()

        # RENDER EXISTS
        for i in range(len(self.listNextmaps)):
            self.surfGame.blit(self.alistNextmaps[self.listNextmaps[i]][2], (int(self.alistNextmaps[self.listNextmaps[i]][0]) * 64, int(self.alistNextmaps[self.listNextmaps[i]][1]) * 64))

        # RENDER DECORS
        for i in range(len(self.listDecors)):
            if(not self.listDecors[i].over):
                self.listDecors[i].Render(self.surfGame)

        self.screen.blit(game.surfGame, (0,0))
        #pygame.display.update()
        #input()

        # RENDER ITEMS
        for i in range(len(self.listItems)):
            self.listItems[i].Render(self.surfGame)

        
                
        # RENDER DEADS
        for i in range(len(self.listUnits)):
            if(not self.listUnits[i].life):
                self.listUnits[i].Render(self, False)
                    
        # RENDER PLAYER                        
        self.player[game.active_player].Render(self, True)
        
        # UPDATE & RENDER ENEMIES
        for i in range(len(self.listUnits)):
                        
            if(self.listUnits[i].life):

                self.listUnits[i].Action(self)
                
                self.listUnits[i].Render(self, True)

        for i in range(len(self.listDecors)):
            if(self.listDecors[i].over):
                self.listDecors[i].Render(self.surfGame)

    def checkExits(self):
        for i in range(0, len(self.listNextmaps)):
            
            if(self.alistNextmaps[self.listNextmaps[i]][0] == self.player.x and
               self.alistNextmaps[self.listNextmaps[i]][1] == self.player.y):
                self.nextMap = self.listNextmaps[i]
                self.getNextMap()

    def drawOneSprite(self, sprite):
        surfTest = pygame.Surface((640, 640))
        self.surfGame.blit(sprite, (0, 0))
        self.screen.blit(game.surfGame, (0,0))
        pygame.display.update()
        input()
        
# OBJECTS
game = Game()

if(config.enterNamePlayer):
    game.player[game.active_player].name = game.readLine(300, 150, u"Введите свое имя:")
else:
    game.player[game.active_player].name = u"Игрок"

game.loadMap()
#game.genMap()
game.initGame()

# INITS
for i in range(len(game.listUnits)):
    game.listUnits[i].init(game)

game.drawCharactersInfo()

game.RenderLandmap()
game.RenderDecors()
game.RenderItems()
game.RenderUnits()
game.RenderPlayer()
game.RenderDecorsOver()

while game.life:

    turn = False
            
    # EVENTS
    for event in pygame.event.get():
        
        if event.type == QUIT:
            
            life = False
            
        elif event.type == KEYDOWN:
            
            if event.key == K_ESCAPE:
                
                game.life = False
                
                break
            
            if(game.player[game.active_player].health > 0):
                    
                if event.key == K_w:
                        
                    game.player[game.active_player].Action(game, 0)
                    turn = True
                        
                elif event.key == K_d:
                        
                    game.player[game.active_player].Action(game, 1)
                    turn = True
                        
                elif event.key == K_x:
                        
                    game.player[game.active_player].Action(game, 2)
                    turn = True
                        
                elif event.key == K_a:

                    game.player[game.active_player].Action(game, 3)
                    #game.player.Action(game, 3)
                    turn = True
                        
                elif event.key == K_SPACE or event.key == K_s:
                        
                    game.player.Action(game, 4)
                    turn = True

                elif event.key == K_t:
                    turn = True
                    game.player[game.active_player].Action(game, 5)

                elif event.key == K_e:
                    turn = True
                    game.player[game.active_player].Action(game, 7)

                elif event.key == K_q:
                    turn = True
                    game.player[game.active_player].Action(game, 8)

                elif event.key == K_z:
                    turn = True
                    game.player[game.active_player].Action(game, 9)

                elif event.key == K_c:
                    turn = True
                    game.player[game.active_player].Action(game, 10)

                elif event.key == K_i:
                    game.player[game.active_player].Action(game, 6)

                elif event.key == K_v:
                    game.player[game.active_player].Action(game, 11)

                elif event.key == K_n:
                    game.getNextMap()

                elif event.key == K_BACKQUOTE:
                    print("> ", end = '')
                    command = input()
                    if(command == "nextmap"):
                        for i in range(0, len(game.listNextmaps)):
                            print(game.listNextmaps[i] + str(game.alistNextmaps[game.listNextmaps[i]]))
                    elif(command == "flip"):
                        pygame.display.flip()

                if(turn):
                    game.RenderAll()
                    game.checkExits()

                game.active_player = game.active_player + 1
                
                if(game.active_player == len(game.player)):
                    game.active_player = 0

            else:

                game.active_player = 0
                    

    # TICK
    game.milli = game.clock.tick(40)
    game.seconds = game.milli / 1000.0

    # RENDER     
    game.screen.blit(game.surfGame, (0,0))
    pygame.display.update()

    print(game.clock.get_fps());
      
pygame.quit()
