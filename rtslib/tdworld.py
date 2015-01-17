import pygame
from rtslib.tdent import *
from rtslib.sheet import *

class tdworld():
	def __init__(self):
		self.entities = [tdent(400, 400, 200, 200, True, pygame.image.load("resources/selectionMarker.png").convert_alpha(), 0, sheet("resources/TownHall.png", [32, 32]), 1)]
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
				elif event.button == 3: # right-click to send to destinatio
					for ent in self.entities:
						if ent.isSelected:
							ent.setDes(pygame.mouse.get_pos())
			elif event.type == pygame.KEYUP: 
				if event.key == pygame.K_w: # w to spawn worker, should be replace with permanent UI
					for ent in self.entities:
						if ent.isSelected:
							tmp = self 
							ent.action(tmp)
		for ent in self.entities:
			ent.update()
	
	def draw(self, surface):
		for ent in self.entities:
			ent.draw(surface)

		