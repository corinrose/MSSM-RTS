import rtslib, pygame

class game():
	def __init__(self):
		self.state = "main"
		self.ssworld = rtslib.ssworld()
		self.tdworld = rtslib.tdworld()
		
	def draw(self, surface):
		surface.fill([0,255,0])
		
	def update(self, events):
		out = {}
		for event in events:
			if event.type == pygame.MOUSEBUTTONDOWN:
				print "GAME CLUNK"
				
		return out