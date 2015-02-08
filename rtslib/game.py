import rtslib, pygame

class game():
	def __init__(self, level):
		self.ssworld = rtslib.ssworld(self, level)
		self.tdworld = rtslib.tdworld(self)
		self.worldFocus = 1
		self.availableUnits={"knight":5, "crossbow":5, "battleaxe":5}
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
		
	def update(self, events):
		out = {}
		for event in events:
			if event.type == pygame.KEYUP:
				if event.key == pygame.K_SPACE:
					self.worldFocus = not self.worldFocus
					
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
		out["title"] = "Save Our City - "+("Battle View"*self.worldFocus)+("Resource View"*(not self.worldFocus))
		if self.goBack:
			out["state"] = "menu"
			if self.gameOver or self.won:
				out["newgame"] = "resources/skele01"
		return out
		
	def clickHandler(self, button):
		if button == "menu":
			self.goBack = True