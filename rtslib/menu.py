import pygame, sys
import rtslib

class menu():
	def __init__(self):
		self.state = "main"
		self.mainbuttons = [rtslib.button("play", [50,50], self.clickHandler),
							rtslib.button("exit", [50,250], self.clickHandler)]
		
	def draw(self, surface):
		surface.fill([255,0,0])
		for b in self.mainbuttons:
			b.draw(surface)
		
	def clickHandler(self, button):
		if self.state == "main":
			if button == "play":
				self.state = "level"
			if button == "exit":
				self.state="exit"
		
	def update(self, events):
		out = {}
		for b in self.mainbuttons:
			b.update(events)
		if self.state == "level":
			out["state"] = "game"
		if self.state == "exit":
			out["exit"]="now"
		out["title"] = "MSSM RTS Menu"
		return out