#! /usr/bin/env python
# -*- coding: utf-8 -*-

import pygame
import random
from os import path
from base_units import Unit

class Spider(Unit):

    # CHARS
    name = "РџР°СѓРє"
    damage = 3
    health = 3
    meleeClose = 3
    stringMeleeAttack = "РџР°СѓРє СѓРєСѓСЃРёР» РІР°СЃ!"
    stringMiss = "РџР°СѓРє РїСЂРѕРјР°С…РЅСѓР»СЃСЏ РїРѕ РІР°Рј"
    sprite = pygame.image.load(path.join('src/gfx/units', 'spider.png'))

    # SPECS
    delete = False
    directx = 1
    directy = 1
    playerIs = False

    def getDamage(self, damage, game, attacker):
        self.health -= damage
        if(self.health < 1):
            self.life = False
            game.writeEvent(u"РџР°СѓРє Р±РѕР»СЊС€Рµ РЅРµ РґРІРёРіР°РµС‚СЃСЏ...", (120, 0, 0))
            self.sprite = pygame.image.load(path.join('src/gfx/units','spider_dead.png'))

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
