from rtslib.ssent import *
from rtslib.tdent import *
from rtslib.path import *
from rtslib.sheet import *
from rtslib.loader import *
from rtslib.button import *
from rtslib.base import *
import rtslib.common #TODO: pls don't
import rtslib #TODO: this too

import random

class ssworld():
	def __init__(self, game, folder="resources/testlevel"):
		#UI Elements
		self.bottombar = rtslib.common.images["resources/ui/GameBottomBar.png"]
		self.topbar = rtslib.common.images["resources/ui/GameTopBar.png"]
		self.unitImages = [rtslib.common.images["resources/player/Knight.png"], rtslib.common.images["resources/player/Crossbowman.png"],
						   rtslib.common.images["resources/player/BattleAxer.png"]]
		self.unitNumbers = ["knight", "crossbow", "battleaxe"]

		self.buttons = [button("knight", [15,670], self.spawnButtonClick, rtslib.common.buttonSets["hud"]),
						button("crossbow", [125,670], self.spawnButtonClick, rtslib.common.buttonSets["hud"]),
						button("battleaxe", [235,670], self.spawnButtonClick, rtslib.common.buttonSets["hud"]),
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
		self.cfg = loadCFG(self.location+"/config.cfg") #TODO Move cfg to game object, add tdworld stuff
		self.background = rtslib.common.images[self.location+"/bg.png"]
		self.foreground = rtslib.common.images[self.location+"/fg.png"]
		self.width = self.background.get_width()
		self.path = path(self.cfg["pathpoints"])

		#Script related variables
		self.script = self.cfg["script"]
		self.units = self.cfg["units"]
		self.waves = self.cfg["waves"]
		self.currentop = -1
		self.scriptStartTime = self.cfg["startdelay"]
		self.startIn = self.cfg["startdelay"]
		self.scriptstarted = False
		self.scripttimer = 0
		self.currentwavespawned=0
		self.spawnqueue=[]
		
		#Unit Definitions
		self.attacks = loadAttacks("resources/attacks.cfg")
		self.unitDefs = loadUnits("resources/player/units.cfg")
		self.unitDefs.update(loadUnits("resources/skeletons/units.cfg"))#Temporary solution, fix later on
		self.unitDefs.update(loadUnits("resources/zombies/units.cfg"))#Temporary solution, fix later on
		#Player unit spawning
		self.playerQueue = []
		self.playerUnits = self.cfg["playerunits"]
		
		#Test Stuff
		self.gates = self.cfg["gates"]
		for gate in self.gates:
			self.ssentities.append(ssent(self.cid, gate["distance"], 0, 
										self.unitDefs[gate["type"]]["width"], 
										sheet(self.unitDefs[gate["type"]]["image"], self.unitDefs[gate["type"]]["dimensions"]), 
										self.path, False, gate["health"],
										self.attacks[self.unitDefs[gate["type"]]["attack"]], self.unitDefs[gate["type"]]["frametime"], self.unitDefs[gate["type"]]["offset"], True)) #Hard-coded offset = bad!
			self.cid += 1
		self.startpos=0
		
		#Add the king
		self.king = self.cfg["king"]
		self.ssentities.append(ssent(self.cid, self.king["distance"], 0, 
										self.unitDefs[self.king["type"]]["width"], 
										sheet(self.unitDefs[self.king["type"]]["image"], self.unitDefs[self.king["type"]]["dimensions"]), 
										self.path, True, self.king["health"],
										self.attacks[self.unitDefs[self.king["type"]]["attack"]], self.unitDefs[self.king["type"]]["frametime"], self.unitDefs[self.king["type"]]["offset"], True))
		self.cid += 1
		self.king = self.ssentities[-1]
		
		#Add the boss
		self.boss = self.cfg["boss"]
		self.ssentities.append(ssent(self.cid, self.path.length-self.boss["distance"], 0, 
										self.unitDefs[self.boss["type"]]["width"], 
										sheet(self.unitDefs[self.boss["type"]]["image"], self.unitDefs[self.boss["type"]]["dimensions"]), 
										self.path, False, self.boss["health"],
										self.attacks[self.unitDefs[self.boss["type"]]["attack"]], self.unitDefs[self.boss["type"]]["frametime"], self.unitDefs[self.boss["type"]]["offset"], True))
		self.cid += 1
		self.boss = self.ssentities[-1]
		
	def clampCamera(self):
		if self.cpos<0:
			self.cpos=0
		if self.cpos+1280>self.width:
			self.cpos=self.width-1280
			
	def update(self, events):
		#Handle events
		for event in events:	
			if event.type == pygame.MOUSEBUTTONDOWN:
				self.startpos = event.pos[0]+self.cpos
			if event.type == pygame.KEYDOWN:
				#Camera movement
				if event.key == pygame.K_d:
					self.cpos+=5
				if event.key == pygame.K_a:
					self.cpos-=5
				#Start script on pressing "s"
				if event.key == pygame.K_s:
					if not self.scriptstarted:
						self.scriptstarted = True
						self.nextOperation()
		#Update Buttons
		for button in self.buttons:
			button.update(events)
		if pygame.mouse.get_pressed()[0]:
			self.cpos=self.startpos-pygame.mouse.get_pos()[0]
		self.clampCamera()#Prevents camera from leaving the field
		#Update entities
		for ent in self.ssentities:
			ent.update(self, self.ssentities)
		for pro in self.projectiles:
			pro.update(self.ssentities)
		#Check for a game over or win
		if self.king.remove:
			self.game.gameOver = True
		if self.boss.remove and not self.game.gameOver:
			self.game.won = True
			self.scriptstarted = False
		#Remove any marked for deletion
		for ent in self.ssentities:
			if ent.remove:
				self.ssentities.remove(ent)
		for pro in self.projectiles:
			if pro.remove:
				self.projectiles.remove(pro)		
		
		#Spawn a player unit if you can
		if len(self.playerQueue)>0:
			fir = self.playerQueue[0]
			firclass = self.playerUnits[fir]
			if self.checkClear([-3, self.unitDefs[firclass["type"]]["width"]+3], 1):
				self.playerQueue = self.playerQueue[1:]
				self.ssentities.append(ssent(self.cid, 0.0, firclass["speed"], 
										self.unitDefs[firclass["type"]]["width"], 
										sheet(self.unitDefs[firclass["type"]]["image"], self.unitDefs[firclass["type"]]["dimensions"]), 
										self.path, True, firclass["health"], 
										self.attacks[self.unitDefs[firclass["type"]]["attack"]],
										self.unitDefs[firclass["type"]]["frametime"], self.unitDefs[firclass["type"]]["offset"]))
				self.cid += 1
				
		#Handle current operation
		if self.scriptstarted:
			if self.script[self.currentop]["command"] == "spawn" or self.script[self.currentop]["command"] == "spawnwave": #Spawning enemies, or waiting between spawns in a "wave"
				if self.currentwavespawned < len(self.spawnqueue):
					if self.scripttimer == 0:
						if self.checkClear([self.path.length-self.unitDefs[self.units[self.spawnqueue[self.currentwavespawned]]["type"]]["width"]-3, self.path.length], 0):
							#print "Spawning: "+self.units[self.spawnqueue[self.currentwavespawned]]["type"]
							self.ssentities.append(ssent(self.cid, self.path.length-1, -float(self.units[self.spawnqueue[self.currentwavespawned]]["properties"][1]), 
													self.unitDefs[self.units[self.spawnqueue[self.currentwavespawned]]["type"]]["width"], 
													sheet(self.unitDefs[self.units[self.spawnqueue[self.currentwavespawned]]["type"]]["image"], self.unitDefs[self.units[self.spawnqueue[self.currentwavespawned]]["type"]]["dimensions"]), 
													self.path, False, float(self.units[self.spawnqueue[self.currentwavespawned]]["properties"][0]),
													self.attacks[self.unitDefs[self.units[self.spawnqueue[self.currentwavespawned]]["type"]]["attack"]], self.unitDefs[self.units[self.spawnqueue[self.currentwavespawned]]["type"]]["frametime"], 
													self.unitDefs[self.units[self.spawnqueue[self.currentwavespawned]]["type"]]["offset"]))
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
		#If the script hasn't been started, count down the timer
		else:
			if self.startIn > 0:
				self.startIn-=1
			else:
				self.scriptstarted = True
				self.nextOperation()
	
	def checkClear(self, distRange, team): #team: 0=bad 1=good 2=either
		for unit in self.ssentities:
			if checkWithin(unit.dist, distRange) or checkWithin(unit.dist-unit.width, distRange) or checkWithin(unit.dist+unit.width, distRange):
				if unit.team == team or team == 2:
					return False
		return True
	
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
		surface.fill([200,200,200])
		surface.blit(self.background, [-self.cpos,0])
		#self.path.debugDraw(surface, self.cpos)
		for ent in self.ssentities:
			ent.draw(surface, self.cpos)
		for pro in self.projectiles:
			pro.draw(surface, self.cpos)
		surface.blit(self.foreground, [-self.cpos,0])
		#Bottom bar UI elements
		surface.blit(self.bottombar, [0,650])
		for button in self.buttons:
			button.draw(surface)
		for unitID in range(0, len(self.game.availableUnits)):
			surface.blit(self.unitImages[unitID], [15+(unitID*110), 675])
			surface.blit(self.numberfont.render(str(self.game.availableUnits[self.unitNumbers[unitID]]), True, [255,255,255]), [60+(unitID*110), 680])
		#Top bar UI stuff
		surface.blit(self.topbar, [0,0])
		if not self.scriptstarted:
			pygame.draw.rect(surface, [255,0,0], [440, 7, 400, 25], 0)
			pygame.draw.rect(surface, [255,255,0], [440, 7, 400*(float(self.startIn)/self.scriptStartTime), 25], 0)
			
	def spawnButtonClick(self, button):
		if self.game.availableUnits[button]>0 and self.scriptstarted:
			self.playerQueue.append(button)
			self.game.availableUnits[button]-=1