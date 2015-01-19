import pygame

def generateBasicButton(size, color):
	s =  pygame.surface.Surface(size)
	s.fill(color)
	return s

class button():
	def __init__(self, name, pos, onClick, images=[generateBasicButton([75,25],[200,200,200]),generateBasicButton([75,25],[150,150,150]),generateBasicButton([75,25],[100,100,100])]):
		self.name = name
		self.pos = pos
		self.onClick = onClick
		self.images = images #First = idle, second = mouseover, third = mousedown
		self.size = [self.images[0].get_width(), self.images[0].get_height()]
		self.state = 0 #0 = idle, 1 = mouseover, 2 = mousedown
		
	def update(self, events):
		for event in events:
			if event.type == pygame.MOUSEBUTTONDOWN:
				if self.checkInside(pygame.mouse.get_pos()):
					self.state = 2
			elif event.type == pygame.MOUSEBUTTONUP:
				if self.checkInside(pygame.mouse.get_pos()):
					self.state = 0
					self.onClick(self.name)
		if self.checkInside(pygame.mouse.get_pos()):
			if self.state!=2:
				self.state = 1
		else:
			self.state=0
				
	def checkInside(self, point):
		if point[0] > self.pos[0] and point[0] < self.pos[0]+self.size[0]:
			if point[1] > self.pos[1] and point[1] < self.pos[1]+self.size[1]:
				return True
			else:
				return False
		else:
			return False
			
	def draw(self, surface):
		surface.blit(self.images[self.state], self.pos)