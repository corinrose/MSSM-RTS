import pygame
from rtslib.tdent import *
from rtslib.sheet import *

class tdworld():
	def __init__(self):
		self.entities = []
		self.f = False # for spritesheet alternating flipping
		
	def update(self, events):
	    for event in events:
			if event.type == pygame.MOUSEBUTTONDOWN:
				self.entities.append(tdent(200, 200, 400, 400, 0.25, sheet("resources/stickman.png", [32, 32]))) ### testing purposes
				self.entities[-1].sheet.setFlipped(self.f)
				self.f = not self.f	
	    for ent in self.entities:
		    ent.update()
	
	def draw(self, surface):
		for ent in self.entities:
			ent.draw(surface)
		