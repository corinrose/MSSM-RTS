from rtslib.base import *
import math

class projectile():
	def __init__(self, pos, speed, image, team, target, properties):
		self.pos = pos
		self.speed = speed
		self.image = image
		self.team = team
		self.target = target
		self.properties = properties
		self.archeight = 50
		self.flightdist = None
		self.currentdist = 0
		
	def draw(self, surface):
		if self.flightdist!=None:
			surface.blit(self.image, [self.pos[0], self.pos[1]-(self.archeight*math.sin(1.5707963*self.currentdist/self.flightdist))])
		
	def update(self, entities):
		for ent in entities:
			if ent.id == self.target:
				target = ent
		if self.flightdist==None:
			self.flightdist = distance(self.pos[0], self.pos[1], target.pos[0], target.pos[1])
		#move towards target
		#if target is hit, remove self and damage target
		#if target leaves entity list, just follow the path originally fired along
		#if target moves, move destination