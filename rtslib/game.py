import rtslib, pygame

class game():
	def __init__(self):
		self.ssworld = rtslib.ssworld("resources/smalllevel")
		self.tdworld = rtslib.tdworld()
		self.worldFocus = 1
		self.availableUnits={"knight":0}
		
	def draw(self, surface):
		# surface.fill([0,255,0]) 
		if self.worldFocus == 0:
			self.tdworld.draw(surface)
		if self.worldFocus == 1:
			self.ssworld.draw(surface)
		
	def update(self, events):
		out = {}
		for event in events:
			if event.type == pygame.KEYUP:
				if event.key == pygame.K_SPACE:
					self.worldFocus = not self.worldFocus
					
		if self.worldFocus == 1:
			self.ssworld.update(self, events)
			self.tdworld.update(self, [])
		else:
			self.ssworld.update(self, [])
			self.tdworld.update(self, events)
			
		out["title"] = "Save Our City - "+("Battle View"*self.worldFocus)+("Resource View"*(not self.worldFocus))
		return out