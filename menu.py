import pygame, sys

class menu():
	def __init__(self):
		self.state = "main"
		
	def draw(self, surface):
		surface.fill([255,0,0])
		
	def update(self, events):
		for event in events:
			if event.type == pygame.MOUSEBUTTONDOWN:
				print "MENU CLUNK"
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_RETURN:
					print "ENTER"