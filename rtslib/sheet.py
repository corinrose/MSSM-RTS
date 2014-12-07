import pygame, os

class SpritesheetSizeError(Exception):
    """Exception raised when a spritesheet's dimensions are not divisible by the dimensions of an individual image"""
    pass

class sheet():
	def __init__(self, image, dimensions):
		self.filename = image
		self.image = pygame.image.load(image)
		self.dim = dimensions
		if int(float(self.image.get_width())/self.dim[0])!=(float(self.image.get_width())/self.dim[0]) or int(float(self.image.get_height())/self.dim[1])!=(float(self.image.get_height())/self.dim[1]):
			raise SpritesheetSizeError("Frame size does not divide into sheet size")
		self.frames = []
		for y in range(0, self.image.get_height()/self.dim[1]):
			for x in range(0, self.image.get_width()/self.dim[0]):
				self.frames.append(self.image.subsurface([x*self.dim[0], y*self.dim[1], self.dim[0], self.dim[1]]))
		self.frame = 0
		self.flipped = False
		self.flippedframes = []
		for frame in self.frames:
			self.flippedframes.append(pygame.transform.flip(frame, True, False))
				
	def getImage(self):
		if self.flipped:
			return self.flippedframes[self.frame]
		else:
			return self.frames[self.frame]
	
	def nextImage(self):
		self.frame += 1
		if self.frame == len(self.frames):
			self.frame = 0
			
	def setFlipped(self, flip):
		self.flipped = flip