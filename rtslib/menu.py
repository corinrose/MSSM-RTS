import pygame, sys
import rtslib

class menu():
	def __init__(self):
		self.state = "main"
		self.testbutton = rtslib.button([50,50], self.playTestLevel)
		
	def draw(self, surface):
		surface.fill([255,0,0])
		self.testbutton.draw(surface)
		
	def playTestLevel(self):
		self.state = "level"
		
	def update(self, events):
		out = {}
		self.testbutton.update(events)
		if self.state == "level":
			out["state"] = "game"
		out["title"] = "MSSM RTS Menu"
		return out