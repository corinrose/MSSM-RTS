import pygame, os

buttonSets = {}
images = {}
sounds = {}
loadTypes = [".png", ".wav"]

def loadAll(surface):
	global buttonSets, images, sounds
	#bg = pygame.image.load() #This goes against the entire idea of this module/function, but whatever
	surface.fill([255,255,255])
	pygame.draw.rect(surface, [0,0,0], [200, 300, 880, 120], 2)
	pygame.display.flip()
	res = list(os.walk("resources"))
	totFiles = 0
	for c in res:
		for p in c[2]:
			if p[-4:] in loadTypes:
				totFiles+=1
	print "Loading "+str(totFiles)+" files"
	cFile = 0.0
	for all in res:
		for possFile in all[2]:
			if possFile[-4:] in loadTypes or possFile[-5:] in loadTypes:
				surface.fill([255,255,255])
				pygame.draw.rect(surface, [0,0,0], [200, 300, (cFile/totFiles)*880, 120], 0)
				pygame.draw.rect(surface, [0,0,0], [200, 300, 880, 120], 2)
				pygame.display.flip()
				if possFile[-4:] == ".png":
					images[(all[0]+"/"+possFile).replace("\\", "/")] = pygame.image.load(all[0]+"/"+possFile).convert_alpha()
				if possFile[-4:] == ".wav":
					sounds[(all[0]+"/"+possFile).replace("\\", "/")] = pygame.mixer.Sound(all[0]+"/"+possFile)
				cFile+=1
					
	buttonSets = {"large":[images["resources/buttons/largeidle.png"], images["resources/buttons/largehover.png"], images["resources/buttons/largeclick.png"]],
				  "hud":[images["resources/buttons/smallidle.png"], images["resources/buttons/smallhover.png"], images["resources/buttons/smallclick.png"]]
				}