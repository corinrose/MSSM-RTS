import pygame

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