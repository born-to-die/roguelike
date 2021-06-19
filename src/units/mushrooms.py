#! /usr/bin/env python
# -*- coding: utf-8 -*-

import pygame
from os import path
from base_units import Unit

class Mushrooms(Unit):

    # DRAW
    sprite = pygame.image.load(path.join('src/gfx/units','enemymushrooms.png'))

    # CHARS
    name = "РќР°СЂРѕСЃС‚ РіСЂРёР±РѕРІ"
    health = 10

    # SPECS
    delete = False
    animation = False

    def getDamage(self, damage, game, attacker):
        self.health -= damage
        if(self.health < 1):
            self.life = False
            game.writeEvent(u"РќР°СЂРѕСЃС‚ РіСЂРёР±РѕРІ Р±РѕР»СЊС€Рµ РЅРµ РЅР°СЂРѕСЃС‚", (120, 0, 0))
            self.sprite = pygame.image.load(path.join('src/gfx','lightconda_dead.png'))

    def __init__(self):
        pass
