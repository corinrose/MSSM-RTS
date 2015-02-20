import pygame, sys
import rtslib

pygame.init()

settings = rtslib.loadSettings()

icon = pygame.image.load("resources/icon.png")
pygame.display.set_icon(icon)
pygame.display.set_caption("Save Our City")
screen = pygame.display.set_mode([1280,720], settings["fullscreen"]*pygame.FULLSCREEN)

rtslib.common.loadAll(screen)

state = "menu"

Menu = rtslib.menu(settings)
Game = rtslib.game("resources/skele01")

clock = pygame.time.Clock()
pygame.key.set_repeat(5,5)

fullscreen = False

while True:
	events = pygame.event.get()
	for event in events:
		if event.type == pygame.QUIT:
			sys.exit()
		if event.type == pygame.KEYUP:
			if event.key == pygame.K_ESCAPE:
				sys.exit()

	out = {}
	if state == "menu":
		out = Menu.update(events)
		Menu.draw(screen)
	elif state == "game":
		out = Game.update(events)
		Game.draw(screen)
	
	if "newgame" in out:
		print "Resetting game, loading " + out["newgame"]
		Game = rtslib.game(out["newgame"])
	
	if "state" in out:
		print "Setting state to "+out["state"]
		state = out["state"]
		
	if "applysettings" in out:
		screen = pygame.display.set_mode([1280,720], settings["fullscreen"]*pygame.FULLSCREEN)
		rtslib.loader.saveSettings(settings)
		
	if "title" in out:
		pygame.display.set_caption(out["title"])
		
	if "exit" in out:
		sys.exit()

	clock.tick(60) # 60 frames per second???
	pygame.display.flip()