#! /usr/bin/env python
# -*- coding: utf-8 -*-

from pygame.locals import *

import sys
import os
import pygame

import base_config

def CastRay(game, x, y, r, angle):

    coords = [0, 0]

    coords[0] = round(x + r * game.cosinus[int(round(angle / 5))])
    coords[1] = round(y - r * game.sinus[int(round(angle / 5))])

    return coords
