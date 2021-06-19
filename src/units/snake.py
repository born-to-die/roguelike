#! /usr/bin/env python
# -*- coding: utf-8 -*-

import pygame
import random
from os import path
from base_units import Unit

class Snake(Unit):

    # DRAW
    sprite = pygame.image.load(path.join('src/gfx/units','snake.png'))

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