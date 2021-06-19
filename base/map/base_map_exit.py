#! /usr/bin/env python
# -*- coding: utf-8 -*-

import pygame
from pygame.locals import *
import config

def checkExits(self):
    for i in range(0, len(self.listNextmaps)):

        if(self.alistNextmaps[self.listNextmaps[i]][0] == self.player.x and
           self.alistNextmaps[self.listNextmaps[i]][1] == self.player.y):
            self.nextMap = self.listNextmaps[i]
            self.getNextMap()
