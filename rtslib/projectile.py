from rtslib.base import *
import math

class projectile():
	def __init__(self, pos, speed, image, target, properties):
		self.pos = pos
		self.startpos = pos
		self.speed = speed
		self.image = image
		self.target = target.id
		self.properties = properties
		self.archeight = 50
		self.steps = int(distance(self.pos[0], self.pos[1], target.pos[0], target.pos[1]-(target.sheet.dim[1]/2))/speed) #Target the center of the enemy
		self.targetposition = target.predictFuture(self.steps)
		self.targetposition[1]-=target.sheet.dim[1]/2
		self.flightdist = distance(self.pos[0], self.pos[1], self.targetposition[0], self.targetposition[1])
		self.currentdist = 0
		self.perframe = [(target.pos[0]-self.pos[0])/self.steps, (target.pos[1]-(target.sheet.dim[1]/2)-self.pos[1])/self.steps]
		
	def draw(self, surface, cpos):
		surface.blit(self.image, [self.pos[0]-cpos, self.pos[1]])#-(self.archeight*math.sin(1.5707963*self.currentdist/self.flightdist))])
		
	def update(self, entities):
		#for ent in entities:
		#	if ent.id == self.target:
		#		target = ent
		self.pos[0]+=self.perframe[0]
		self.pos[1]+=self.perframe[1]
		if distance(self.pos[0], self.pos[1], self.targetposition[0], self.targetposition[1])<5:
			self.perframe=[0,0]
		self.flightdistance = distance(self.pos[0], self.pos[1], self.startpos[0], self.startpos[1])
		#move towards target
		#if target is hit, remove self and damage target
		#if target leaves entity list, just follow the path originally fired along
		#if target moves, move destination