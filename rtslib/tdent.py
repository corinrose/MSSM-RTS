import pygame, math
from rtslib.sheet import *

class tdent():
	def __init__(self, posX, posY, desX, desY, isSelected, speed, sheet, UIdesc, type):
		self.pos = [posX, posY]
		self.des = [desX, desY]
		self.isSelected = isSelected 
		self.speed = speed
		self.sheet = sheet
		self.sheetCounter = 0
		self.isMoving = False
		self.type = type # 0 = worker, 1 = buildings, 2.1-2.3= resource, 3.1 = knight
		self.timer = -1 # positive means working, 0 is currently doing a task, -1 is finished
		self.command = []
		self.UIsprite = [pygame.font.SysFont("monospace", 14).render(UIdesc, 1, (255, 255, 0)), (15, 720 - 144 + 15)] # 144 is height, 15 is buffer zone
		
	def draw(self, surface):
		surface.blit(self.sheet.getImage(), self.pos)
		if self.isMoving:
			self.sheetCounter+=1
			if self.sheetCounter == 10: # 10 frames a sheet 
				self.sheet.nextImage()
				self.sheetCounter = 0
		if self.des[0] < self.pos[0] and self.speed > 0: 
			self.sheet.setFlipped(True)
		else:
			self.sheet.setFlipped(False)
		if self.isSelected:
			self.drawSelectionMarker(surface)
			self.drawDestinationMarker(surface)
		self.drawWorkingMarker(surface)
		
	def drawUIText(self, surface):
		surface.blit(self.UIsprite[0], self.UIsprite[1]) # display unit-specific UI text
	
	def update(self, world):
		if self.timer < 0:
			self.move()
		else:
			if self.timer == 0:
				self.action(world, self.command[0][0])
			self.timer -= 1
		if int(self.type) == 3: # attacking units
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
			self.sheetCounter = 0
			
	def drawSelectionMarker(self, surface): # RED
		pygame.draw.polygon(surface, (255, 0, 0), [self.pos, \
									  [self.pos[0] + self.sheet.dim[0], self.pos[1]], \
									  [self.pos[0] + self.sheet.dim[0], self.pos[1] + self.sheet.dim[1]], \
									  [self.pos[0], self.pos[1] + self.sheet.dim[1]]], \
									  2)
									  
	def drawWorkingMarker(self, surface): # YELLOW
		if len(self.command) > 0 and self.timer >= 0:
			pygame.draw.polygon(surface, (255, 255, 0), [[self.pos[0], self.pos[1] + 6], \
						 				  [self.pos[0] + ((float(self.command[0][1]) - float(self.timer))/float(self.command[0][1]))*self.sheet.dim[0], self.pos[1] + 6]], \
										  3)
								
	def drawDestinationMarker(self, surface): # RED
		pygame.draw.circle(surface, (255, 0, 0), self.des, 6, 2)
				
############################################################################ 

	def action(self, world, eventKey):
		if self.type == 0: # worker
			if eventKey == pygame.K_w:
				self.spawn(world, eventKey, [0, 20, 0, 1, 3*60], 
						   tdent(self.pos[0], self.pos[1], self.des[0], self.des[1], \
								False, 0, sheet("resources/Barracks.png", [160, 160]), \
								"Barracks. Press w to train soldier : 10 food, 10 wood, 1 pop.", 1.2))
			elif eventKey == pygame.K_e:
				self.spawn(world, eventKey, [0, 20, 0, 0, 3*60], 
						   tdent(self.pos[0], self.pos[1], self.des[0], self.des[1], \
								False, 0, sheet("resources/Food.png", [160, 160]), \
								"Mill. For food.", 2.1))
		elif self.type == 1.1: # town hall
			if eventKey == pygame.K_w: 
				self.spawn(world, eventKey, [10, 0, 0, 1, 1*60], 
						   tdent(self.pos[0], self.pos[1], self.des[0], self.des[1], \
								False, 1.0, sheet("resources/worker.png", [40, 40]), \
								"Worker. Press w to build barracks : 20 wood. Press e to build mill.", 0))
		elif self.type == 1.2: # barracks
			if eventKey == pygame.K_w:
				self.spawn(world, eventKey, [10, 10, 0, 1, 1*60], 
						   tdent(self.pos[0], self.pos[1], self.des[0], self.des[1], \
								 False, 1.0, sheet("resources/Knight.png", [36, 36]), \
								"Knight. Move to gate to transfer to battle.", 3.1))
		elif int(self.type) == 2:
			if eventKey == "":
				if self.type == 2.1:  # 2.1 is food
					self.addFood(world)
				elif self.type == 2.2: # 2.2 is food
					self.addWood(world)
				elif self.type == 2.3: # 2.3 is food
					self.addGold(world)
		elif int(self.type) == 3:
			if eventKey == "":
				self.transfer(world)
		if self.timer == -1 and len(self.command) > 0:
			self.timer = self.command[0][1]
		if self.timer == 0:
			self.command.pop(0)
			if len(self.command) > 0:
				self.timer = self.command[0][1]
		
	def checkCost(self, costList, world): # 0 = food, 1 = wood, 2 = gold, 3 = pop 
		if world.food >= costList[0] and world.wood >= costList[1] and world.gold >= costList[2] and world.pop + costList[3] <= world.poplimit:
			world.food -= costList[0]
			world.wood -= costList[1]
			world.gold -= costList[2]
			world.pop += costList[3]
			return True
		else:
			return False
			
	def addFood(self, world):
		world.food += 1/60.0
	def addWood(self, world):
		world.wood += 1/60.0
	def addGold(self, world):
		world.gold += 1/60.0
		
	def transfer(self, world):
		if world.unitDictionary[self.type] in world.game.availableUnits:
			world.game.availableUnits[world.unitDictionary[self.type]] += 1
		else:
			world.game.availableUnits[world.unitDictionary[self.type]] = 1
		world.entities.remove(self)
		
	def spawn(self, world, eventKey, costList, tdent):
		if self.timer != 0:
			if self.checkCost(costList, world):
				self.command.append([eventKey, costList[4]]) # 4 = time
		elif self.timer == 0:
			if self.speed != 0:
				world.entities.insert(0, tdent)
			else:
				world.entities.append(tdent)