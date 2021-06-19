#! /usr/bin/env python
# -*- coding: utf-8 -*-

import pygame
from pygame.locals import *
import config

def writeEvent(self, text, color):

    if(self.currentLineWrite > 24):

        self.surfMessages.set_alpha(200)
        self.surfMessages.fill((25, 25, 25))
        self.screen.blit(self.surfMessages, (640, 320))
        self.currentLineWrite = 0

    textSprite = self.fontDefault.render(text, 0, (color))
    self.screen.blit(textSprite, (650, 320 + self.currentLineWrite * 12))
    self.currentLineWrite += 1
