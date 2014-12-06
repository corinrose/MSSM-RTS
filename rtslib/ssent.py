import pygame

class ssent():
	def __init__(self, dist, sheet, path):
		self.dist = dist
		self.sheet = sheet
		self.path = path
		self.pos = self.path.calcPos(self.dist)
		
	def update(self):
		self.dist+=0.005
		self.pos = self.path.calcPos(self.dist)
		
	def pathDistance(dist):
		return abs(self.dist - dist)
		
	def distance(pos):
		return math.sqrt(((pos[0]-self.pos[0])**2)+((pos[1]-self.pos[1])**2))
		
	def draw(self, surface):
		pygame.draw.circle(surface, [0,0,255], [int(self.pos[0]),int(self.pos[1])], 3, 0)
 