from math import sqrt
import pygame
from AI import AI

import PathFinding
import numpy as np
from random import random

import Physics
import matplotlib.pyplot as plt
FEAR_CONST = 20
ATTRACTIVE_CONST = -300000
ZONE_OF_REPULSION = 16
ZONE_OF_WALL = 10

REPULSIVE_CONST = 100000
WALL_CONST = 2.0
ZONE_OF_FEAR = 30.0


# Not usefull
def collision(rectA, rectB):

	if rectB.right < rectA.left:
		# rectB est à gauche
		right = True
		return False
	if rectB.bottom < rectA.top:
		# rectB est au-dessus
		bottom = True
		return False
	if rectB.left > rectA.right:
		# rectB est à droite
		left = True
		return False
	if rectB.top > rectA.bottom:
		# rectB est en-dessous
		top = True
		return False
	# Dans tous les autres cas il y a collision
	return True

def from_coord_to_grid(pos):
    """Retourne la position dans le niveau en indice (i, j)

    `pos` est un tuple contenant la position (x, y) du coin supérieur gauche.
    On limite i et j à être positif.
    """
    x, y = pos
    i = max(0, int(x / 25))
    j = max(0, int(y / 25))
    return i, j

def get_neighbour_blocks(niveau, i_start, j_start):
    """Retourne la liste des rectangles autour de la position (i_start, j_start).

    Vu que le personnage est dans le carré (i_start, j_start), il ne peut
    entrer en collision qu'avec des blocks dans sa case, la case en-dessous,
    la case à droite ou celle en bas et à droite. On ne prend en compte que
    les cases du niveau avec une valeur de 1.
    """
    blocks = list()
    for j in range(j_start, j_start+2):
        for i in range(i_start, i_start+2):
            if niveau[j][i] == 1:
                topleft = i*25, j*25
                blocks.append(pygame.Rect((topleft), (25, 25)))
    return blocks

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
wall=[]
for i in range(len(GRID)):
	for j in range(len(GRID)):
		if GRID[i][j] == 1:
			wall.append((i,j))

