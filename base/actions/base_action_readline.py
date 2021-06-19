#! /usr/bin/env python
# -*- coding: utf-8 -*-

import pygame
from pygame.locals import *

def readLine(self, width, height, text):

    readLineWidth = width
    readLineHeight = height

    readWindow = pygame.Surface((readLineWidth, readLineHeight))

    readLineStr = "";
    enterIsDown = False

    while (not enterIsDown):

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

        textSprite = self.fontDefault.render(
            text, config.antialias, (150, 150, 150)
        )

        readSprite = self.fontDefault.render(
            readLineStr, config.antialias, (0, 0, 0)
        )

        self.screen.blit(readWindow,
                         ((self.windowWidth - readLineWidth) / 2,
                          (self.windowHeight - readLineHeight) / 2))

        self.screen.blit(textSprite,
                         ((self.windowWidth - readLineWidth) / 2 + 10,
                          (self.windowHeight - readLineHeight) / 2 + 10 ))

        self.screen.blit(readSprite,
                         ((self.windowWidth - readLineWidth) / 2 + 10,
                          (self.windowHeight - readLineHeight) / 2 + 30 ))

        pygame.display.update(self.surfGame)

    return readLineStr
