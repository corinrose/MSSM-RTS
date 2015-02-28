import rtslib, pygame

class game():
	def __init__(self, level):
		self.ssworld = rtslib.ssworld(self, level)
		self.tdworld = rtslib.tdworld(self, level)
		self.worldFocus = 1
		self.availableUnits={"knight":5, "crossbow":5, "battleaxe":5}
		#Common UI Stuff
		self.buttons = [rtslib.button("switch", [1000,670], self.clickHandler, rtslib.common.buttonSets["hud"], "resources/fonts/Deutsch.ttf", "Swap"),
						rtslib.button("menu", [1125,670], self.clickHandler, rtslib.common.buttonSets["hud"], "resources/fonts/Deutsch.ttf", "Menu")]
		#Pause menu things
		self.paused = False
		self.pauseback = pygame.surface.Surface([1280,720]).convert_alpha() #this is temporary
		self.pauseback.fill([100, 100, 100, 100])
		self.pauseButtons = [rtslib.button("menu", [480,200], self.clickHandler, rtslib.common.buttonSets["large"], "resources/fonts/Deutsch.ttf", "Main Menu"),
							 rtslib.button("back", [480,350], self.clickHandler, rtslib.common.buttonSets["large"], "resources/fonts/Deutsch.ttf", "Back")]
		#Endgame things
		self.gameOver = False
		self.gameOverBack = pygame.surface.Surface([1280, 720]).convert_alpha()
		self.gameOverBack.fill([100, 100, 100, 0])
		self.gameOverFade = 0
		self.gameOverButtons = [rtslib.button("menu", [650,300], self.clickHandler, rtslib.common.buttonSets["large"], "resources/fonts/Deutsch.ttf", "Menu")]
		self.goBack = False #TODO: This is bad
		self.won = False
		self.gameWonButtons = [rtslib.button("menu", [650,300], self.clickHandler, rtslib.common.buttonSets["large"], "resources/fonts/Deutsch.ttf", "Menu")]
		
	def draw(self, surface):
		# surface.fill([0,255,0]) 
		if self.worldFocus == 0:
			self.tdworld.draw(surface)
		if self.worldFocus == 1:
			self.ssworld.draw(surface)
		for button in self.buttons:
			button.draw(surface)
		#Game over screen
		if self.gameOver:
			self.gameOverBack.fill([100,100,100,self.gameOverFade])
			surface.blit(self.gameOverBack, [0,0])	
			for button in self.gameOverButtons:
				button.draw(surface)
		#Game won screen
		if self.won:
			self.gameOverBack.fill([100,100,100,self.gameOverFade])
			surface.blit(self.gameOverBack, [0,0])	
			for button in self.gameOverButtons:
				button.draw(surface)
		#Pause menu
		if self.paused:
			surface.blit(self.pauseback, [0,0])
			for button in self.pauseButtons:
				button.draw(surface)
		
	def update(self, events):
		out = {}
		if not self.paused:
			for event in events:
				if event.type == pygame.KEYUP:
					if event.key == pygame.K_SPACE:
						self.worldFocus = not self.worldFocus
			
			for button in self.buttons:
				button.update(events)
				
			if self.gameOver:
				self.worldFocus = 1
				if self.gameOverFade<100:
					self.gameOverFade+=2
				for button in self.gameOverButtons:
					button.update(events)
			if self.won:
				self.worldFocus = 1
				if self.gameOverFade<100:
					self.gameOverFade+=2
				for button in self.gameWonButtons:
					button.update(events)
					
			if self.worldFocus == 1:
				self.ssworld.update(events)
				self.tdworld.update([])
			else:
				self.ssworld.update([])
				self.tdworld.update(events)
		else:
			for button in self.pauseButtons:
				button.update(events)
		out["title"] = "Save Our City - "+("Battle View"*self.worldFocus)+("Resource View"*(not self.worldFocus))
		if self.goBack:
			out["state"] = "menu"
			if self.won:
				out["unlocks"] = self.ssworld.cfg["unlocks"] #TODO: NO. Just no.
		return out
		
	def clickHandler(self, button):
		if self.paused == False:
			if button == "menu":
				self.paused = True
			if button == "switch":
				self.worldFocus = not self.worldFocus
		else:
			if button == "menu":
				self.goBack = True
			if button == "back":
				self.paused = False