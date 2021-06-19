#! /usr/bin/env python
# -*- coding: utf-8 -*-

import pygame
import random
from os import path
from base_units import Unit


class Human(Unit):
    # DRAW
    sprite = pygame.image.load(path.join('src/gfx/units', 'npc1.png'))

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

        if (self.life):

            self.last_x = self.x
            self.last_y = self.y

            if (self.attacker != None):

                if (self.attacker.health <= 0):
                    self.attacker = None
                else:
                    if (self.playerIsClose(game.player)):
                        self.getMeleeAttack(game)
                    else:
                        self.moveSimpleDirect(game, game.player.x,
                                              game.player.y)
            else:
                if (self.behavior == "move"):
                    self.moveSimpleDirect(game, self.move_x, self.move_y)
