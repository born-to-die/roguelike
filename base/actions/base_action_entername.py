#! /usr/bin/env python
# -*- coding: utf-8 -*-

import pygame
from pygame.locals import *
import config

def enterNamePlayer(self):

    if(config.enterNamePlayer):
        self.player[self.active_player].name = self.readLine(300, 150, u"Введите свое имя:")
    else:
        self.player[self.active_player].name = u"Игрок"
