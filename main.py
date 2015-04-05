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

	out = {}
	if state == "menu":
		out = Menu.update(events)
	elif state == "game":
		out = Game.update(events)
	
	if "newgame" in out:
		Game = rtslib.game(out["newgame"])
		
	if "unlocks" in out:
		Menu.unlock(out["unlocks"])
	
	if "state" in out:
		state = out["state"]
		
	if "applysettings" in out:
		screen = pygame.display.set_mode([1280,720], settings["fullscreen"]*pygame.FULLSCREEN)
		rtslib.loader.saveSettings(settings)
		
	if "title" in out:
		pygame.display.set_caption(out["title"])
		
	if "backtogame" in out:
		Menu.state = "settings"
		Menu.goBackToGame = True
		
	if "exit" in out:
		sys.exit()

	if state == "menu":
		Menu.draw(screen)
	elif state == "game":
		Game.draw(screen)		
		
	clock.tick(60) # 60 frames per second???
	pygame.display.flip()