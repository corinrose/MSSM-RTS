class tdent():
	def __init__(self, posX, posY, desX, desY, speed, sheet):
		self.pos = [posX, posX]
		self.des = [desX, desY]
		self.speed = speed
		self.sheet = sheet
		
    def draw(surface):
	    surface.blit(self.sheet.getImage())
	
	def update(events):
	    if (self.posX != self.desX)
	        if (self.posX < self.desX < self.posX + self.speed or self.posX + self.speed < self.desX < self.posX):
		        self.posX = self.desX
	        else:
			    self.posX += self.speed
			    
		elif (self.posY != self.desX)
		    if (self.posY < self.desY < self.posY + self.speed or self.posY + self.speed < self.desY < self.posY):
		        self.posY = self.desY 
	        else:
			    self.posY += self.speed 
		