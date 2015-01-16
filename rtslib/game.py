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
			if event.type == pygame.KEYUP:
				if event.key == pygame.K_SPACE:
					self.worldFocus = not self.worldFocus
					
		if self.worldFocus == 1:
			self.ssworld.update(events)
			self.tdworld.update([])
		else:
			self.ssworld.update([])
			self.tdworld.update(events)
			
		out["title"] = "MSSM RTS - "+("Battle View"*self.worldFocus)+("Resource View"*(not self.worldFocus))
		return out