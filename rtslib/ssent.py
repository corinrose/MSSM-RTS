import pygame
from rtslib.projectile import *

class ssent():
	def __init__(self, id, dist, speed, width, sheet, path, team, health, attack):
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
		if self.attack["style"]=="ranged":
			self.attacktimer = self.attack["rate"]*60
		
	def update(self, world, entities):
		if self.health <= 0:
				self.remove = True
		else:
			self.dist+=self.speed
			for ent in entities:
				if abs(self.dist-ent.dist) < self.width+ent.width and self.dist!=ent.dist:
					self.dist-=self.speed
					if self.attack["style"] == "melee":
						if self.team != ent.team:
							ent.health-=self.attack["power"]
			self.pos = self.path.calcPos(self.dist)
			self.counter+=1
			if self.counter == 8:
				self.sheet.nextImage()
				self.counter = 0
			if self.dist < 0 or self.dist > 100:
				self.remove = True
			if self.attack["style"]=="ranged": #{"style":"ranged", "power":10, "range":100, "rate":5}
				self.attacktimer -= 1
				if self.attacktimer <= 0:
					for ent in entities:
						if ent.team != self.team:
							if self.distance(ent.pos) < self.attack["range"]:
								self.attacktimer = self.attack["rate"]*60
								world.projectiles.append(projectile(self.pos, 5, pygame.image.load("resources/arrow.png"), ent, {})) #(self, pos, speed, image, target, properties)
								break
		
	def pathDistance(self, dist):
		return abs(self.dist - dist)
		
	def distance(self, pos):
		return math.sqrt(((pos[0]-self.pos[0])**2)+((pos[1]-self.pos[1])**2))
		
	def draw(self, surface, cpos):
		#pygame.draw.circle(surface, [0,0,255], [int(self.pos[0]),int(self.pos[1])], 3, 0)
		surface.blit(self.sheet.getImage(), [self.pos[0]-cpos-(self.sheet.dim[0]/2), self.pos[1]-self.sheet.dim[1]])
		if self.health!=self.maxhealth:
			pygame.draw.rect(surface, [255,0,0], [self.pos[0]-((self.sheet.dim[0])/2)-cpos, self.pos[1]-self.sheet.dim[1]-5-2, self.sheet.dim[0], 5], 0) 
			pygame.draw.rect(surface, [0,255,0], [self.pos[0]-((self.sheet.dim[0])/2)-cpos, self.pos[1]-self.sheet.dim[1]-5-2, self.sheet.dim[0]*(self.health/self.maxhealth), 5], 0) 
			
	def predictFuture(self, timeahead):
		return self.path.calcPos(self.dist+(timeahead*self.speed))