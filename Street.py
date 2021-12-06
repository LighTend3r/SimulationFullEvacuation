#!/usr/bin/env python
import sys
from random import random,randint,choice

import pygame
from pygame.locals import *
from time import sleep
import Pnj
import Physics
import Wall

import numpy as np

GRID = np.array([

    [1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1],

    [1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1],

    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],

    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],

    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],

    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],

    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],

    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],

    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],

    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],

    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],

    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],

    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],

    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],

    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],

    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],

    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],

    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],

    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],

    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]])

NUMBER_OF_PNJ = 1

grayColor = pygame.Color(128,128,128)
blackColor = pygame.Color(255,255,255)
balckGrayColor = pygame.Color(200,200,200)
whiteColor = pygame.Color(0,0,0)
greenColor = pygame.Color(0,255,0)


class Street:

	def __init__(self, width=600, height=600):
		"""Initialize pygame."""
		pygame.init()
		self.width = width
		self.height = height
		self.screen = pygame.display.set_mode((self.width, self.height))
		pygame.display.set_caption('Street')


	def draw_direction_line(self, pnj):
		"""Given a fish sprite, draw a line of motion using xVel and yVel."""
		startX = pnj.rect[0]
		startY = pnj.rect[1]
		endX = (pnj.rect[0] + 2*pnj.xVel)
		endY = (pnj.rect[1] + 2*pnj.yVel)
		pygame.draw.line(self.screen, blackColor, (startX, startY), (endX, endY), 3)

	def load_sprites(self):
		"""Load all of the fish sprites."""      
		self.pnj_group = pygame.sprite.Group()		
		'''
		for i in range(1):
			self.pnj_group.add(Pnj.Pnj(rect=pygame.Rect(15*30, 18*30, 10, 10), color=whiteColor, finish= (0,10)))
		
		for i in range(2,20):
			self.pnj_group.add(Pnj.Pnj(rect=pygame.Rect(14*30, i*30, 10, 10), color=whiteColor, finish= (0,10)))
		for i in range(2,20):
			self.pnj_group.add(Pnj.Pnj(rect=pygame.Rect(10*30, i*30, 10, 10), color=whiteColor, finish= (0,10)))
		for i in range(2,20):
			self.pnj_group.add(Pnj.Pnj(rect=pygame.Rect(18*30, i*30, 10, 10), color=whiteColor, finish= (0,10)))
		for i in range(2,20):
			self.pnj_group.add(Pnj.Pnj(rect=pygame.Rect(16*30, i*30, 10, 10), color=whiteColor, finish= (0,10)))
		for i in range(2,20):
			self.pnj_group.add(Pnj.Pnj(rect=pygame.Rect(15*30, i*30, 10, 10), color=whiteColor, finish= (0,10)))
		for i in range(2,20):
			self.pnj_group.add(Pnj.Pnj(rect=pygame.Rect(13*30, i*30, 10, 10), color=whiteColor, finish= (0,10)))
		'''
		L = [(0,8),(0,7)]
		for i in range(150):
			nb = choice(L)
			print(nb)
			self.pnj_group.add(Pnj.Pnj(rect=pygame.Rect(randint(70,590), randint(10,300), 10, 10), color=whiteColor, finish= nb))
		
		L = [(0,11),(0,12)]
		for i in range(150):
			nb = choice(L)
			print(nb)
			self.pnj_group.add(Pnj.Pnj(rect=pygame.Rect(randint(70,590), randint(300,590), 10, 10), color=whiteColor, finish= nb))
	def load_wall(self):
		wall = []
		for i in range(len(GRID)):
			for j in range(len(GRID)):
				if GRID[i][j] == 1:
					wall.append((i,j))
		self.wall_group = pygame.sprite.Group()
		for i in wall:
			self.wall_group.add(Wall.Wall(rect=pygame.Rect(i[0]*30, i[1]*30, 30, 30), color=balckGrayColor))


	def main_loop(self):

		"""The main loop for drawing into the street."""
		fpsClock = pygame.time.Clock()
		self.load_sprites()
		self.load_wall()
		#arrival = pygame.sprite.Sprite.__init__()
		

		while True:
			self.screen.fill(grayColor)
			pygame.draw.rect(self.screen,greenColor,(0*30,11*30,2*30,2*30))
			pygame.draw.rect(self.screen,greenColor,(0*30,7*30,2*30,2*30))
			self.wall_group.draw(self.screen)
			self.pnj_group.draw(self.screen)

	
			# Update the pnj velocities
			for pnj in self.pnj_group.sprites():
				pnj.update_velocity(street=self)
	
			# Move pnj                             
			for pnj in self.pnj_group.sprites():
				pnj.swim(street=self)
	
			# Draw direction arrows

			'''
			for pnj in self.pnj_group.sprites():
				self.draw_direction_line(pnj)
			'''
			
	
			# Check for all colisions among exit and pnj
			#spriteHitList = pygame.sprite.groupcollide(self.end, self.pnj_group, False, True, collided=physics.fish_collision)
	
			# Go through a list of all Event objects that happened since the last get()
			for event in pygame.event.get():
				if event.type == QUIT:
					pygame.quit()
					sys.exit()
	
				elif event.type == KEYDOWN:
					if event.key == K_a:
						Prey.REPULSIVE_CONST += 1.0
						Prey.REPULSIVE_CONST = max(0.0, Prey.REPULSIVE_CONST)
						print( 'REPULSIVE_CONST = %.1f' % Prey.REPULSIVE_CONST)
					if event.key == K_q:
						Prey.REPULSIVE_CONST -= 1.0
						Prey.REPULSIVE_CONST = max(0.0, Prey.REPULSIVE_CONST)
						print( 'REPULSIVE_CONST = %.1f' % Prey.REPULSIVE_CONST)
					if event.key == K_w:
						Prey.WALL_CONST += 1.0
						Prey.WALL_CONST = max(0.0, Prey.WALL_CONST)
						print( 'WALL_CONST = %.1f' % Prey.WALL_CONST)
					if event.key == K_s:
						Prey.WALL_CONST -= 1.0
						Prey.WALL_CONST = max(0.0, Prey.WALL_CONST)
						print( 'WALL_CONST = %.1f' % Prey.WALL_CONST)
	
			# Draw new window to the screen.
			pygame.display.update()
			fpsClock.tick(30)   # Wait long enough so fps <= 30.


def main():
	street = Street()
	street.main_loop()

if __name__ == "__main__":
	main()


