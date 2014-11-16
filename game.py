import pygame, sys

class game():
	def __init__(self):
		self.state = "main"
		
	def draw(self, surface):
		surface.fill([0,255,0])
		
	def update(self, events):
		for event in events:
			if event.type == pygame.MOUSEBUTTONDOWN:
				print "GAME CLUNK"