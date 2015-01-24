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
		self.type = type # 0 = worker, 1 = town hall, 2.1-2.3= resource, 3 = barracks, 4.1 = knight
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
		if self.des[0] < self.pos[0] and self.type in [0, 4.1]: # list of all moving units
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
		if self.type == 0: 
			if eventKey == pygame.K_w:
				self.spawnBarracks(world, eventKey)
			elif eventKey == pygame.K_e:
				self.spawnMill(world, eventKey)
		elif self.type == 1:
			if eventKey == pygame.K_w: 
				self.spawnWorker(world, eventKey)
		elif round(self.type) == 2:
			if eventKey == "":
				if self.type == 2.1:  # 2.1 is food
					self.addFood(world)
				elif self.type == 2.2: # 2.2 is food
					self.addWood(world)
				elif self.type == 2.3: # 2.3 is food
					self.addGold(world)
		elif self.type == 3:
			if eventKey == pygame.K_w:
				self.spawnSoldier(world, eventKey)
			elif eventKey == pygame.K_e:
				self.upgradeWorker(world, eventKey)
		if self.timer == -1 and len(self.command) > 0:
			self.timer = self.command[0][1]
		if self.timer == 0:
			self.command.pop(0)
			if len(self.command) > 0:
				self.timer = self.command[0][1]
		
	def addFood(self, world):
		world.food += 1/60.0
	def addWood(self, world):
		world.wood += 1/60.0
	def addGold(self, world):
		world.gold += 1/60.0
		
	def spawnWorker(self, world, eventKey):
		pop = 1
		food = 10
		wood = 0
		gold = 0
		time = 1*60
		if self.timer != 0:
			if world.pop + pop <= world.poplimit and world.food >= food and world.wood >= wood and world.gold >= gold:
				world.pop += pop
				world.food -= food
				world.wood -= wood
				world.gold -= gold
				self.command.append([eventKey, time])
		elif self.timer == 0:
			world.entities.append(tdent(self.pos[0], self.pos[1], self.des[0], self.des[1], \
								False, 1.0, sheet("resources/worker.png", [40, 40]), \
								"Worker. Press w to build barracks : 20 wood. Press e to build mill.", 0)) 
			
	
	def spawnMill(self, world, eventKey):
		pop = 0
		food = 0
		wood = 20
		gold = 0
		time = 3*60
		if self.timer != 0:
			if world.pop + pop <= world.poplimit and world.food >= food and world.wood >= wood and world.gold >= gold:
				world.pop += pop
				world.food -= food
				world.wood -= wood
				world.gold -= gold
				self.command.append([eventKey, time])
		elif self.timer == 0:
			world.entities.insert(0, tdent(self.pos[0], self.pos[1], self.des[0], self.des[1], \
								False, 0, sheet("resources/Food.png", [160, 160]), \
								"Mill. For food.", 2.1))
		
	def spawnBarracks(self, world, eventKey):
		pop = 0
		food = 0
		wood = 20
		gold = 0
		time = 3*60
		if self.timer != 0:
			if world.pop + pop <= world.poplimit and world.food >= food and world.wood >= wood and world.gold >= gold:
				world.pop += pop
				world.food -= food
				world.wood -= wood
				world.gold -= gold
				self.command.append([eventKey, time])
		elif self.timer == 0:
			world.entities.insert(0, tdent(self.pos[0], self.pos[1], self.des[0], self.des[1], \
								False, 0, sheet("resources/Barracks.png", [160, 160]), \
								"Barracks. Press w to train soldier : 10 food, 10 wood, 1 pop.", 3))
	
	def spawnSoldier(self, world, eventKey):
		pop = 1
		food = 10
		wood = 10
		gold = 0
		time = 1*60
		if self.timer != 0:
			if world.pop + pop <= world.poplimit and world.food >= food and world.wood >= wood and world.gold >= gold:
				world.pop += pop
				world.food -= food
				world.wood -= wood
				world.gold -= gold
				self.command.append([eventKey, time])
		elif self.timer == 0:
			world.entities.append(tdent(self.pos[0], self.pos[1], self.des[0], self.des[1], \
								 False, 1.0, sheet("resources/Knight.png", [36, 36]), \
								"Knight. Move to gate to transfer to battle.", 4.1))
	
	def upgradeWorker(self, world, eventKey):
		pass 
		# resources -= 100
		# upgrade worker