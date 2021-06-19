#! /usr/bin/env python
# -*- coding: utf-8 -*-

from pygame.locals import *

import sys
import os
import pygame

import base_config

def drawCharactersInfo(game):

    game.surfCharacter.fill((25, 25, 25))
    game.screen.blit(game.surfCharacter, (640, 0))

    textSprite = game.fontDefault.render(
                    game.player[game.active_player].name,
                    base_config.antialias,
                    (0, 100, 0)
                )

    game.screen.blit(textSprite, (650, 5))

    textHealth = game.fontDefault.render(
                    u"Здоровье: " + str(game.player[game.active_player].health),
                    base_config.antialias,
                    (0, 100, 0)
                )

    game.screen.blit(textHealth, (650, 15))

    textHealth = game.fontDefault.render(
                    u"Режим: " + game.player[game.active_player].interaction,
                    base_config.antialias,
                    (0, 100, 0)
                )

    game.screen.blit(textHealth, (760, 15))

    textMissClose = game.fontDefault.render(
                        u"Навык владения ближним боем: "
                        + str(10 - game.player[game.active_player].missClose),
                        base_config.antialias, (0, 100, 0)
                    )

    game.screen.blit(textMissClose, (650, 25))


    # DRAW PLAYERS ITEMS

    for i in range(3):
        for j in range(4):

            game.screen.blit(game.cellSprite, (j * 64 + 640, i * 64 + 128))

            if(game.player[game.active_player].items[i * 4 + j] != 0):
                game.screen.blit(
                    game.player[game.active_player].items[i * 4 + j].sprite,
                    (j * 64 + 640, i * 64 + 128)
                )
