import random
from math import sqrt
from os import path
from pygame import image
from pygame import time

class Item:
    
    sprite = image.load(path.join('images','bar.png'))
    spriteHand = image.load(path.join('images','handbar.png'))
    
    x = 0
    y = 0

    delete = False

    def __init__(self, x, y):
        
        self.x = x
        self.y = y

    def Render(self, Surf):
        Surf.blit(self.sprite, (self.x * 64, self.y * 64))

    def setPosition(self, x, y):
        self.x = x
        self.y = y

    def spawnOnArea(self, sx, sy, fx, fy):

        self.x = random.randint(sx, fx)
        self.y = random.randint(sy, fy)

class Crowbar(Item):

    name = "Crowbar"
    typeItem = "closeweapon"
    damage = 5

    sprite = image.load(path.join('images','bar.png'))
    spriteHand = image.load(path.join('images','handbar.png'))

class Shotgun(Item):

    name = "Shotgun"
    typeItem = "closeweapon"
    damage = 10

    sprite = image.load(path.join('images','shotgun.png'))
    spriteHand = image.load(path.join('images','handShotgun.png'))

