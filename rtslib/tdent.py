import pygame
from rtslib.sheet import *

class tdent():
	def __init__(self, posX, posY, desX, desY, speed, sheet):
		self.pos = [posX, posY]
		self.des = [desX, desY]
		self.speed = speed
		self.sheet = sheet
		
	def draw(self, surface):
		surface.blit(self.sheet.getImage(), (self.pos[0], self.pos[1]))
	
	def update(self):
		if self.pos[0] != self.des[0]:
			if self.pos[0] < self.des[0] < self.pos[0] + self.speed or self.pos[0] + self.speed < self.des[0] < self.pos[0]:
				self.pos[0] = self.des[0]
			else:
				self.pos[0] += self.speed
		elif self.pos[1] != self.des[1]:
			if self.pos[1] < self.des[1] < self.pos[1] + self.speed or self.pos[1] + self.speed < self.des[1] < self.pos[1]:
				self.pos[1] = self.des[1]
			else:
				self.pos[1] += self.speed