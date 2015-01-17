import pygame
from rtslib.tdent import *
from rtslib.sheet import *

class tdworld():
	def __init__(self):
		self.entities = [tdent(400, 400, 200, 200, \
							   True, pygame.image.load("resources/selectionMarker.png").convert_alpha(), 0, sheet("resources/TownHall.png", [32, 32]), \
							   False, "UI SPRITE HERE", 1)]
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
				for ent in self.entities:
					if ent.isSelected:
						ent.action(self, event.key)
		for ent in self.entities:
			ent.update()
			ent.working = False
			for ent2 in self.entities:
				if ent2.type == 2 and ent.type == 0:
					if ent2.pos[0] < ent.pos[0] < ent2.pos[0] + ent2.sheet.dim[0] and \
					   ent2.pos[1] < ent.pos[1] < ent2.pos[2] + ent2.sheet.dim[1]:
						ent.isWorking = True 
						ent2.action(self, "placeholder")
	
	def draw(self, surface):
		for ent in self.entities:
			ent.draw(surface)

		