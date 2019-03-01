import pygame
from os import path
from units import Unit

class Mushrooms(Unit):

    # DRAW
    sprite = pygame.image.load(path.join('images','enemy_mushrooms.png'))

    # CHARS
    name = "Нарост грибов"
    health = 10

    # SPECS
    delete = False
    animation = False

    def getDamage(self, damage, game, attacker):
        self.health -= damage
        if(self.health < 1):
            self.life = False
            game.writeEvent(u"Нарост грибов больше не нарост", (120, 0, 0))
            self.sprite = pygame.image.load(path.join('images','lightcondaDead.png'))

    def __init__(self):
        pass
