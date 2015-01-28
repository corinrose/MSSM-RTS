from rtslib.ssent import *
from rtslib.tdent import *
from rtslib.path import *
from rtslib.sheet import *
from rtslib.loader import *
from rtslib.button import *

import random

class ssworld():
	def __init__(self, game, folder="resources/testlevel"):
		#UI Elements
		self.bottombar = pygame.image.load("resources/ui/GameBottomBar.png").convert_alpha()
		self.topbar = pygame.image.load("resources/ui/GameTopBar.png").convert_alpha()
		self.unitImages = [pygame.image.load("resources/Knight.png").convert_alpha(), pygame.image.load("resources/Crossbowman.png").convert_alpha(),
						   pygame.image.load("resources/BattleAxer.png").convert_alpha()]
		self.unitNumbers = ["knight", "crossbow", "battleaxe"]
		self.smallbuttonset = [pygame.image.load("resources/buttons/smallidle.png").convert_alpha(),
							pygame.image.load("resources/buttons/smallhover.png").convert_alpha(),
							pygame.image.load("resources/buttons/smallclick.png").convert_alpha()
							]
		self.buttons = [button("knight", [15,670], self.spawnButtonClick, self.smallbuttonset),
						button("crossbow", [125,670], self.spawnButtonClick, self.smallbuttonset),
						button("battleaxe", [235,670], self.spawnButtonClick, self.smallbuttonset),
						]
		self.numberfont = pygame.font.Font("resources/fonts/Deutsch.ttf", 36)
		#Basic Properties
		self.game = game
		self.tdentities = []
		self.ssentities = []
		self.projectiles = []
		self.cid = 0
		self.cpos = 0
		self.location = folder
		#Level-specific things
		self.cfg = loadCFG(self.location+"/config.cfg")
		self.background = pygame.image.load(self.location+"/bg.png").convert_alpha()
		self.width = self.background.get_width()
		self.path = path(self.cfg["pathpoints"])
		#Script related variables
		self.script = self.cfg["script"]
		self.units = self.cfg["units"]
		self.waves = self.cfg["waves"]
		self.currentop = -1
		self.scriptstarted = False
		self.scripttimer = 0
		self.currentwavespawned=0
		self.spawnqueue=[]
		
		#Test stuff
		self.attacks = loadAttacks("resources/attacks.cfg")
		self.unitDefs = loadUnits("resources/player/units.cfg")
		self.testattack = {"style":"melee", "power":0.05}
		self.testattack2 = {"style":"melee", "power":1}
		self.testattack3 = {"style":"ranged", "power":10, "range":300, "delay":5}
		
	def update(self, events):
		#Handle events
		for event in events:
			#if event.type == pygame.MOUSEBUTTONDOWN:
			#	if self.game.availableUnits["knight"]>0:
			#		self.ssentities.append(ssent(self.cid, 0.0, 0.035, 0.3, sheet("resources/Knight.png", [36,36]), self.path, True, 100, self.testattack2))
			#		self.cid += 1
			#		self.game.availableUnits["knight"]-=1
					
			if event.type == pygame.KEYDOWN:
				#Camera movement
				if event.key == pygame.K_RIGHT:
					self.cpos+=5
				if event.key == pygame.K_LEFT:
					self.cpos-=5
				#Prevent camera from leaving the field
				if self.cpos<0:
					self.cpos=0
				if self.cpos+1280>self.width:
					self.cpos = self.width-1280
				#Start script on pressing "s"
				if event.key == pygame.K_s:
					if not self.scriptstarted:
						self.scriptstarted = True
						self.nextOperation()
		#Update Buttons
		for button in self.buttons:
			button.update(events)
		#Update entities
		for ent in self.ssentities:
			ent.update(self, self.ssentities)
		for pro in self.projectiles:
			pro.update(self.ssentities)
		#Remove any marked for deletion
		for ent in self.ssentities:
			if ent.remove:
				self.ssentities.remove(ent)
		for pro in self.projectiles:
			if pro.remove:
				self.projectiles.remove(pro)
				
		#Handle current operation
		if self.scriptstarted:
			if self.script[self.currentop]["command"] == "spawn" or self.script[self.currentop]["command"] == "spawnwave": #Spawning enemies, or waiting between spawns in a "wave"
				if self.currentwavespawned < len(self.spawnqueue):
					if self.scripttimer == 0:
						self.ssentities.append(ssent(self.cid, self.path.length-1, -float(self.units[self.spawnqueue[self.currentwavespawned]]["properties"][1]), 20, sheet("resources/badstick.png", [32,32]), self.path, False, float(self.units[self.spawnqueue[self.currentwavespawned]]["properties"][0]), self.testattack))
						self.cid += 1
						self.currentwavespawned += 1
						if self.script[self.currentop]["command"] == "spawn":
							self.scripttimer = self.script[self.currentop]["delay"]*60
						else:
							self.scripttimer = self.waves[self.script[self.currentop]["id"]]["delay"]*60
					else:
						self.scripttimer -= 1
				else:
					self.nextOperation();
			if self.script[self.currentop]["command"] == "delay": #Waiting until a further command
				self.scripttimer -= 1
				if self.scripttimer == 0:
					self.nextOperation();
				
	def nextOperation(self):
		self.currentop += 1
		if self.script[self.currentop]["command"] == "repeat":
			self.currentop = 0
			
		if self.script[self.currentop]["command"] == "delay":
			if self.script[self.currentop]["time"][0] == "r":
				sep = self.script[self.currentop]["time"][1:].split(":")
				self.scripttimer = random.randint(int(sep[0]),int(sep[1]))*60
			else:
				self.scripttimer = int(self.script[self.currentop]["time"])*60
				
		if self.script[self.currentop]["command"] == "spawn":	
			self.currentwavespawned = 0
			self.scripttimer = 0
			self.spawnqueue = [self.script[self.currentop]["id"]]*self.script[self.currentop]["quantity"]
			
		if self.script[self.currentop]["command"] == "spawnwave":
			self.currentwavespawned = 0
			self.scripttimer = 0
			self.spawnqueue = self.waves[self.script[self.currentop]["id"]]["pattern"]
	
	def draw(self, surface):
		surface.blit(self.background, [-self.cpos,0])
		#self.path.debugDraw(surface, self.cpos)
		for ent in self.ssentities:
			ent.draw(surface, self.cpos)
		for pro in self.projectiles:
			pro.draw(surface, self.cpos)
		surface.blit(self.bottombar, [0,650])
		surface.blit(self.topbar, [0,0])
		for button in self.buttons:
			button.draw(surface)
		for unitID in range(0, len(self.game.availableUnits)):
			surface.blit(self.unitImages[unitID], [15+(unitID*110), 675])
			surface.blit(self.numberfont.render(str(self.game.availableUnits[self.unitNumbers[unitID]]), True, [255,255,255]), [60+(unitID*110), 680])
			
	def spawnButtonClick(self, button):
		if self.game.availableUnits[button]>0:
			self.ssentities.append(ssent(self.cid, 0.0, self.unitDefs[button]["speed"], self.unitDefs[button]["width"], sheet(self.unitDefs[button]["image"], [40,40]), self.path, True, self.unitDefs[button]["health"], self.attacks[self.unitDefs[button]["attack"]]))
			self.cid += 1
			self.game.availableUnits[button]-=1