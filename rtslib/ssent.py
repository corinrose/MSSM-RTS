import pygame

class ssent():
	def __init__(self, dist, sheet, path):
		self.dist = dist
		self.sheet = sheet
		self.path = path
		self.pos = self.path.calcPos(self.dist)
		self.remove = False
		
		self.counter = 0
		
	def update(self):
		self.dist+=0.015
		self.pos = self.path.calcPos(self.dist)
		self.counter+=1
		if self.counter == 8:
			self.sheet.nextImage()
			self.counter = 0
		if self.dist > self.path.distRange[1]:
			self.remove = True
		
	def pathDistance(dist):
		return abs(self.dist - dist)
		
	def distance(pos):
		return math.sqrt(((pos[0]-self.pos[0])**2)+((pos[1]-self.pos[1])**2))
		
	def draw(self, surface, cpos):
		#pygame.draw.circle(surface, [0,0,255], [int(self.pos[0]),int(self.pos[1])], 3, 0)
		surface.blit(self.sheet.getImage(), [self.pos[0]-cpos-(self.sheet.dim[0]/2), self.pos[1]-(self.sheet.dim[1]/2)])