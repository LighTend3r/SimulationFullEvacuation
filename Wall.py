
"""Consider using cartesian vectors only, and ditching the polar.  (self.vector = x, y for direction)"""
from math import pi, sqrt, cos, sin
from random import random

from pygame import sprite, Color, Surface
from pygame.locals import *

import Physics


class Wall(sprite.Sprite):
    """This is the Fish Sprite that will move around the aquarium. y-axis points DOWN"""
    count = 0

    def __init__(self, rect=None, color=None):
        sprite.Sprite.__init__(self)
        
        Wall.count += 1
        self.fishID = Wall.count

        if color is not None:
            self.color = color
        else:
            self.color = Color(200, 200, 200)

        if rect is not None:
            self.image = Surface([rect[2], rect[3]])
            self.image.fill(self.color)
            self.rect = rect
        else:
            self.image = Surface([20, 20])
            self.image.fill(self.color)
            self.rect = self.image.get_rect()