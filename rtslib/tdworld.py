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
				if event.button == 1: # left-click
					self.spawnWorker();
				if event.button == 3: # right-click
					for ent in self.entities:
						if ent.isSelected:
							ent.setDes(pygame.mouse.get_pos())
	    for ent in self.entities:
		    ent.update()
	
	def draw(self, surface):
		for ent in self.entities:
			ent.draw(surface)
			
	def spawnWorker(self):
		# resources -= 10
		self.entities.append(tdent(200, 200, 400, 400, True, pygame.image.load("resources/selectionMarker.png").convert_alpha(), 0.25, sheet("resources/stickman.png", [32, 32]))) # worker
		self.entities[-1].sheet.setFlipped(self.f)
		self.f = not self.f
		