from rtslib.ssent import *
from rtslib.tdent import *
from rtslib.path import *
from rtslib.sheet import *

class ssworld():
	def __init__(self):
		self.tdentities = []
		self.testpath = path([[30,30],[100,50],[200,150],[250,100],[375, 125]])
		self.ssentities = []
		
	def update(self):
		for ent in self.ssentities:
			ent.update()
			if ent.remove:
				self.ssentities.remove(ent)
			
	def spawn(self):
		self.ssentities.append(ssent(0.0, sheet("resources/stickman.png", [32,32]), self.testpath))
		
	def draw(self, surface):
		self.testpath.debugDraw(surface)
		for ent in self.ssentities:
			ent.draw(surface)