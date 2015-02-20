import pygame, sys
import rtslib

class menu():
	def __init__(self, settings):
		self.settings = settings
		self.state = "main"
		self.mainbg = rtslib.common.images["resources/menubg/main.png"]
		self.fileselectbg = rtslib.common.images["resources/menubg/fileselect.png"]
		self.settingsbg = rtslib.common.images["resources/menubg/settings.png"]
		self.creditsbg = rtslib.common.images["resources/menubg/credits.png"]
		
		self.mainbuttons = [rtslib.button("play", [100,325], self.clickHandler, rtslib.common.buttonSets["large"], "resources/fonts/Deutsch.ttf", "Play"),
							rtslib.button("settings", [100,405], self.clickHandler, rtslib.common.buttonSets["large"], "resources/fonts/Deutsch.ttf", "Settings"),
							rtslib.button("credits", [100,485], self.clickHandler, rtslib.common.buttonSets["large"], "resources/fonts/Deutsch.ttf", "Credits"),
							rtslib.button("exit", [100,565], self.clickHandler, rtslib.common.buttonSets["large"], "resources/fonts/Deutsch.ttf", "Exit")]
							
		self.fileselectbuttons = [rtslib.button("saves/1.sav", [60,250], self.clickHandler, rtslib.common.buttonSets["large"], "resources/fonts/Deutsch.ttf", "File 1"),
								  rtslib.button("saves/2.sav", [480,250], self.clickHandler, rtslib.common.buttonSets["large"], "resources/fonts/Deutsch.ttf", "File 2"),
							      rtslib.button("saves/3.sav", [900,250], self.clickHandler, rtslib.common.buttonSets["large"], "resources/fonts/Deutsch.ttf", "File 3"),
							      rtslib.button("back", [50,500], self.clickHandler, rtslib.common.buttonSets["large"], "resources/fonts/Deutsch.ttf", "Back")]
		
		self.levelselectbuttons = []
		self.levelbuttons = rtslib.loader.loadLevelButtons(self)
		
		self.creditsbuttons = [rtslib.button("back", [480,650], self.clickHandler, rtslib.common.buttonSets["large"], "resources/fonts/Deutsch.ttf", "Back")]
		
		self.settingsbuttons = [rtslib.button("back", [480,650], self.clickHandler, rtslib.common.buttonSets["large"], "resources/fonts/Deutsch.ttf", "Back"),
							    rtslib.button("fullscreen", [480,200], self.clickHandler, rtslib.common.buttonSets["large"], "resources/fonts/Deutsch.ttf", "Fullscreen: "+("On"*self.settings["fullscreen"])+("Off"*(not self.settings["fullscreen"])))]

		self.applySettings = False
		
		self.save = None
		self.saveData = []
	
	def draw(self, surface):
		if self.state == "main":
			surface.blit(self.mainbg, [0,0])
			for b in self.mainbuttons:
				b.draw(surface)
		elif self.state == "fileselect":
			surface.blit(self.fileselectbg, [0,0])
			for b in self.fileselectbuttons:
				b.draw(surface)
		elif self.state == "levelselect":
			surface.fill([150,150,150])
			for b in self.levelselectbuttons:
				b.draw(surface)
			for b in self.levelbuttons:
				self.levelbuttons[b].draw(surface)
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
				self.save = button
				self.saveData = rtslib.loader.loadSave(self.save)
				print self.save
				print self.saveData
				self.enableLevelButtons()
				self.state = "levelselect"
		elif self.state == "levelselect":
			if button == "back":
				pass
			else:
				self.state="play-"+button
		elif self.state == "credits":
			if button == "back":
				self.state = "main"
		elif self.state == "settings":
			if button == "fullscreen":
				self.settings["fullscreen"] = not self.settings["fullscreen"]
				self.settingsbuttons[1].setText("Fullscreen: "+("On"*self.settings["fullscreen"])+("Off"*(not self.settings["fullscreen"])))
				self.applySettings = True
				
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
		elif self.state == "levelselect":
			for b in self.levelselectbuttons:
				b.update(events)
			for b in self.levelbuttons:
				self.levelbuttons[b].update(events)
		elif self.state == "settings":
			for b in self.settingsbuttons:
				b.update(events)
		elif self.state == "credits":
			for b in self.creditsbuttons:
				b.update(events)
				
		if self.state[0:4] == "play":
			out["state"] = "game"
			out["newgame"] = self.state[5:]
			self.state = "levelselect"
		if self.applySettings:
			out["applysettings"] = True
			self.applySettings = False
		if self.state == "exit":
			out["exit"]="now"
		out["title"] = "Save Our City"
		return out
	
	def enableLevelButtons(self):
		for b in self.levelbuttons:
			self.levelbuttons[b].setEnabled(False)
		for level in self.saveData:
					self.levelbuttons[level].setEnabled(True)
	
	def unlock(self, unlocks):
		for unlock in unlocks:
			if unlock not in self.saveData:
				self.saveData.append(unlock)
		rtslib.loader.saveSave(self.saveData, self.save)
		self.enableLevelButtons()