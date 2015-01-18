import pygame, math
from rtslib.sheet import *

class tdent():
	def __init__(self, posX, posY, desX, desY, isSelected, speed, sheet, UIsprite, type):
		self.pos = [posX, posY]
		self.des = [desX, desY]
		self.isSelected = isSelected 
		self.speed = speed
		self.sheet = sheet
		self.sheetCounter = 0
		self.isMoving = False
		self.UIsprite = UIsprite 
		self.type = type # 0 = worker, 1 = town hall, 2 = resource, 3 = barracks
		self.timer = -1 # positive means working, 0 is currently doing a task, -1 is finished
		self.command = pygame.K_z # z
		
	def draw(self, surface):
		surface.blit(self.sheet.getImage(), self.pos)
		if self.timer > 0:
			pass # display universal working symbol
		elif self.isMoving:
			self.sheetCounter+=1
			if self.sheetCounter == 10: # 10 frames a sheet 
				self.sheet.nextImage()
				self.sheetCounter = 0
		if self.isSelected:
			self.drawSelectionMarker(surface)
			self.drawDestinationMarker(surface)
			surface.blit(self.UIsprite, (1280-self.UIsprite.get_width(), 720-self.UIsprite.get_height())) # display UI
	
	def update(self, world):
		if self.timer < 0:
			self.move()
		else:
			if self.timer == 0:
				self.action(world, self.command)
			self.timer -= 1
	
	def setDes(self, des):
		self.des[0], self.des[1] = des
		
	def setSel(self, isSelected):
		self.isSelected = isSelected
		
	def move(self):
		if (self.des[0] - self.pos[0])**2 + (self.des[1] - self.pos[1])**2 > (self.speed)**2: # just go there if close enough
			self.isMoving = True 
			xDis = self.des[0] - self.pos[0]
			yDis = self.des[1] - self.pos[1]
			Dis = abs(xDis) + abs(yDis) 
			self.pos[0] += self.speed*xDis/Dis 
			self.pos[1] += self.speed*yDis/Dis
		else:
			self.isMoving = False 
			self.pos[0], self.pos[1] = self.des[0], self.des[1]
			self.sheetCounter = 0
			
	def drawSelectionMarker(self, surface): # RED
		pygame.draw.polygon(surface, (255, 0, 0), [self.pos, \
									  [self.pos[0] + self.sheet.dim[0], self.pos[1]], \
									  [self.pos[0] + self.sheet.dim[0], self.pos[1] + self.sheet.dim[1]], \
									  [self.pos[0], self.pos[1] + self.sheet.dim[1]]], \
									  2)
								
	def drawDestinationMarker(self, surface): # RED
		pygame.draw.circle(surface, (255, 0, 0), self.des, 6, 2)
				
############################################################################ 

	def action(self, world, eventKey):
		if self.type == 0: 
			if eventKey == pygame.K_w:
				if self.timer == 0:
					self.spawnBarracks(world)
				else:
					self.timer = 1*60
		elif self.type == 1:
			if eventKey == pygame.K_w: 
				if self.timer == 0:
					self.spawnWorker(world)
				else:
					self.timer = 1*60
		elif self.type == 2:
			if eventKey == "w": # w for wood
				self.addWood(world)
		elif self.type == 3:
			if eventKey == pygame.K_w:
				if self.timer == 0:
					self.spawnSoldier(world)
				else:
					self.timer = 1*60
			elif eventKey == pygame.K_e:
				if self.timer == 0:
					self.upgradeWorker(world)
				else:
					self.timer = 5*60
		self.command = eventKey
		
	def addWood(self, world):
		world.wood += 1.0
		
	def spawnWorker(self, world):
		world.pop += 1
		world.food -= 10
		world.entities.append(tdent(self.pos[0], self.pos[1], self.des[0], self.des[1], \
							False, 0.50, sheet("resources/stickman.png", [32, 32]), \
							pygame.image.load("resources/GameBottomBar.png").convert_alpha(), 0)) # worker
		world.entities[-1].sheet.setFlipped(world.f)
		world.f = not world.f
	
	def spawnBarracks(self, world):
		world.wood -= 20
		world.entities.append(tdent(self.pos[0], self.pos[1], self.des[0], self.des[1], \
							 False, 0, sheet("resources/Barracks.png", [320, 320]), \
							 pygame.image.load("resources/GameBottomBar.png").convert_alpha(), 0))
	
	def spawnSoldier(self, world):
		world.food -= 10 
		world.wood -= 10
		# spawn Soldier
	
	def upgradeWorker(self, world):
		pass 
		# resources -= 100
		# upgrade worker