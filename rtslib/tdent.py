import pygame, math
from rtslib.sheet import *

class tdent():
	def __init__(self, posX, posY, desX, desY, isSelected, selectionMarker, speed, sheet, isWorking, UIsprite, type):
		self.pos = [posX, posY]
		self.des = [desX, desY]
		self.isSelected = isSelected 
		self.selectionMarker = selectionMarker 
		self.speed = speed
		self.sheet = sheet
		self.sheetCounter = 0
		self.isMoving = False
		self.isWorking = isWorking
		self.UIsprite = UIsprite 
		self.type = type # 0 = worker, 1 = town hall, 2 = resource
		
	def draw(self, surface):
		surface.blit(self.sheet.getImage(), self.pos)
		if self.isMoving:
			self.sheetCounter+=1
			if self.sheetCounter == 10: # 10 frames a sheet 
				self.sheet.nextImage()
				self.sheetCounter = 0
		if self.isWorking:
			pass # display universal working symbol
		if self.isSelected:
			surface.blit(self.selectionMarker, self.pos)
			surface.blit(self.selectionMarker, self.des) # should get a different destination marker
			# surface.blit(self.UIsprite, )
	
	def update(self):
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
	
	def setDes(self, des):
		self.des[0], self.des[1] = des
		
	def setSel(self, isSelected):
		self.isSelected = isSelected
		
	def action(self, tmp, eventKey):
		if self.type == 0: 
			if eventKey == pygame.K_w: # w
				pass # special worker ability
		elif self.type == 1:
			if eventKey == pygame.K_w: # w
				# resources -= 10
				tmp.entities.append(tdent(self.pos[0], self.pos[1], self.des[0], self.des[1], \
									 False, pygame.image.load("resources/selectionMarker.png").convert_alpha(), 0.50, sheet("resources/stickman.png", [32, 32]), \
									 False, "UI SPRITE HERE", 0)) # worker
				tmp.entities[-1].sheet.setFlipped(tmp.f)
				tmp.f = not tmp.f