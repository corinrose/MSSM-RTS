import pygame

buttonSets = {}
images = {}

def loadAll():
	global buttonSets, images
	buttonSets = {"large":[pygame.image.load("resources/buttons/largeidle.png").convert_alpha(), pygame.image.load("resources/buttons/largehover.png").convert_alpha(), pygame.image.load("resources/buttons/largeclick.png").convert_alpha()],
				  "hud":[pygame.image.load("resources/buttons/smallidle.png").convert_alpha(), pygame.image.load("resources/buttons/smallhover.png").convert_alpha(), pygame.image.load("resources/buttons/smallclick.png").convert_alpha()]
				}