class Pnj(AI):
	"""This is the AI Sprite that will move around the street. y-axis points DOWN"""
	count = 0

	def __init__(self, rect=None, color=None, finish=None):
		AI.__init__(self, rect, color)
		Pnj.count += 1
		self.pnjID = Pnj.count
		self.MAX_SPEED_X = 2.0
		self.MAX_SPEED_Y = 2.0
		self.finish = finish
		rando = True
		# Permet d'jouter des vitesses different au PNJ
		while rando:
			a = random()
			if a >= 0.7:
				self.vitesse = a
				rando = False


	def calc_walls_forces(self, wallList):
		"""Calcule la force pour éviter les murs."""
		F_x, F_y = 0, 0
		if not wallList:
			return F_x, F_y
		for wall in wallList:
			if self.behind_me(wall):
				continue
			else:

				dx = self.rect[0] - (wall.rect[0])
				dy = self.rect[1] - (wall.rect[1])

				r = sqrt(dx**2 + dy**2)
				if r > ZONE_OF_FEAR or r == 0:
					continue
				else :
					F_x += 100000*FEAR_CONST * (dx / r**3)

		return F_x, 0

	def calc_pathFinding_forces(self, array=None):
		"""Calcule la force du chemin a suivre pour trouver le chemin"""
		n = 0
		if n == 0:
			before = False
		if n == 0:
			n+=1
		F_x, F_y = 0, 0
		start = (int((self.rect[0])//30),int((self.rect[1]+1)//30))
		if array is None:
			return F_x, F_y

		route = PathFinding.astar(array, start, self.finish)

		#x_coords = []
		#
		#y_coords = []
		#
		#for i in (range(0,len(route))):
		#
		#    x = route[i][0]
		#
		#    y = route[i][1]
		#
		#    x_coords.append(x)
		#
		#    y_coords.append(y)
		#
		## plot map and path
		#
		#fig, ax = plt.subplots(figsize=(20,20))
		#
		#ax.imshow(GRID, cmap=plt.cm.Dark2)
		#
		#ax.scatter(start[0],start[1], marker = "*", color = "yellow", s = 200)
		#
		#ax.scatter(self.finish[0],self.finish[1], marker = "*", color = "red", s = 200)
		#
		#ax.plot(x_coords,y_coords, color = "black")
		#
		#plt.show()

		if route == [] or  not route:
			return F_x, F_y
		elif len(route)>2:
			route = route[::-1]

			for i in range(3):

				dx = self.rect[0] - (route[i][0]*30)
				dy = self.rect[1] - (route[i][1]*30)
				r = sqrt(dx**2 + dy**2)
				if r == 0:
					F_x += (ATTRACTIVE_CONST / 1.) * (dx / 1.)
					F_y += (ATTRACTIVE_CONST / 1.) * (dy / 1.)
				else:
					F_x += (ATTRACTIVE_CONST / r**2) * (dx / r**2)
					F_y += (ATTRACTIVE_CONST / r**2) * (dy / r**2)
			return F_x, F_y

		elif len(route)>1:
			route = route[::-1]

			for i in range(2):

				dx = self.rect[0] - (route[i][0]*30)
				dy = self.rect[1] - (route[i][1]*30)
				r = sqrt(dx**2 + dy**2)
				if r == 0:
					F_x += (ATTRACTIVE_CONST / 1.) * (dx / 1.)
					F_y += (ATTRACTIVE_CONST / 1.) * (dy / 1.)
				else:
					F_x += (ATTRACTIVE_CONST / r**2) * (dx / r**2)
					F_y += (ATTRACTIVE_CONST / r**2) * (dy / r**2)
			return F_x, F_y
		else:
			route = route[::-1]

			for i in range(1):
				dx = self.rect[0] - route[i][0]
				dy = self.rect[1] - route[i][1]
				r = sqrt(dx**2 + dy**2)
				if r == 0:
					F_x -= (ATTRACTIVE_CONST / 1.) * (dx / 1.)
					F_y -= (ATTRACTIVE_CONST / 1.) * (dy / 1.)
				else:
					F_x -= (ATTRACTIVE_CONST / r) * (dx / r)
					F_y -= (ATTRACTIVE_CONST / r) * (dy / r)
			return F_x, F_y


	def calc_repulsive_forces(self, pnjList): # A MODIFIER
		"""Calcule la force de répulsion entre les PNJ"""
		F_x, F_y = 0, 0
		if not pnjList:
			return F_x, F_y
		for pnj in pnjList:
			if self.behind_me(pnj):
				continue
			else:
				dx = self.rect[0] - pnj.rect[0]
				dy = self.rect[1] - pnj.rect[1]
				r = sqrt(dx**2 + dy**2)
				if r == 0 or r > ZONE_OF_REPULSION:
					continue
				else:
					F_x += (REPULSIVE_CONST / r**2) * (dx / r**2)
					F_y += (REPULSIVE_CONST / r**2) * (dy / r**2)
					if dx < 0:
						F_x += 10
					else:
						F_x -= 10
					if dy < 0:
						F_y += 10
					else:
						F_x -= 10
		return F_x, F_y


	def calc_wall_forces(self, width, height):
		"""Calcule la force des bords"""
		F_x, F_y = 0, 0
		if self.rect[0] < ZONE_OF_WALL:
			F_x += WALL_CONST
		elif (self.rect[0]+self.rect[2]) > (width-ZONE_OF_WALL):
			F_x -= WALL_CONST
		if self.rect[1] < ZONE_OF_WALL:
			F_y += WALL_CONST
		elif (self.rect[1]+self.rect[3]) > (height-ZONE_OF_WALL):
			F_y -= WALL_CONST
		return F_x, F_y


	def update_velocity(self, street):

		"""Update the fishes velocity based on forces from other pnj."""
		# Stay near other pnj, but not too close, and swim in same direction.
		pnjList = street.pnj_group.sprites()
		wallList = street.wall_group.sprites()
		#pnjList.remove(self)

		if 0<=self.rect[0]<=2*30 and 7*30<=self.rect[1]<=9*30:
			pygame.sprite.Sprite.kill(self)
		if 0<=self.rect[0]<=2*30 and 11*30<=self.rect[1]<=13*30:
			pygame.sprite.Sprite.kill(self)

		if 0<=self.rect[0]<=2*30 and 11.1*30<=self.rect[1]<=19*30:
			self.rect.move_ip(3, 0)

		if 0<=self.rect[0]<=2*30 and 0*30<=self.rect[1]<=8.9*30:
			self.rect.move_ip(3, 0)

		if 0<=self.rect[0]<=2*28 and 11.1*30<=self.rect[1]<=19*30:
			self.rect.move_ip(5, 0)

		if 0<=self.rect[0]<=2*28 and 0*30<=self.rect[1]<=8.9*30:
			self.rect.move_ip(5, 0)

		attractiveForces = self.calc_pathFinding_forces(array=GRID)
		repulsiveForces = self.calc_repulsive_forces(pnjList)
		wallsForces = self.calc_walls_forces(wallList)



		# Check the walls.
		wallForces = self.calc_wall_forces(street.width, street.height)
		self.xVel = 0
		self.yVel = 0
		# Calculate final speed for this step.
		allForces = [repulsiveForces, attractiveForces, wallForces, wallsForces]

		for force in allForces:
			self.xVel += force[0]*30
			self.yVel += force[1]*30

		# Ensure pnj doesn't swim too fast.
		if self.xVel >= 0:
			self.xVel = min(self.MAX_SPEED_X, self.xVel)
		else:
			self.xVel = max(-self.MAX_SPEED_X, self.xVel)
		if self.yVel >= 0:
			self.yVel = min(self.MAX_SPEED_Y, self.yVel)
		else:
			self.yVel = max(-self.MAX_SPEED_Y, self.yVel)


	def swim(self, street):
		"""Using my xVel and yVel values, take a step, so long as we don't swim out of bounds."""
		# Keep pnj in the window

		if self.rect[0]+self.xVel <= 0 or self.rect[0]+self.xVel >= street.width:
			dx = 0
		else:
			dx = self.xVel
		if self.rect[1]+self.yVel <= 0 or self.rect[1]+self.yVel >= street.height:
			dy = 0
		else:
			dy = self.yVel
		'''
		if 1 > self.vitesse >= 0.7:
			dx *= self.vitesse
			dy *= self.vitesse
		'''
		self.rect.move_ip(dx, dy)
