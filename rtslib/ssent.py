import pygame, random
from rtslib.projectile import *
from rtslib.base import *

#TODO: Verify the offsets in collision things are working properly
class ssent():
	def __init__(self, id, dist, speed, width, sheet, path, team, health, attack, frametime, offset, teamPassthrough=False):
		self.id = id
		self.dist = dist
		self.speed = speed
		self.originalSpeed = speed
		self.width = width
		self.sheet = sheet
		self.path = path
		self.pos = self.path.calcPos(self.dist)
		self.scatter = random.randint(-5, 5)
		self.remove = False
		self.sheet.setFlipped(self.speed<0)
		self.counter = 0
		self.team = team
		self.maxhealth = health
		self.health = health
		self.attack = attack
		self.frametime = frametime
		self.teamPassthrough = teamPassthrough
		if self.attack["style"] in ("ranged","melee","suicide","heal"):
			self.attacktimer = self.attack["delay"]*60
		self.offset = offset
		self.effects = []
		self.stunned = False
		self.selected = False
		self.stopped = False
		
	def update(self, world, entities):
		if self.health <= 0:
			self.remove = True
		else:
			if not self.stunned:
				hitThisFrame = False
				if self.attacktimer>0:
					self.dist+=self.speed*(not self.stopped)
					for ent in entities:
						if abs(self.dist-ent.dist) < self.width+ent.width and self.id!=ent.id:
							if not (self.team == ent.team and ent.teamPassthrough):
								self.dist-=self.speed*(not self.stopped)
								hitThisFrame = True
				else:
					hitThisFrame = True

			self.pos = self.path.calcPos(self.dist)
			#Update spritesheet image
			if not self.stunned:
				if not hitThisFrame:
					self.counter+=1
				if self.counter == self.frametime:
					self.sheet.nextImage()
					self.counter = 0
			#Die if at the ends of the path
			if self.dist < 0 or self.dist > self.path.length:
				self.remove = True
				
			#Handle effects
			for effect in self.effects:
				if effect["time"] != -1:
					effect["time"] -= 1
					if effect["time"] == 0:
						if effect["type"] == "slow":
							self.speed = self.originalSpeed
							self.effects.remove(effect)
						if effect["type"] == "burn":
							self.health -= effect["damage"]
							effect["hits"]-=1
							if effect["hits"] == 0:
								self.effects.remove(effect)
							else:
								effect["time"] = effect["pause"]
						if effect["type"] == "stun":
							self.stunned = False
							self.effects.remove(effect)
				
			#Rewrite for multiple attacks!
			#Do a ranged attack if we have one	
			enemyInRange = False
			if not self.stunned:
				if self.attack["style"]=="ranged": #{"style":"ranged", "power":10, "range":100, "rate":5}
					for ent in entities:
						if ent.team != self.team:
							if self.distance(ent.pos) < self.attack["range"]:
								enemyInRange = True
								self.attacktimer -= 1
								if self.attacktimer <= 0:
									self.attacktimer = self.attack["delay"]*60
									props = {"team":self.team, "arc":self.attack["arc"], "onhit":self.attack["onhit"],"multitarget":self.attack["multitarget"]}
									if props["onhit"] == "damage":
										props["damage"] = self.attack["damage"]
									if props["onhit"] == "slow":
										props["percent"] = self.attack["percent"]
										props["time"] = self.attack["time"]
									if props["onhit"] == "burn":
										props["damage"] = self.attack["damage"]
										props["pause"] = self.attack["pause"]
										props["hits"] = self.attack["hits"]
									if props["onhit"] == "stun":
										props["time"] = self.attack["time"]
									if props["multitarget"]:
										props["spreadrange"] = self.attack["spreadrange"]
									world.projectiles.append(projectile([self.pos[0], self.pos[1]-self.sheet.dim[1]-self.scatter], self.attack["speed"], rtslib.common.images[self.attack["image"]], ent, props))
									break
								else:
									break
									
				#If any enemy is in melee range, count down towards the strike
				if self.attack["style"]=="melee":
					for ent in entities:
						if ent.team != self.team:
							if self.pathDistance(ent.dist) < self.attack["range"]+self.width+ent.width:
								self.attacktimer -= 1
								enemyInRange = True
								break #Found one, we're done here
					#Do a melee attack if we have one
					attacked = False #This allows it to loop through all of the enemies before resetting the attack timer so an entity can hit more than one enemy
					if self.attacktimer <= 0:
						for ent in entities:
							if ent.team != self.team:
								if self.pathDistance(ent.dist) < self.attack["range"]+self.width+ent.width:
									attacked = True
									ent.health-=self.attack["damage"]
					if attacked:
						self.attacktimer = self.attack["delay"]*60
				
				#If any enemy is in the suicide trigger range, do that
				if self.attack["style"] == "suicide":
					for ent in entities:
						if ent.team != self.team:
							if self.pathDistance(ent.dist) < self.attack["triggerrange"]+self.width+ent.width:
								self.attacktimer -= 1
								enemyInRange = True
								break #Found one, we're done here
					if self.attackTimer <= 0:
						for ent in entities:
							if ent.team != self.team:
								if self.pathDistance(ent.dist) < self.attack["range"]+self.width+ent.width:
									ent.health-=self.attack["damage"]
						self.remove = True
				if self.attack["style"] == "heal":
					for ent in entities:
						if ent.team == self.team:
							if self.pathDistance(ent.dist) < self.attack["range"]+self.width+ent.width:
								self.attacktimer -= 1
								enemyInRange = True
								break #Found one, we're done here
					if self.attacktimer <= 0:
						for ent in entities:
							if ent.team == self.team:
								if self.pathDistance(ent.dist) < self.attack["range"]+self.width+ent.width:
									ent.health += self.attack["health"]
									ent.health = clamp(ent.health, 0, ent.maxhealth)
									self.attacktimer = self.attack["delay"]*60
				#If there is no enemy in range, reset the attack timer
				if not enemyInRange:
					self.attacktimer = self.attack["delay"]*60
		
	def pathDistance(self, dist):
		return abs(self.dist - dist)
		
	def distance(self, pos):
		return math.sqrt(((pos[0]-self.pos[0]-self.offset[0])**2)+((pos[1]-self.pos[1]-self.offset[1]-self.scatter)**2))
		
	def pointIn(self, point):
		return checkWithinRect([self.pos[0]-(self.sheet.dim[0]/2)-self.offset[0], self.pos[1]-self.sheet.dim[1]-self.offset[1]-self.scatter, self.sheet.dim[0], self.sheet.dim[1]], point)
		
	def draw(self, surface, cpos):
		surface.blit(self.sheet.getImage(), [self.pos[0]-cpos-(self.sheet.dim[0]/2)-self.offset[0], self.pos[1]-self.sheet.dim[1]-self.offset[1]-self.scatter])
		if self.health!=self.maxhealth:
			pygame.draw.rect(surface, [255,0,0], [self.pos[0]-((self.sheet.dim[0])/2)-cpos-self.offset[0], self.pos[1]-self.sheet.dim[1]-5-2-self.offset[1]-self.scatter, self.sheet.dim[0], 5], 0) 
			pygame.draw.rect(surface, [0,255,0], [self.pos[0]-((self.sheet.dim[0])/2)-cpos-self.offset[0], self.pos[1]-self.sheet.dim[1]-5-2-self.offset[1]-self.scatter, self.sheet.dim[0]*(self.health/self.maxhealth), 5], 0) 
		for effect in self.effects:
			if effect["type"] == "burn":
				pygame.draw.circle(surface, [255,0,0], [int(self.pos[0]-((self.sheet.dim[0])/2)-cpos-self.offset[0]), int(self.pos[1]-self.sheet.dim[1]-5-2-self.offset[1]-self.scatter)], 10)
			if effect["type"] == "slow":
				pygame.draw.circle(surface, [0,255,0], [int(self.pos[0]-((self.sheet.dim[0])/2)-cpos-self.offset[0]), int(self.pos[1]-self.sheet.dim[1]-5-2-self.offset[1]-self.scatter)], 10)
			if effect["type"] == "stun":
				pygame.draw.circle(surface, [0,0,255], [int(self.pos[0]-((self.sheet.dim[0])/2)-cpos-self.offset[0]), int(self.pos[1]-self.sheet.dim[1]-5-2-self.offset[1]-self.scatter)], 10)
		if self.selected:
			pygame.draw.rect(surface, [255,255,0], [self.pos[0]-cpos-(self.sheet.dim[0]/2)-self.offset[0], self.pos[1]-self.sheet.dim[1]-self.offset[1]-self.scatter, self.sheet.dim[0], self.sheet.dim[1]], 1) 
			
	def predictFuture(self, timeahead):
		pos = self.path.calcPos(self.dist+(timeahead*self.speed*(not self.stopped)))
		return [pos[0]-self.offset[0], pos[1]-self.offset[1]-self.scatter]
		
	#Method called to stop a unit on the path but still have it fight	
	def stop(self):
		if not self.teamPassthrough:
			self.stopped = True
			self.teamPassthrough = True
	#Method called when a unit should start walking again
	def start(self):
		if self.stopped:
			self.stopped = False
			self.teamPassthrough = False
	
	def applyEffect(self, effect):
		etypelist = []
		for effect in self.effects:
			etypelist.append(effect["type"])
		if effect["type"] not in etypelist:
			self.effects.append(effect)
			if effect["type"] == "slow":
				self.speed*=effect["percent"]
			if effect["type"] == "burn":
				effect["time"] = effect["pause"]
			if effect["type"] == "stun":
				self.stunned = True