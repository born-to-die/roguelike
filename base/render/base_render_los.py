#! /usr/bin/env python
# -*- coding: utf-8 -*-

from pygame.locals import *

import sys
import os
import pygame

import base_config

def Sgn(x):

    if(x == 0):
        return 0
    if(x > 0):
        return 1
    if(x < 0):
        return -1

# Slightly modified solution from
# http://rlgclub.ru/wiki/%D0%9F%D0%BE%D0%BB%D0%B5_%D0%B7%D1%80%D0%B5%D0%BD%D0%B8%D1%8F
def Los(game, x1, y1, x2, y2):

    i = 0
    j = 0
    dx = 0
    dy = 0
    sdx = 0
    sdy = 0
    dxabs = 0
    dyabs = 0
    x = 0
    y = 0
    px = 0
    py = 0

    dx = x2 - x1
    dy = y2 - y1
    dxabs = abs(dx);
    dyabs = abs(dy);
    sdx = Sgn(dx);
    sdy = Sgn(dy);
    x = round(dyabs / 2, 1);
    y = round(dxabs / 2, 1);
    px = x1;
    py = y1;

    if(dxabs >= dyabs):
        for i in range(int(dxabs)):
            y = y + dyabs
            if(y >= dxabs):
                y = y - dxabs
                py = py + sdy
            px = px + sdx
            try:
                if(game.assTileType[game.map.landmap[py][px]] == "floor"):
                    game.surfGame.blit(
                        game.assTiles[game.map.landmap[py][px]],
                        (64 * px, 64 * py)
                    )
                elif(game.assTileType[game.map.landmap[py][px]] == "wall"):
                    game.surfGame.blit(
                        game.assTiles[game.map.landmap[py][px]],
                        (64 * px, 64 * py)
                    )
                    return
            except:
                pass
    else:
        for i in range(int(dyabs)):
            x = x + dxabs
            if(x >= dyabs):
                x = x - dyabs
                px = px + sdx
            py = py + sdy
            try:
                if(game.assTileType[game.map.landmap[py][px]] == "floor"):
                    game.surfGame.blit(
                        game.assTiles[game.map.landmap[py][px]],
                        (64 * px, 64 * py)
                    )
                elif(game.assTileType[game.map.landmap[py][px]] == "wall"):
                    game.surfGame.blit(
                        game.assTiles[game.map.landmap[py][px]],
                        (64 * px, 64 * py)
                    )
                    return
            except:
                pass
