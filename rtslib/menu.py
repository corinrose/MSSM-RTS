import pygame, sys
import rtslib

class menu():
	def __init__(self):
		self.state = "main"
		self.menubuttonset=[pygame.image.load("resources/buttons/largeidle.png").convert_alpha(),
							pygame.image.load("resources/buttons/largehover.png").convert_alpha(),
							pygame.image.load("resources/buttons/largeclick.png").convert_alpha()
							]
		self.mainbg = pygame.image.load("resources/menubg/main.png").convert_alpha()
		self.fileselectbg = pygame.image.load("resources/menubg/fileselect.png").convert_alpha()
		self.settingsbg = pygame.image.load("resources/menubg/settings.png").convert_alpha()
		self.creditsbg = pygame.image.load("resources/menubg/credits.png").convert_alpha()
		
		self.mainbuttons = [rtslib.button("play", [100,325], self.clickHandler, self.menubuttonset, "resources/fonts/Deutsch.ttf", "Play"),
							rtslib.button("settings", [100,405], self.clickHandler, self.menubuttonset, "resources/fonts/Deutsch.ttf", "Settings"),
							rtslib.button("credits", [100,485], self.clickHandler, self.menubuttonset, "resources/fonts/Deutsch.ttf", "Credits"),
							rtslib.button("exit", [100,565], self.clickHandler, self.menubuttonset, "resources/fonts/Deutsch.ttf", "Exit")]
							
		self.fileselectbuttons = [rtslib.button("file1", [60,250], self.clickHandler, self.menubuttonset, "resources/fonts/Deutsch.ttf", "File 1"),
								  rtslib.button("file2", [480,250], self.clickHandler, self.menubuttonset, "resources/fonts/Deutsch.ttf", "File 2"),
							      rtslib.button("file3", [900,250], self.clickHandler, self.menubuttonset, "resources/fonts/Deutsch.ttf", "File 3"),
							      rtslib.button("back", [50,500], self.clickHandler, self.menubuttonset, "resources/fonts/Deutsch.ttf", "Back")]
		
		self.creditsbuttons = [rtslib.button("back", [480,650], self.clickHandler, self.menubuttonset, "resources/fonts/Deutsch.ttf", "Back")]
		
		self.settingsbuttons = [rtslib.button("back", [480,650], self.clickHandler, self.menubuttonset, "resources/fonts/Deutsch.ttf", "Back"),
							   rtslib.button("audio", [480,200], self.clickHandler, self.menubuttonset, "resources/fonts/Deutsch.ttf", "Audio")]
								  
		#self.settings
		
	def draw(self, surface):
		if self.state == "main":
			surface.blit(self.mainbg, [0,0])
			for b in self.mainbuttons:
				b.draw(surface)
		elif self.state == "fileselect":
			surface.blit(self.fileselectbg, [0,0])
			for b in self.fileselectbuttons:
				b.draw(surface)
		elif self.state == "settings":
			surface.blit(self.settingsbg, [0,0])
			for b in self.settingsbuttons:
				b.draw(surface)
		elif self.state == "credits":
			surface.blit(self.creditsbg, [0,0])
			for b in self.creditsbuttons:
				b.draw(surface)
		
	def clickHandler(self, button):
		if self.state == "main":
			if button == "play":
				self.state = "fileselect"
			if button == "settings":
				self.state = "settings"	
			if button == "credits":
				self.state = "credits"
			if button == "exit":
				self.state = "exit"
		elif self.state == "fileselect":
			if button == "back":
				self.state = "main"
			else:
				self.state = "level"
		elif self.state == "credits":
			if button == "back":
				self.state = "main"
		elif self.state == "settings":
			if button == "back":
				self.state = "main"
		
	def update(self, events):
		out = {}
		if self.state == "main":
			for b in self.mainbuttons:
				b.update(events)
		elif self.state == "fileselect":
			for b in self.fileselectbuttons:
				b.update(events)
		elif self.state == "settings":
			for b in self.settingsbuttons:
				b.update(events)
		elif self.state == "credits":
			for b in self.creditsbuttons:
				b.update(events)
		if self.state == "level":
			out["state"] = "game"
		if self.state == "exit":
			out["exit"]="now"
		out["title"] = "Save Our City"
		return out