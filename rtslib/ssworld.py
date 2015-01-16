from rtslib.ssent import *
from rtslib.tdent import *
from rtslib.path import *
from rtslib.sheet import *
from rtslib.cfgloader import *

class ssworld():
	def __init__(self, folder="resources/testlevel"):
		self.tdentities = []
		self.ssentities = []
		self.cpos = 0
		self.location = folder
		self.cfg = loadCFG(self.location+"/config.cfg")
		self.background = pygame.image.load(self.location+"/bg.png").convert_alpha()
		self.width = self.background.get_width()
		self.path = path(self.cfg["pathpoints"])
		
	def update(self, events):
		for event in events:
			if event.type == pygame.MOUSEBUTTONDOWN:
				self.ssentities.append(ssent(0.0, sheet("resources/stickman.png", [32,32]), self.path))
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_RIGHT:
					self.cpos+=5
				if event.key == pygame.K_LEFT:
					self.cpos-=5
				if self.cpos<0:
					self.cpos=0
				if self.cpos+1280>self.width:
					self.cpos = self.width-1280
				
		for ent in self.ssentities:
			ent.update()
			if ent.remove:
				self.ssentities.remove(ent)
		
	def draw(self, surface):
		surface.blit(self.background, [-self.cpos,0])
		#self.path.debugDraw(surface, self.cpos)
		for ent in self.ssentities:
			ent.draw(surface, self.cpos)