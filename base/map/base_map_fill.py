#! /usr/bin/env python
# -*- coding: utf-8 -*-

from pygame.locals import *

import pygame

import base_config

def fillMap(self, fill):

    for i in range(10):
        for j in range(10):
            self.landmap[i][j] = fill
