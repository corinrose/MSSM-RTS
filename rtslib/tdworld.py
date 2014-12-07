import pygame

class tdworld():
	def __init__(self):
		self.entities = []
		
	def update(self, events):
	    for event in events:
		    if event == pygame.mouseButtonDown:
			    tdent(200, 200, 400, 400, 1, sheet("resources/stickman.png", [32, 32])) ##### testing
	    for i in self.entities:
		    self.entities[i].update()
	
	def draw(self, surface):
		for i in self.entities:
			self.entities[i].draw(surface)
		