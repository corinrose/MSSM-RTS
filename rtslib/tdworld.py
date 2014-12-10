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
				if event.button == 1: # left-click to select unit
					for ent in self.entities:
						if ent.pos[0] < pygame.mouse.get_pos()[0] < ent.pos[0] + ent.sheet.dim[0] and \
						   ent.pos[1] < pygame.mouse.get_pos()[1] < ent.pos[1] + ent.sheet.dim[1]: 
							ent.setSel(True)
						else:
							ent.setSel(False)
				elif event.button == 3: # right-click to send to des
					for ent in self.entities:
						if ent.isSelected:
							ent.setDes(pygame.mouse.get_pos())
			elif event.type == pygame.KEYDOWN:
				if event.key == pygame.K_w: # s to spawn worker 
					self.spawnWorker();
	    for ent in self.entities:
		    ent.update()
	
	def draw(self, surface):
		for ent in self.entities:
			ent.draw(surface)
			
	def spawnWorker(self):
		# resources -= 10
		self.entities.append(tdent(200, 200, 400, 400, True, pygame.image.load("resources/selectionMarker.png").convert_alpha(), 0.50, sheet("resources/stickman2.png", [32, 32]))) # worker
		self.entities[-1].sheet.setFlipped(self.f)
		self.f = not self.f
		