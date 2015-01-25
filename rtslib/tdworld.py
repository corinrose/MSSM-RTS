import pygame
from rtslib.tdent import *
from rtslib.sheet import *

class tdworld():
	def __init__(self, game):
		self.entities = [tdent(400, 400, 400, 400, \
							   True, 0, sheet("resources/TownHall.png", [160,160]), \
							   "Town Hall. Press w to train worker : 10 food, 1 pop", 1.1), \
						tdent(50, 50, 200, 200, \
							   False, 0, sheet("resources/Wood.png", [80,80]), \
							   "Wood", 2.2), \
						tdent(500, 270, 270, 270, \
							   False, 0, sheet("resources/Gold.png", [80,80]), \
							   "Gold", 2.3)]
		self.poplimit = 10.0
		self.pop = 0.0
		self.food = 100.0
		self.wood = 50.0
		self.gold = 0.0
		self.topBarText = pygame.font.SysFont("monospace", 14) # text for top bar
		self.UIelements = [[pygame.image.load("resources/ui/GameBottomBar.png").convert_alpha(), (1280 - pygame.image.load("resources/ui/GameBottomBar.png").convert_alpha().get_width(), 720 - pygame.image.load("resources/ui/GameBottomBar.png").convert_alpha().get_height())], \
						   [pygame.image.load("resources/ui/GameTopBar.png").convert_alpha(), (0,0)], []] # defined in update
		self.background = pygame.image.load("resources/GameGrass.png").convert_alpha()
		self.unitDictionary = {3.1:"knight"}
		self.game = game
		
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
			for ent2 in self.entities: 
				if ent.type == 0 and round(ent2.type) == 2: # handles resource gathering
					if ent2.pos[0] < ent.pos[0] < ent2.pos[0] + ent2.sheet.dim[0] and \
					   ent2.pos[1] < ent.pos[1] < ent2.pos[1] + ent2.sheet.dim[1]:
						ent2.action(self, "") 
				if (ent.pos[0] - ent2.pos[0])**2 + (ent.pos[1] - ent2.pos[1])**2 > 0 and \
				      (ent.pos[0] - ent2.pos[0])**2 + (ent.pos[1] - ent2.pos[1])**2 < 20**2: # built-in proximity limit  # handles collision
					tmp0 = ent.pos[0]
					tmp1 = ent.pos[1]
					xDis = ent2.pos[0] - ent.pos[0]
					yDis = ent2.pos[1] - ent.pos[1]
					Dis = abs(xDis) + abs(yDis) 
					ent.pos[0] -= ent.speed*xDis/Dis 
					ent.pos[1] -= ent.speed*yDis/Dis
					xDis = tmp0 - ent2.pos[0]
					yDis = tmp1 - ent2.pos[1]
					Dis = abs(xDis) + abs(yDis) 
					ent2.pos[0] -= ent2.speed*xDis/Dis 
					ent2.pos[1] -= ent2.speed*yDis/Dis
		self.gold += self.pop * 10.0 / 3600.0 # 10 gold per min per pop - gold trickle based on population
		self.UIelements[2] = [self.topBarText.render(     "pop: " + str(int(self.pop)) + "/" + str(int(self.poplimit)) + \
													"    food: " + str(int(self.food)) + \
													"    wood: " + str(int(self.wood)) + \
													"    gold: " + str(int(self.gold)), 1, (255,255,0)), (10, 10)] # update resource UI
	
	def draw(self, surface):
		surface.blit(self.background, (0,0)) # draw background
		for ent in self.entities: # draw units, buildings, resources
			ent.draw(surface)
			if ent.isSelected: # blits unit UI bar + text
				surface.blit(self.UIelements[0][0], self.UIelements[0][1])
				ent.drawUIText(surface)
		for i in range(1, len(self.UIelements)): # draw general UI (0 is unit UI)
			surface.blit(self.UIelements[i][0], self.UIelements[i][1])

		