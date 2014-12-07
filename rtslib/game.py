import rtslib, pygame

class game():
	def __init__(self):
		self.ssworld = rtslib.ssworld()
		self.tdworld = rtslib.tdworld()
		self.worldFocus = 1
		
	def draw(self, surface):
		surface.fill([0,255,0])
		if self.worldFocus == 0:
			self.tdworld.draw(surface)
		if self.worldFocus == 1:
			self.ssworld.draw(surface)
		
	def update(self, events):
		out = {}
		for event in events:
			if event.type == pygame.KEYDOWN:
				self.worldFocus = not self.worldFocus
			if event.type == pygame.MOUSEBUTTONDOWN:
				if self.worldFocus == 1:
					self.ssworld.spawn()
		
		self.tdworld.update()
		self.ssworld.update()
		out["title"] = "MSSM RTS - Battle View: "+str(self.worldFocus) 
		return out