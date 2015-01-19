import pygame
from rtslib.tdent import *
from rtslib.sheet import *

class tdworld():
	def __init__(self):
		self.entities = [tdent(400, 400, 400, 400, \
							   True, 0, sheet("resources/TownHall.png", [160,160]), \
							   "Town Hall. Press w to train worker : 10 food, 1 pop", 1), \
						tdent(50, 50, 200, 200, \
							   False, 0, sheet("resources/Wood.png", [80,80]), \
							   "Wood", 2.2), \
						tdent(500, 270, 270, 270, \
							   False, 0, sheet("resources/Gold.png", [80,80]), \
							   "Gold", 2.3)]
		self.f = False # for spritesheet alternating flipping
		self.pop = 0.0
		self.food = 100.0
		self.wood = 0.0
		self.gold = 0.0
		self.topBarText = pygame.font.SysFont("monospace", 14) # text for top bar
		self.UIelements = [] # defined in update
		self.background = pygame.image.load("resources/resourceViewBG.png").convert_alpha()
		
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
				elif event.button == 3: # right-click to send to destination
					for ent in self.entities:
						if ent.isSelected:
							ent.setDes(pygame.mouse.get_pos())
			elif event.type == pygame.KEYUP: # handles unit key commands
				for ent in self.entities:
					if ent.isSelected:
						ent.action(self, event.key)
		for ent in self.entities: 
			ent.update(self)
			for ent2 in self.entities: # handles resource gathering
				if round(ent2.type) == 2 and ent.type == 0: # type for resource 2.1-2.3
					if ent2.pos[0] < ent.pos[0] < ent2.pos[0] + ent2.sheet.dim[0] and \
					   ent2.pos[1] < ent.pos[1] < ent2.pos[1] + ent2.sheet.dim[1]:
						ent2.action(self, "")  # how to determine resource type
		self.gold += self.pop * 10.0 / 3600.0 # 10 gold per min per pop - gold trickle based on population
		self.UIelements = [[pygame.image.load("resources/GameTopBar.png").convert_alpha(), (0,0)], \
						   [self.topBarText.render(     "pop: " + str(round(self.pop)) + \
													"    food: " + str(round(self.food)) + \
													"    wood: " + str(round(self.wood)) + \
													"    gold: " + str(round(self.gold)), 1, (255,255,0)), (10, 10)]]
	
	def draw(self, surface):
		surface.blit(self.background, (0,0))# draw background
		for ent in self.entities:
			ent.draw(surface)
		for element in self.UIelements:
			surface.blit(element[0], element[1])

		