from rtslib.ssent import *
from rtslib.tdent import *
from rtslib.path import *
from rtslib.sheet import *

class ssworld():
	def __init__(self):
		self.tdentities = []
		self.testpath = path([[30,30],[100,50],[200,150],[250,100],[375, 125]])
		self.ssentities = []
		self.cpos = 0
		
	def update(self, events):
		for event in events:
			if event.type == pygame.MOUSEBUTTONDOWN:
				self.ssentities.append(ssent(0.0, sheet("resources/stickman.png", [32,32]), self.testpath))
				
		for ent in self.ssentities:
			ent.update()
			if ent.remove:
				self.ssentities.remove(ent)
		
	def draw(self, surface):
		self.testpath.debugDraw(surface, cpos)
		for ent in self.ssentities:
			ent.draw(surface, cpos)