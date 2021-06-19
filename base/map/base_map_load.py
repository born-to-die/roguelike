#! /usr/bin/env python
# -*- coding: utf-8 -*-

from pygame.locals import *

import sys
import os
import pickle
import pygame

import base_config
import base_map
import base_map_gen

def loadMap(map, loadmap, assTileType, assTiles, player, active_player, free_tiles):

    file = open(loadmap + ".map", 'r')

    bMapLoad = False
    bReadCmd = True
    mapLine = 0
    mapx = 0
    mapy = 0

    for line in file:

        words = line.split()

        currentWord = 0

        for word in words:

            if(bMapLoad):

                map.landmap[mapy][mapx] = int(word)

                assTileType[int(word)] = "floor"

                mapx += 1

                if(mapx == 10):
                    mapx = 0
                    mapy += 1

                if(mapy == 10):
                    bMapLoad = False
                    bReadCmd = True
                    mapx = 0
                    mapy = 0


            if(bReadCmd):
                if(word == "@next"):

                    self.nextMap = words[currentWord + 1]

                    self.listNextmaps.append(words[currentWord + 1])

                    self.alistNextmaps[words[currentWord + 1]] = [
                        int(words[currentWord + 2]),
                        int(words[currentWord + 3]),
                        pygame.image.load(os.path.join('src/gfx', words[currentWord + 4] + '.png'))
                    ]

                    break

                elif(word == "@player"):
                    with open('data.pickle', 'rb') as f:
                        player[active_player] = pickle.load(f)

                    if(words[currentWord + 2] == "position"):

                        self.player[int(words[currentWord + 1])].setPosition(
                            int(words[currentWord + 3]),
                            int(words[currentWord + 4])
                        )
                        break

                    if(words[currentWord + 1] == "hp"):

                        self.player[self.active_player].health = int(words[currentWord + 2])
                        break

                    if(words[currentWord + 1] == "area"):

                        self.player[self.active_player].x = random.randint(
                            int(words[currentWord + 2]),
                            int(words[currentWord + 4])
                        )

                        self.player[self.active_player].y = random.randint(
                            int(words[currentWord + 3]),
                            int(words[currentWord + 5])
                        )
                        break

                    if(words[currentWord + 1] == "item"):

                        self.player.addItem(copy.copy(self.allListItems[words[currentWord + 2]]))
                        break

                elif(word == "@spawn"):

                    if(words[currentWord + 1] == "unit"):

                        self.listUnits.append(copy.copy(self.allListUnits[words[currentWord + 2]]))

                    elif(words[currentWord + 1] == "item"):

                        if(words[currentWord + 3] == "area"):

                            self.listItems.append(copy.copy(self.allListItems[words[currentWord + 2]]))
                            self.listItems[-1].spawnOnArea(
                                int(words[currentWord + 4]),
                                int(words[currentWord + 5]),
                                int(words[currentWord + 6]),
                                int(words[currentWord + 7])
                            )
                            break

                        else:

                            self.listItems.append(copy.copy(self.allListItems[words[currentWord + 2]]))
                            self.listItems[-1].setPosition(
                                int(words[currentWord + 2]),
                                int(words[currentWord + 4])
                            )
                            break

                elif(word == "@test"):

                    for i in range(len(words)):
                        print(words[i])

                elif(word == "@amap"):

                    bReadCmd = False
                    bMapLoad = True


                elif(word == "@map"):

                    if(words[currentWord + 1] == "fill"):

                        fromX = 0
                        fromY = 0
                        dX = 0
                        dY = 0
                        endFillX = 10
                        endFillY = 10
                        nY = 1
                        nX = 1

                        for i in range(len(words)):
                            if(words[i] == "-s"):
                                fromX = int(words[i + 1])
                                fromY = int(words[i + 2])
                            elif(words[i] == "-d"):
                                dX = int(words[i + 1])
                                nX = int(words[i + 2])
                                dY = int(words[i + 3])
                                nY = int(words[i + 4])

                        for y in range(endFillY):
                            for x in range(endFillX):
                                try:
                                    map.landmap[(fromY + y) * nY + dY][(fromX + x) * nX + dX] = int(words[currentWord + 2])
                                except:
                                    print("@")
                                    pass


                    elif(words[currentWord + 1] == "clear"):

                        self.landmap = [
                            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
                        ]
                        break

                    elif(words[currentWord + 1] == "waypoint"):

                        base_map_gen.mapWay(map, int(words[currentWord + 2]),
                                    int(words[currentWord + 3]),
                                    int(words[currentWord + 4]),
                                    int(words[currentWord + 5]),
                                    int(words[currentWord + 6]),
                                    int(words[currentWord + 7]))
                        break

                    elif(words[currentWord + 1] == "downdecors"):

                        self.listDecors.append(
                            decors.staticDecor(
                                pygame.image.load(os.path.join('src/gfx', words[currentWord + 2] + '.png')),
                                False, int(words[currentWord + 3]),
                                int(words[currentWord + 4]),
                                int(words[currentWord + 5]),
                                int(words[currentWord + 6])
                            )
                        )

                        break

                    elif(words[currentWord + 1] == "updecors"):

                        self.listDecors.append(decors.staticDecor(pygame.image.load(os.path.join('src/gfx', words[currentWord + 2] + '.png')), True, int(words[currentWord + 3]), int(words[currentWord + 4]), int(words[currentWord + 5]), int(words[currentWord + 6])))
                        break

                    elif(words[currentWord + 1] == "counts"):

                        self.countFloor = int(words[currentWord + 2])
                        self.countWalls = int(words[currentWord + 3])
                        self.countTraps = int(words[currentWord + 4])
                        break

                    elif(words[currentWord + 1] == "tile"):

                        assTiles[int(words[currentWord + 2])] = pygame.image.load(os.path.join('src/gfx/tiles', words[currentWord + 3] + '.png'))

                        break

                    elif(words[currentWord + 1] == "tile-type"):

                        assTileType[int(words[currentWord + 2])] = words[currentWord + 3]

                        break

                    elif(words[currentWord + 1] == "drop"):
                        if(words[currentWord + 2] == "floor"):
                            for i in range(int(words[currentWord + 4])):
                                self.floormap[random.randint(0, 9)][random.randint(0, 9)] = int(words[currentWord + 3])
                            break

                    elif(words[currentWord + 1] == "set"):

                        self.landmap[int(words[currentWord + 4])][int(words[currentWord + 3])] = int(words[currentWord + 2])

                currentWord += 1

    for i in range(10):
        for j in range(10):
            if(assTileType[map.landmap[i][j]] == "floor"):
                free_tiles.append([i, j])
