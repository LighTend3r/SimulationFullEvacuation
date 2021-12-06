"""Consider using cartesian vectors only, and ditching the polar.  (self.vector = x, y for direction)"""
from math import pi, sqrt, cos, sin
from random import random

from pygame import sprite, Color, Surface
from pygame.locals import *

import Physics

class AI(sprite.Sprite):
    """This is the Fish Sprite that will move around the aquarium. y-axis points DOWN"""
    count = 0

    def __init__(self, rect=None, color=None):
        sprite.Sprite.__init__(self)
        
        AI.count += 1
        self.fishID = AI.count

        if color is not None:
            self.color = color
        else:
            self.color = Color(255, 0, 0)

        if rect is not None:
            self.image = Surface([rect[2], rect[3]])
            self.image.fill(self.color)
            self.rect = rect
        else:
            self.image = Surface([20, 20])
            self.image.fill(self.color)
            self.rect = self.image.get_rect()
        
        self.blindFOV = 0.01
        self.blindLeft = pi - self.blindFOV/2.
        self.blindRight = pi + self.blindFOV/2.
        self.MAX_SPEED_X = 2.0
        self.MAX_SPEED_Y = 2.0
        self.xVel = 0        
        self.yVel = 0


    def calc_orientation(self):
        """Based on xVel, yVel, which way am I facing? 
        Change to call this once per timestep!"""
        return Physics.orientation_from_components(self.xVel,self.yVel)


    def behind_me(self, otherFish):
        """Return boolean wether the other fish is behind this fish. 
        Uses xVel, yVel and position."""
        theta1 = self.calc_orientation()
        theta2 = self.direction_to(otherFish)
        return abs(theta1-theta2) > self.blindLeft and abs(theta1-theta2) < self.blindRight


    def direction_to(self, otherFish):
        """Use the two coordinates to determine direction to other fish."""
        dx = otherFish.rect[0] - self.rect[0]
        dy = otherFish.rect[1] - self.rect[1]
        return Physics.orientation_from_components(dx, dy)


    def distance_to(self, otherFish):
        """Calculate the distance to another fish."""
        myX, myY = self.rect[0], self.rect[1]
        otherX, otherY = otherFish.rect[0], otherFish.rect[1]
        return sqrt((myX-otherX)**2 + (myY-otherY)**2)