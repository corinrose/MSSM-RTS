import pygame
from rtslib.tdent import *
from rtslib.sheet import *
from rtslib.button import *
from rtslib.common import *
import rtslib # redundancy???
import random
random.seed()

def distance(point1, point2):
	return ((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2)**(0.5)

def center(self):
	return [self.pos[0] + self.sheet.dim[0]/2, self.pos[1] + self.sheet.dim[1]/2]
		
def formatSpaces(desiredLength, string): # returns some spaces + a string
	return " "*(desiredLength - len(string)) + string
		
def loadCFG(file): ########################################################################## ADD BUTTONS
	config = {}
	f = open(file, "r")
	lines = f.read().split("\n")
	f.close()
	
	Rstart = lines.index("<resources>")
	Rend = lines.index("</resources>")
	details = []
	for i in range(Rstart+1, Rend, 1):
		details.append(lines[i].split(" "))
	config["resources"] = details
	
	Nstart = lines.index("<naturals>")
	Nend = lines.index("</naturals>")
	details = []
	for i in range(Nstart+1, Nend, 1):
		details.append(lines[i].split(" "))
	config["naturals"] = details
	
	Ustart = lines.index("<units>")
	Uend = lines.index("</units>")
	details = []
	for i in range(Ustart+1, Uend, 1):
		details.append(lines[i].split(" "))
	config["units"] = details
	
	return config 
	
		
class tdworld():
	def __init__(self, game, path="resources/testlevel"):
		self.cfg = loadCFG(path+"/tdworld.cfg")
		self.entities = []
		for i in range(len(self.cfg["units"])):
			self.entities.append(tdent(int(self.cfg["units"][i][0]), int(self.cfg["units"][i][1]), int(self.cfg["units"][i][2]), int(self.cfg["units"][i][3]), 
										bool(self.cfg["units"][i][4]), float(self.cfg["units"][i][5]), 
								 sheet(self.cfg["units"][i][6], [int(self.cfg["units"][i][7]), int(self.cfg["units"][i][8])]),
								 self.cfg["units"][i][9], float(self.cfg["units"][i][10])))
		for i in range(len(self.cfg["naturals"])):
			for k in range(int(self.cfg["naturals"][i][0])):
				x = random.randint(1, 1280-int(self.cfg["naturals"][i][5]))
				y = random.randint(1, 720-int(self.cfg["naturals"][i][6]))
				j = 0
				while j < len(self.entities):
					########
					while distance(center(self.entities[j]), [x + int(self.cfg["naturals"][i][5])/2, y + int(self.cfg["naturals"][i][6])/2]) < 400:#int(self.cfg["naturals"][i][1]):
					#while (self.entities[j].pos[0]-x)**2 + (self.entities[j].pos[1]-y)**2 < 400**2:#int(self.cfg["naturals"][i][1]):
					#while self.entities[j].rectangularCollision([x,y],[x+int(self.cfg["naturals"][i][5]),y+int(self.cfg["naturals"][i][6])]):
						#print (self.entities[j].pos[0]-x)**2 + (self.entities[j].pos[1]-y)**2
						x = random.randint(1, 1280-int(self.cfg["naturals"][i][5]))
						y = random.randint(1, 720-int(self.cfg["naturals"][i][6]))
						j = -1
					j += 1
				self.entities.append(tdent(x, y, x, y, 
										bool(self.cfg["naturals"][i][2]), float(self.cfg["naturals"][i][3]), 
									 sheet(self.cfg["naturals"][i][4], [int(self.cfg["naturals"][i][5]), int(self.cfg["naturals"][i][6])]),
									 self.cfg["naturals"][i][7], float(self.cfg["naturals"][i][8])))
		self.food = float(self.cfg["resources"][0][0])
		self.wood = float(self.cfg["resources"][1][0])
		self.gold = float(self.cfg["resources"][2][0])
		self.poplimit = int(self.cfg["resources"][3][0])
		self.maxpoplimit = int(self.cfg["resources"][4][0])
		self.pop = 0
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
		self.unitDictionary = {3.11:"knight", 3.12:"crossbow", 3.13:"battleaxe", 3.21:"brother clint"} # will eventually be a config thing
		self.game = game 
		self.selectionCoordinates = [[0,0], [0,0]]
		self.selecting = False
		### self.building = False ###
		self.selectedAlready = False
		### 
		self.entities[0].buttons = [button("Spawn Worker", [125, 670], self.entities[0].addCommand, rtslib.common.buttonSets["hud"]),
									button("Increase Pop", [235, 670], self.entities[0].addCommand, rtslib.common.buttonSets["hud"])] # one-time deal # WILL BE CONFIG-ED
		###
		#self.levelPath = path 
		
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
						if ent2.type != 2.2:
							ent2.action(self, 1/60.0) # default gather speed per resource per worker 
						else:
							for ent3 in self.entities: # Horrendously Inefficient (for wood hut) ###########################################################################
								if ent3.type == 2.21 and \
								   (ent2.pos[0] - ent3.pos[0])**2 + (ent2.pos[1] - ent3.pos[1])**2 < 360**2: # radius of gathering
									ent2.action(self, 1/60.0)
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
			
		#I don't think this is how you want me to do this, but whatever
		if not self.game.ssworld.scriptstarted:
			pygame.draw.rect(surface, [255,0,0], [440, 7, 400, 25], 0)
			pygame.draw.rect(surface, [255,255,0], [440, 7, 400*(float(self.game.ssworld.startIn)/self.game.ssworld.scriptStartTime), 25], 0)
			