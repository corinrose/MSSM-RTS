from rtslib.base import *
import math, pygame, rtslib

class projectile():
	def __init__(self, pos, speed, image, target, properties):
		#Basic properties
		self.pos = [pos[0], pos[1]] #pass by reference problems
		self.startpos = [pos[0], pos[1]] #pass by reference problems
		self.speed = speed
		self.image = image
		self.target = target.id
		self.properties = properties
		#Movement related
		self.steps = int(distance(self.pos[0], self.pos[1], target.pos[0], target.pos[1]-(target.sheet.dim[1]/2))/speed) #Target the center of the enemy
		self.targetposition = target.predictFuture(self.steps)
		self.targetposition[1]-=target.sheet.dim[1] #Target the center of the enemy
		self.flightdist = distance(self.pos[0], self.pos[1], self.targetposition[0], self.targetposition[1])
		self.currentdist = 0
		self.perframe = [(target.pos[0]-self.pos[0])/self.steps, (target.pos[1]-(target.sheet.dim[1]/2)-self.pos[1])/self.steps]
		#End of flight
		self.remove = False
		#Arc things
		self.arc = properties["arc"]
		if self.arc:
			self.archeight = self.flightdist/5
		
	def draw(self, surface, cpos):
		im = self.image
		if self.arc:
			angle = 57.2958279*math.atan(math.cos(3.1415926*self.currentdist/self.flightdist))
			if self.perframe[0] < 0:
				angle = -angle
			im = pygame.transform.rotate(self.image, angle)
		surface.blit(im, [self.pos[0]-cpos, self.pos[1]-(self.archeight*math.sin(3.1415926*self.currentdist/self.flightdist))])
		
	def update(self, entities):
		self.pos[0]+=self.perframe[0]
		self.pos[1]+=self.perframe[1]
		self.currentdist = distance(self.pos[0], self.pos[1], self.startpos[0], self.startpos[1])
		if self.currentdist > self.flightdist:
			hits=[]
			for ent in entities:
				if ent.id == self.target:
					hits.append(ent)
				elif self.properties["multitarget"]:			
					if distance(self.pos[0], self.pos[1], ent.pos[0], ent.pos[1])<self.properties["spreadrange"]:
						hits.append(ent)
			for ent in hits:	
				if self.properties["onhit"]=="damage":
					ent.health -= self.properties["damage"]
			self.remove = True