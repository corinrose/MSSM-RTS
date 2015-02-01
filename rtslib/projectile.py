from rtslib.base import *
import math, pygame

class projectile():
	def __init__(self, pos, speed, image, target, properties):
		#Basic properties
		self.pos = [pos[0], pos[1]] #pass by reference problems
		self.startpos = [pos[0], pos[1]] #pass by reference problems
		self.speed = speed
		self.image = image
		self.target = target.id
		self.properties = properties
		self.archeight = 50
		#Movement related
		self.steps = int(distance(self.pos[0], self.pos[1], target.pos[0], target.pos[1]-(target.sheet.dim[1]/2))/speed) #Target the center of the enemy
		self.targetposition = target.predictFuture(self.steps)
		self.targetposition[1]-=target.sheet.dim[1]/2 #Target the center of the enemy
		self.flightdist = distance(self.pos[0], self.pos[1], self.targetposition[0], self.targetposition[1])
		self.currentdist = 0
		self.perframe = [(target.pos[0]-self.pos[0])/self.steps, (target.pos[1]-(target.sheet.dim[1]/2)-self.pos[1])/self.steps]
		#End of flight
		self.remove = False
		
	def draw(self, surface, cpos):
		#im = self.image
		im = pygame.transform.rotate(self.image, 57.295827908797774375395898255342*math.atan(math.cos(3.1415926*self.currentdist/self.flightdist)))
		surface.blit(im, [self.pos[0]-cpos, self.pos[1]-(self.archeight*math.sin(3.1415926*self.currentdist/self.flightdist))])
		
	def update(self, entities):
		self.pos[0]+=self.perframe[0]
		self.pos[1]+=self.perframe[1]
		self.currentdist = distance(self.pos[0], self.pos[1], self.startpos[0], self.startpos[1])
		if self.currentdist > self.flightdist:
			for ent in entities:
				if ent.id == self.target:
					ent.health -= 10
					self.remove = True
		