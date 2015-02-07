import pygame, os

buttonSets = {}
images = {}
loadTypes = [".png"]

def loadAll():
	global buttonSets, images
	for all in os.walk("resources"): #TODO: Put a loading bar on here as it could take time eventually
		for possFile in all[2]:
			if possFile[-4:] in loadTypes:
				if possFile[-4:] == ".png":
					images[(all[0]+"/"+possFile).replace("\\", "/")] = pygame.image.load(all[0]+"/"+possFile).convert_alpha()
	buttonSets = {"large":[images["resources/buttons/largeidle.png"], images["resources/buttons/largehover.png"], images["resources/buttons/largeclick.png"]],
				  "hud":[images["resources/buttons/smallidle.png"], images["resources/buttons/smallhover.png"], images["resources/buttons/smallclick.png"]]
				}