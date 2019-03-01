import random
from math import sqrt
from os import path
from pygame import image
from pygame import time

class Decor:
    
    sprite = image.load(path.join('images','bar.png'))
    
    x = 0
    y = 0
    offsetx = 0
    offsety = 0
    over = False

    def __init__(self, x, y, offsetx, offsety):
        
        self.x = x
        self.y = y
        self.offsetx = offsetx
        self.offsety = offsety

    def Render(self, Surf):
        Surf.blit(self.sprite, (self.x * 64 + self.offsetx, self.y * 64 + self.offsety))

    def setPosition(self, x, y):
        self.x = x
        self.y = y

class testBeacon(Decor):

    over = True

    sprite = image.load(path.join('images','testBeacon.png'))

class staticDecor(Decor):

    def __init__(self, sprite, over, x, y, offsetx, offsety):
        self.sprite = sprite
        self.x = x
        self.y = y
        self.over = over
        self.offsetx = offsetx
        self.offsety = offsety
