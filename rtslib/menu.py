import pygame, sys
import rtslib

class menu():
	def __init__(self):
		self.state = "main"
		
	def draw(self, surface):
		surface.fill([255,0,0])
		
	def update(self, events):
		out = {}
		for event in events:
			if event.type == pygame.MOUSEBUTTONDOWN:
				print "MENU CLUNK"
			if event.type == pygame.KEYUP:
				print event.key
				if event.key == pygame.K_RETURN:
					out["state"] = "game"
		
		out["title"] = "MSSM RTS Menu"
		return out