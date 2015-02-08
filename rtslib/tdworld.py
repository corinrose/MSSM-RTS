import pygame
from rtslib.tdent import *
from rtslib.sheet import *
from rtslib.button import *
import rtslib

def formatSpaces(desiredLength, string): # returns some spaces + a string
		return " "*(desiredLength - len(string)) + string
		
class tdworld():
	def __init__(self, game):
		self.entities = [tdent(400, 400, 400, 400, 
							   True, 0, sheet("resources/buildings/TownHall.png", [160,160]), 
							   "Town Hall.", 1.1), 
						tdent(50, 50, 200, 200, 
							   False, 0, sheet("resources/Wood.png", [160,160]), 
							   "Wood.", 2.2), 
						tdent(500, 270, 270, 270, 
							   False, 0, sheet("resources/Gold.png", [80,80]), 
							   "Gold.", 2.3)] 
		self.poplimit = 10.0
		self.pop = 0.0
		self.food = 100.0
		self.wood = 50.0
		self.gold = 0.0
		self.topBarText = pygame.font.Font("resources/fonts/Deutsch.ttf", 14) # text for top bar
		self.UIelements = [[rtslib.common.images["resources/ui/GameBottomBar.png"], (0, 650)], 
						   [rtslib.common.images["resources/ui/GameTopBar.png"], (0,0)], 
						   [], #This is gross. We need to change this...
						   [rtslib.common.images["resources/ui/population.png"], (5, 5)],
						   [rtslib.common.images["resources/ui/food.png"], (105, 10)],
						   [rtslib.common.images["resources/ui/wood.png"], (205, 8)],
						   [rtslib.common.images["resources/ui/gold.png"], (305, 8)]
						   ] # defined in update
		self.background = rtslib.common.images["resources/GameGrass.png"]
		self.unitDictionary = {3.11:"knight", 3.12:"crossbow", 3.13:"battleaxe"} # will eventually be a config thing
		self.game = game 
		self.selectionCoordinates = [[0,0], [0,0]]
		self.selecting = False
		### self.building = False ###
		self.selectedAlready = False
		self.entities[0].buttons = [button("Spawn Worker", [125, 670], self.entities[0].addCommand, rtslib.common.buttonSets["hud"]),
									button("Increase Pop", [235, 670], self.entities[0].addCommand, rtslib.common.buttonSets["hud"])] # one-time deal
		
	def update(self, events):
		for event in events:
			if event.type == pygame.MOUSEBUTTONDOWN: 
				if event.button == 1: # left-click to select unit
					self.selecting = True 
					self.selectionCoordinates[0] = pygame.mouse.get_pos()
				elif event.button == 3: # right-click to send to destination
					### self.building = False ###
					for ent in self.entities:
						if ent.isSelected:
							ent.setDes(pygame.mouse.get_pos())
			elif event.type == pygame.MOUSEBUTTONUP: # left-click drag
				if event.button == 1:
					self.selecting = False
		if self.selecting: # drag selection
			self.selectionCoordinates[1] = pygame.mouse.get_pos()
			
		self.selectedAlready = False 
		for ent in reversed(self.entities):
			if self.selecting:
					if (not self.selectedAlready) and ent.rectangularCollision([min(self.selectionCoordinates[0][0], self.selectionCoordinates[1][0]), 
																				  min(self.selectionCoordinates[0][1], self.selectionCoordinates[1][1])], 
																				 [max(self.selectionCoordinates[0][0], self.selectionCoordinates[1][0]), 
																				  max(self.selectionCoordinates[0][1], self.selectionCoordinates[1][1])]): # drag selection
						ent.setSel(True)
						if (self.selectionCoordinates[0][0] - self.selectionCoordinates[1][0])**2 + \
						   (self.selectionCoordinates[0][1] - self.selectionCoordinates[1][1])**2 < 5: # 5 pixel single selection radius
							self.selectedAlready = True
					elif min(self.selectionCoordinates[0][1], self.selectionCoordinates[1][1]) < 720-144: # ui size 
						ent.setSel(False)
		
		for ent in self.entities: 
			ent.update(self, events)
			for ent2 in self.entities: 
				if ent.type == 0 and round(ent2.type) == 2: # handles resource gathering
					if ent2.rectangularCollision(ent.pos, [ent.pos[0] + ent.sheet.dim[0], ent.pos[1] + ent.sheet.dim[1]]):
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
		self.UIelements[2] = [self.topBarText.render(formatSpaces(8, str(int(self.pop))) + "/" + formatSpaces(3, str(int(self.poplimit))) + \
													 formatSpaces(12, str(int(self.food))) + \
													 formatSpaces(12, str(int(self.wood))) + \
													 formatSpaces(12, str(int(self.gold))), 1, (255,255,0)), (10, 15)] # update resource UI.
	
	def draw(self, surface):
		surface.blit(self.background, (0,0)) # draw background
		for ent in self.entities: # draw units, buildings, resources
			ent.draw(surface)
		if self.selecting: # draw drag selection box 
			pygame.draw.polygon(surface, (255, 255, 0), [self.selectionCoordinates[0],
														 [self.selectionCoordinates[1][0], self.selectionCoordinates[0][1]],
														 self.selectionCoordinates[1],
														 [self.selectionCoordinates[0][0], self.selectionCoordinates[1][1]]],
														 2)
		surface.blit(self.UIelements[0][0], self.UIelements[0][1])
		for ent in self.entities:
			if ent.isSelected: # blits unit UI bar + text
				ent.drawUIText(surface)
				for button in ent.buttons:
					button.draw(surface)
		for i in range(1, len(self.UIelements)): # draw general UI (0 is unit UI)
			surface.blit(self.UIelements[i][0], self.UIelements[i][1])
			