from rtslib.ssent import *
from rtslib.tdent import *
from rtslib.path import *
from rtslib.sheet import *

class ssworld():
	def __init__(self):
		self.tdentities = []
		self.testpath = path([[-50,53],[0,53],[492,165],[690,510],[1005, 585],[1376,348],[1869,260],[2050,260]])
		self.ssentities = []
		self.cpos = 0
		self.testbg = pygame.image.load("resources/testpath.png").convert_alpha()
		
	def update(self, events):
		for event in events:
			if event.type == pygame.MOUSEBUTTONDOWN:
				self.ssentities.append(ssent(0.0, sheet("resources/stickman.png", [32,32]), self.testpath))
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_RIGHT:
					self.cpos+=5
				if event.key == pygame.K_LEFT:
					if self.cpos>0:
						self.cpos-=5
				
		for ent in self.ssentities:
			ent.update()
			if ent.remove:
				self.ssentities.remove(ent)
		
	def draw(self, surface):
		surface.blit(self.testbg, [-self.cpos,0])
		#self.testpath.debugDraw(surface, self.cpos)
		for ent in self.ssentities:
			ent.draw(surface, self.cpos)