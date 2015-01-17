import pygame, math
from rtslib.sheet import *

class tdent():
	def __init__(self, posX, posY, desX, desY, isSelected, selectionMarker, speed, sheet, UIsprite, type):
		self.pos = [posX, posY]
		self.des = [desX, desY]
		self.isSelected = isSelected 
		self.selectionMarker = selectionMarker 
		self.speed = speed
		self.sheet = sheet
		self.sheetCounter = 0
		self.isMoving = False
		self.UIsprite = UIsprite 
		self.type = type # 0 = worker, 1 = town hall, 2 = barracks
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
			surface.blit(self.selectionMarker, self.pos)
			surface.blit(self.selectionMarker, self.des) # should get a different destination marker
			# surface.blit(self.UIsprite, ) # display UI
	
	def update(self, tmp):
		if self.timer < 0:
			self.move()
		else:
			if self.timer == 0:
				self.action(tmp, self.command)
			self.timer -= 1
	
	def setDes(self, des):
		self.des[0], self.des[1] = des
		
	def setSel(self, isSelected):
		self.isSelected = isSelected
		
	def action(self, tmp, eventKey):
		if self.type == 0: 
			if eventKey == pygame.K_w:
				if self.timer == 0:
					self.spawnBarracks(tmp)
				else:
					self.timer = 1*60
		elif self.type == 1:
			if eventKey == pygame.K_w: 
				if self.timer == 0:
					self.spawnWorker(tmp)
				else:
					self.timer = 1*60
		elif self.type == 3:
			if eventKey == pygame.K_w:
				if self.timer == 0:
					self.spawnSoldier(tmp)
				else:
					self.timer = 1*60
		self.command = eventKey
		
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
				
############################################################################ 

	def spawnWorker(self, tmp):
		if self.timer == 0:
			# resources -= 10
			tmp.entities.append(tdent(self.pos[0], self.pos[1], self.des[0], self.des[1], \
								False, pygame.image.load("resources/selectionMarker.png").convert_alpha(), 0.50, sheet("resources/stickman.png", [32, 32]), \
								"UI SPRITE HERE", 0)) # worker
			tmp.entities[-1].sheet.setFlipped(tmp.f)
			tmp.f = not tmp.f
	
	def spawnBarracks(self, tmp):
		if self.timer == 0:
			#resources -= 50 
			tmp.entities.append(tdent(self.pos[0], self.pos[1], self.des[0], self.des[1], \
								 False, pygame.image.load("resources/selectionMarker.png").convert_alpha(), 0, sheet("resources/Barracks.png", [320, 320]), \
								 "UI SPRITE HERE", 0))
	
	def spawnSoldier(self, tmp):
		pass
		# resources -= 10
		# spawn soldier