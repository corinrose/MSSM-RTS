import pygame, math
from rtslib.sheet import *
from rtslib.button import *

class tdent():
	def __init__(self, posX, posY, desX, desY, isSelected, speed, sheet, UIdesc, type): #,buttons=[]):
		self.pos = [posX, posY]
		self.des = [desX, desY]
		self.isSelected = isSelected 
		self.speed = speed
		self.sheet = sheet
		self.sheetCounter = 0
		self.isMoving = False
		self.type = type # 0 = worker, 1 = buildings, 2.1-2.3= resource, 3.1 = knight, etc.
		self.timer = -1 # positive means working, 0 is currently doing a task, -1 is finished
		self.command = []
		self.newCommands = []
		self.UIsprite = [pygame.font.Font("resources/fonts/Deutsch.ttf", 14).render(UIdesc, 1, (255, 255, 0)), (15, 720 - 50 + 15)] # FONT? 50 is height, 15 is buffer zone
		self.buttons = []
		
	def draw(self, surface):
		surface.blit(self.sheet.getImage(), self.pos)
		if (self.isMoving) or(self.speed == 0): 
			self.sheetCounter+=1
			if self.sheetCounter == 6: # x frames a sheet 
				self.sheet.nextImage()
				self.sheetCounter = 0
		if self.des[0] < self.pos[0] and self.speed > 0: 
			self.sheet.setFlipped(True)
		else:
			self.sheet.setFlipped(False)
		if self.isSelected:
			self.drawSelectionMarker(surface)
			if int(self.type) != 2: # not resource
				self.drawDestinationMarker(surface)
		self.drawWorkingMarker(surface)
		
	def drawUIText(self, surface):
		surface.blit(self.UIsprite[0], self.UIsprite[1]) # display unit-specific UI text
		
	def update(self, world, events):
		if self.isSelected:
			for i in range(0, len(self.buttons), 1):
				self.buttons[i].update(events)
		for command in self.newCommands:
			self.action(world, command)
		self.newCommands = []
		if self.timer < 0:
			self.move()
		else:
			if self.timer == 0:
				self.action(world, self.command[0][0])
			self.timer -= 1
		if int(self.type) == 3: # attacking units transfer
			if self.pos[0] > 1200 and self.pos[1] > 240 and self.pos[1] < 480: # arbitrary gate size 
				self.action(world, "")
	
	def setDes(self, des):
		self.des[0], self.des[1] = des
		
	def setSel(self, isSelected):
		self.isSelected = isSelected
		
	def move(self):
		if (self.des[0] - self.pos[0])**2 + (self.des[1] - self.pos[1])**2 > (self.speed)**2: # just go there if close enough
			self.isMoving = True 
			xDis = self.des[0] - self.pos[0]
			yDis = self.des[1] - self.pos[1]
			Dis = abs(xDis) + abs(yDis) 
			self.pos[0] += self.speed*xDis/Dis 
			self.pos[1] += self.speed*yDis/Dis
		else:
			self.isMoving = False 
			self.pos[0], self.pos[1] = self.des[0], self.des[1]
			if self.speed != 0:
				self.sheetCounter = 0
			
	def drawSelectionMarker(self, surface): # RED
		pygame.draw.polygon(surface, (255, 0, 0), [self.pos, \
									  [self.pos[0] + self.sheet.dim[0], self.pos[1]], \
									  [self.pos[0] + self.sheet.dim[0], self.pos[1] + self.sheet.dim[1]], \
									  [self.pos[0], self.pos[1] + self.sheet.dim[1]]], \
									  2)
									  
	def drawWorkingMarker(self, surface): # YELLOW
		if self.isSelected:
			if len(self.command) > 0 and self.timer >= 0:
				pygame.draw.polygon(surface, (255, 255, 0), [[self.pos[0], self.pos[1] - 4], \
												  [self.pos[0] + ((float(self.command[0][1]) - float(self.timer))/float(self.command[0][1]))*self.sheet.dim[0], self.pos[1] - 4]], \
												  2)
				for i in range(1, len(self.command), 1):
					pygame.draw.polygon(surface, (255, 255, 0), [[self.pos[0], self.pos[1] - 4 - 4*i], \
												  [self.pos[0] + self.sheet.dim[0], self.pos[1] - 4 - 4*i]], \
												  2)
								
	def drawDestinationMarker(self, surface): # RED
		pygame.draw.circle(surface, (255, 0, 0), self.des, 6, 2)

	def action(self, world, eventKey): ########################################################################## ADD BUTTONS
		if self.type == 0: # worker
			if eventKey == "Spawn Barracks":
				self.spawn(world, eventKey, [0, 20, 0, 0, 3*60], 
						   tdent(self.pos[0], self.pos[1], self.des[0], self.des[1], \
								False, 0, sheet("resources/buildings/Barracks.png", [160, 160]), \
								"Barracks.", 1.2), [["Spawn Knight", [125, 670]],\
													["Spawn Crossbowman", [235, 670]],\
													["Spawn Battleaxer", [345, 670]]])
			elif eventKey == "Spawn Mill":
				self.spawn(world, eventKey, [0, 20, 0, 0, 3*60], 
						   tdent(self.pos[0], self.pos[1], self.des[0], self.des[1], \
								False, 0, sheet("resources/buildings/Food.png", [160, 160]), \
								"Mill.", 2.1))
		elif self.type == 1.1: # town hall
			if eventKey == "Spawn Worker":
				self.spawn(world, eventKey, [10, 0, 0, 1, 1*60], 
						   tdent(self.pos[0], self.pos[1], self.des[0], self.des[1], \
								False, 1.0, sheet("resources/player/worker.png", [40, 40]), \
								"Worker.", 0), [["Spawn Barracks", [125, 670]], ["Spawn Mill", [235, 670]]])
			elif eventKey == "Increase Pop":
				self.addResource(world, [0, 0,0, 10], [0,0,20,0])
				self.addResource(world, [0, 0,0, 10], [0,0,20,0])
		elif self.type == 1.2: # barracks
			if eventKey == "Spawn Knight":
				self.spawn(world, eventKey, [10, 10, 0, 1, 1*60], 
						   tdent(self.pos[0], self.pos[1], self.des[0], self.des[1], \
								 False, 1.0, sheet("resources/player/Knight.png", [40, 40]), \
								"Knight. Move to gate to transfer to battle.", 3.11))
			elif eventKey == "Spawn Crossbowman":
				self.spawn(world, eventKey, [10, 10, 0, 1, 1*60], 
						   tdent(self.pos[0], self.pos[1], self.des[0], self.des[1], \
								 False, 1.0, sheet("resources/player/Crossbowman.png", [40, 40]), \
								"Crossbowman. Move to gate to transfer to battle.", 3.12))
			elif eventKey == "Spawn Battleaxer":
				self.spawn(world, eventKey, [10, 10, 0, 1, 1*60], 
						   tdent(self.pos[0], self.pos[1], self.des[0], self.des[1], \
								 False, 1.0, sheet("resources/player/Battleaxer.png", [40, 40]), \
								"Crossbowman. Move to gate to transfer to battle.", 3.13))
		elif int(self.type) == 2:
			if eventKey == "":
				if self.type == 2.1:  # 2.1 is food
					self.addResource(world, [1/60.0, 0,0,0], [0,0,0,0])
				elif self.type == 2.2: # 2.2 is wood
					self.addResource(world, [0, 1/60.0,0,0], [0,0,0,0])
				elif self.type == 2.3: # 2.3 is gold
					self.addResource(world, [0, 0,1/60.0,0], [0,0,0,0])
		elif int(self.type) == 3:
			if eventKey == "":
				self.transfer(world)
		if self.timer == -1 and len(self.command) > 0:
			self.timer = self.command[0][1]
		if self.timer == 0:
			self.command.pop(0)
			if len(self.command) > 0:
				self.timer = self.command[0][1]
		
	def addCommand(self, command):
		self.newCommands.append(command)
		
	def checkCost(self, costList, world): # 0 = food, 1 = wood, 2 = gold, 3 = pop 
		if world.food >= costList[0] and world.wood >= costList[1] and world.gold >= costList[2] and world.pop + costList[3] <= world.poplimit:
			world.food -= costList[0]
			world.wood -= costList[1]
			world.gold -= costList[2]
			world.pop += costList[3]
			return True
		else:
			return False # play sound:"you require more resources" 
		
	def checkSize(self, tdent, world): 
		for ent in world.entities:
			if ent.rectangularCollision(tdent.pos, [tdent.pos[0] + tdent.sheet.dim[0], tdent.pos[1] + tdent.sheet.dim[1]]):
				if ent != self:
					return False 
		return True 
		
	def rectangularCollision(self, topLeft, bottomRight):
		if (topLeft[0] > self.pos[0] + self.sheet.dim[0] or bottomRight[0] < self.pos[0]) or \
			(topLeft[1] > self.pos[1] + self.sheet.dim[1] or bottomRight[1] < self.pos[1]):
			return False 
		else:
			return True
			
	def addResource(self, world, resourceList, costList):
		if self.checkCost(costList, world):
			world.food += resourceList[0]
			world.wood += resourceList[1]
			world.gold += resourceList[2]
			world.poplimit += resourceList[3]
		
	def transfer(self, world):
		if world.unitDictionary[self.type] in world.game.availableUnits:
			world.game.availableUnits[world.unitDictionary[self.type]] += 1
		else:
			world.game.availableUnits[world.unitDictionary[self.type]] = 1
		world.pop -= 1
		world.entities.remove(self)
		
	### def build(self, world): ###
		### world.building = True ###
		
	def spawn(self, world, eventKey, costList, tdent, buttonSpecs=[]):
		font_size = 12 # default font size
		default_font = "resources/fonts/Deutsch.ttf" # default button font
		images=[pygame.image.load("resources/buttons/smallidle.png").convert_alpha(), pygame.image.load("resources/buttons/smallhover.png").convert_alpha(), pygame.image.load("resources/buttons/smallclick.png").convert_alpha()] #Please don't load this every spawn... we need to restructure this!
		#[generateBasicButton([75,25],[200,200,200]),generateBasicButton([75,25],[150,150,150]),generateBasicButton([75,25],[100,100,100])] # default 
		if self.timer != 0:
			if tdent.speed > 0 or self.checkSize(tdent, world):
				if self.checkCost(costList, world):
					self.command.append([eventKey, costList[4]]) # 4 = time
		elif self.timer == 0:
			if self.speed != 0:
				world.entities.insert(0, tdent)
				for buttonSpec in buttonSpecs:
					world.entities[0].buttons.append(button(buttonSpec[0], buttonSpec[1], world.entities[0].addCommand, images, default_font, buttonSpec[0], font_size))
			else:
				world.entities.append(tdent)
				for buttonSpec in buttonSpecs:
					world.entities[-1].buttons.append(button(buttonSpec[0], buttonSpec[1], world.entities[-1].addCommand, images, default_font, buttonSpec[0], font_size))