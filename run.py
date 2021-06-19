#! /usr/bin/env python
# -*- coding: utf-8 -*-

import pygame, sys, os
from pygame.locals import *
from game import Game
import base_config

pygame.init()

game = Game()
game.initGame()
game.life()
pygame.quit()
    
