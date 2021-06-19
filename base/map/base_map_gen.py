#! /usr/bin/env python
# -*- coding: utf-8 -*-

import pygame
from pygame.locals import *
import random

import base_config

def mapWay(map, fromX, fromY, toX, toY, points, tile):

    wayX = fromX
    wayY = fromY

    map.landmap[wayY][wayX] = tile

    while(points != 0):

        x = random.randint(0, 9)
        y = random.randint(0, 9)

        while(wayX != x or wayY != y):

            if(wayX == x and wayY > y): # UP
                wayY -= 1
            elif(wayX < x and wayY > y): # UP-RIGHT
                wayX += 1
                wayY -= 1
            elif(wayX < x and wayY == y): # RIGHT
                wayX += 1
            elif(wayX < x and wayY < y): # DOWN-RIGHT
                wayX += 1
                wayY += 1
            elif(wayX == x and wayY < y): # DOWN
                wayY += 1
            elif(wayX > x and wayY < y): # DOWN-LEFT
                wayX -= 1
                wayY += 1
            elif(wayX > x and wayY == y): # LEFT
                wayX -= 1
            elif(wayX > x and wayY > y): # UP-LEFT
                wayX -= 1
                wayY -= 1

            map.landmap[wayY][wayX] = tile

        points -= 1

    while(wayX != toX or wayY != toY):
        if(wayX == toX and wayY > toY): # UP
            wayY -= 1
        elif(wayX < toX and wayY > toY): # UP-RIGHT
            wayX += 1
            wayY -= 1
        elif(wayX < toX and wayY == toY): # RIGHT
            wayX += 1
        elif(wayX < toX and wayY < toY): # DOWN-RIGHT
            wayX += 1
            wayY += 1
        elif(wayX == toX and wayY < toY): # DOWN
            wayY += 1
        elif(wayX > toX and wayY < toY): # DOWN-LEFT
            wayX -= 1
            wayY += 1
        elif(wayX > toX and wayY == toY): # LEFT
            wayX -= 1
        elif(wayX > toX and wayY > toY): # UP-LEFT
            wayX -= 1
            wayY -= 1

        map.landmap[wayY][wayX] = tile
