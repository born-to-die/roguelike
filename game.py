#! /usr/bin/env python
# -*- coding: utf-8 -*-

import math
import pygame
import sys
import os
from pygame.locals import *

sys.path.append(os.path.abspath('src'))
sys.path.append(os.path.abspath('src/units'))
sys.path.append(os.path.abspath('base/config'))
sys.path.append(os.path.abspath('base/units'))
sys.path.append(os.path.abspath('base/player'))
sys.path.append(os.path.abspath('base/decors'))
sys.path.append(os.path.abspath('base/items'))
sys.path.append(os.path.abspath('base/base_items'))
sys.path.append(os.path.abspath('base/map'))
sys.path.append(os.path.abspath('base/render'))

pygame.init()

# * Движок

import base_config
import base_player
import base_ui
import base_items
import base_map
import base_map_load
import base_render
import base_render_fullscreen

# * Враги

import mushrooms
import spider
import snake
import human
import deadhelmet


class Game:

    life = True  # флаг для жизни игры (не игрока)

    # * Окно
    window_width = base_config.window_width
    window_height = base_config.window_height
    window_title = base_config.window_title
    window_bg = (0, 0, 0)
    fullscreen = base_config.fullscreen

    # * Экран
    screen = pygame.display.set_mode(
        (window_width, window_height),
        0,
        32
    )
    surfGame = pygame.Surface((640, 640))
    surfMessages = pygame.Surface((260, 320))
    surfCharacter = pygame.Surface((260, 320))

    # * Лист объектов (текущие)
    player = [base_player.Player()]
    listUnits = []
    listItems = []
    listDecors = []

    # * Словарь предметов (все)
    alllistItems = {
        'crowbar': base_items.Crowbar(0, 0),
        'shotgun': base_items.Shotgun(0, 0)
    }

    # * Словарь врагов (все)
    allListUnits = {
        'snake': snake.Snake(),
        'spider': spider.Spider(),
        'deadhelmet': deadhelmet.Deadhelmet(),
        'human': human.Human(),
        'mushrooms': mushrooms.Mushrooms()
    }

    # * Следующие карты
    listNextmaps = []
    alistNextmaps = {}

    # * Шрифт
    fontDefaultSize = 20
    fontDefault = pygame.font.SysFont("None", fontDefaultSize)
    fontDefaultColor = (250, 250, 250)
    fontDefaultBackColor = (0, 0, 0)

    # * Счётчик
    clock = pygame.time.Clock()

    # * Окно сообщений
    currentLineWrite = 0

    # * Карта
    currentMap = "src/maps/intro"
    map = base_map.Map()
    free_tiles = []

    nextMap = None
    assTiles = {}
    assTileType = {}

    cellSprite = pygame.image.load(os.path.join('src/gfx/ui', 'cell.png'))

    active_player = 0

    CONST_PI = 3.1415926535
    cosinus = []
    sinus = []

    def __init__(self):

        pygame.display.set_caption(self.window_title)

        if not pygame.image.get_extended():
            raise SystemExit('Sorry, extended image module required')

    def initGame(self):

        base_render_fullscreen.changeFullscreen(self)

        for i in range(72):
            self.cosinus.append(math.cos(i * 5 * self.CONST_PI / 180))

        for i in range(72):
            self.sinus.append(math.sin(i * 5 * self.CONST_PI / 180))

        self.surfMessages.fill((25, 25, 25))
        self.screen.blit(self.surfMessages, (640, 320))

        self.surfCharacter.fill((25, 25, 25))
        self.screen.blit(self.surfCharacter, (640, 0))

        base_map_load.loadMap(self.map,
                              self.currentMap,
                              self.assTileType,
                              self.assTiles,
                              self.player,
                              self.active_player,
                              self.free_tiles)

        # INITS
        for i in range(len(self.listUnits)):
            self.listUnits[i].init(self)

        base_ui.drawCharactersInfo(self)

        base_render.RenderLandmap(self)
        base_render.RenderDecors(self)
        base_render.RenderItems(self)
        base_render.RenderUnits(self)
        base_render.RenderPlayer(self)
        base_render.RenderDecorsOver(self)

    def life(self):

        while self.life:

            turn = False  # флаг обозначающий ход игрока, нужен для рисовки изменений

            # EVENTS
            for event in pygame.event.get():

                if event.type == QUIT:

                    life = False

                elif event.type == KEYDOWN:

                    if event.key == K_ESCAPE:
                        self.player[self.active_player].save()
                        self.life = False

                        break

                    if (self.player[self.active_player].health > 0):

                        if event.key == K_w:

                            self.player[self.active_player].Action(self, 0)
                            turn = True

                        elif event.key == K_d:

                            self.player[self.active_player].Action(self, 1)
                            turn = True

                        elif event.key == K_x:

                            self.player[self.active_player].Action(self, 2)
                            turn = True

                        elif event.key == K_a:

                            self.player[self.active_player].Action(self, 3)
                            turn = True

                        elif event.key == K_SPACE or event.key == K_s:

                            self.player.Action(self, 4)
                            turn = True

                        elif event.key == K_t:
                            turn = True
                            self.player[self.active_player].Action(self, 5)

                        elif event.key == K_e:
                            turn = True
                            self.player[self.active_player].Action(self, 7)

                        elif event.key == K_q:
                            turn = True
                            self.player[self.active_player].Action(self, 8)

                        elif event.key == K_z:
                            turn = True
                            self.player[self.active_player].Action(self, 9)

                        elif event.key == K_c:
                            turn = True
                            self.player[self.active_player].Action(self, 10)

                        elif event.key == K_i:
                            self.player[self.active_player].Action(self, 6)

                        elif event.key == K_v:
                            self.player[self.active_player].Action(self, 11)

                        elif event.key == K_n:
                            self.getNextMap()

                        elif event.key == K_RETURN:
                            self.changeFullscreen()

                        elif event.key == K_BACKQUOTE:
                            command = input()
                            if (command == "nextmap"):
                                for i in range(0, len(self.listNextmaps)):
                                    print(self.listNextmaps[i] + str(self.alistNextmaps[self.listNextmaps[i]]))
                            elif (command == "flip"):
                                pygame.display.flip()

                        if (turn):
                            base_render.RenderAll(self)

                        self.active_player = self.active_player + 1

                        if (self.active_player == len(self.player)):
                            self.active_player = 0

                    else:
                        self.active_player = 0

            base_render.blitSurfGame(self)
            base_render.displayUpdate(self)
