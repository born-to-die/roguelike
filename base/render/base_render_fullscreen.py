#! /usr/bin/env python
# -*- coding: utf-8 -*-

from pygame.locals import *

import sys
import os
import pygame

import base_config
import base_ui

def changeFullscreen(game):

    if(game.fullscreen):
        game.fullscreen = False
        screen = pygame.display.set_mode(
            (game.window_width, game.window_height),
            (pygame.FULLSCREEN | pygame.DOUBLEBUF | pygame.HWSURFACE),
            0,
            32
        )
    else:
        game.fullscreen = True
        screen = pygame.display.set_mode(
            (game.window_width, game.window_height),
            0,
            32
        )

    base_ui.drawCharactersInfo(game)
