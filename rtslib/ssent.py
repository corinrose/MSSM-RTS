import pygame
from rtslib.projectile import *

class ssent():
	def __init__(self, id, dist, speed, width, sheet, path, team, health, attack, frametime, teamPassthrough=False):
		self.id = id
		self.dist = dist
		self.speed = speed
		self.width = width
		self.sheet = sheet
		self.path = path
		self.pos = self.path.calcPos(self.dist)
		self.remove = False
		self.sheet.setFlipped(self.speed<0)
		self.counter = 0
		self.team = team
		self.maxhealth = health
		self.health = health
		self.attack = attack
		self.frametime = frametime
		self.teamPassthrough = teamPassthrough
		if self.attack["style"]=="ranged" or self.attack["style"]=="melee":
			self.attacktimer = self.attack["delay"]*60
		
	def update(self, world, entities):
		if self.health <= 0:
				self.remove = True
		else:
			hitThisFrame = False
			self.dist+=self.speed
			for ent in entities:
				if abs(self.dist-ent.dist) < self.width+ent.width and self.id!=ent.id:
					if not (self.team == ent.team and ent.teamPassthrough):
						self.dist-=self.speed
						hitThisFrame = True

			self.pos = self.path.calcPos(self.dist)
			#Update spritesheet image
			if not hitThisFrame:
				self.counter+=1
			if self.counter == self.frametime:
				self.sheet.nextImage()
				self.counter = 0
			#Die if at the ends of the path
			if self.dist < 0 or self.dist > self.path.length:
				self.remove = True
				
			#Rewrite from multiple attacks!
			#Do a ranged attack if we have one	
			if self.attack["style"]=="ranged": #{"style":"ranged", "power":10, "range":100, "rate":5}
				self.attacktimer -= 1
				if self.attacktimer <= 0:
					for ent in entities:
						if ent.team != self.team:
							if self.distance(ent.pos) < self.attack["range"]:
								self.attacktimer = self.attack["delay"]*60
								props = {"arc":self.attack["arc"], "onhit":self.attack["onhit"]}
								if props["onhit"]=="damage":
									props["damage"] = self.attack["damage"]
								world.projectiles.append(projectile([self.pos[0], self.pos[1]-self.sheet.dim[1]], self.attack["speed"], rtslib.common.images[self.attack["image"]], ent, props))
								break
			
			#Do a melee attack if we have one
			if self.attack["style"]=="melee":
				self.attacktimer -= 1
				if self.attacktimer <= 0:
					for ent in entities:
						if ent.team != self.team:
							if self.pathDistance(ent.dist) < self.attack["range"]+self.width+ent.width:
								self.attacktimer = self.attack["delay"]*60
								ent.health-=self.attack["damage"]
		
	def pathDistance(self, dist):
		return abs(self.dist - dist)
		
	def distance(self, pos):
		return math.sqrt(((pos[0]-self.pos[0])**2)+((pos[1]-self.pos[1])**2))
		
	def draw(self, surface, cpos):
		surface.blit(self.sheet.getImage(), [self.pos[0]-cpos-(self.sheet.dim[0]/2), self.pos[1]-self.sheet.dim[1]])
		if self.health!=self.maxhealth:
			pygame.draw.rect(surface, [255,0,0], [self.pos[0]-((self.sheet.dim[0])/2)-cpos, self.pos[1]-self.sheet.dim[1]-5-2, self.sheet.dim[0], 5], 0) 
			pygame.draw.rect(surface, [0,255,0], [self.pos[0]-((self.sheet.dim[0])/2)-cpos, self.pos[1]-self.sheet.dim[1]-5-2, self.sheet.dim[0]*(self.health/self.maxhealth), 5], 0) 
			
	def predictFuture(self, timeahead):
		return self.path.calcPos(self.dist+(timeahead*self.speed))