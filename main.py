import pygame, sys
import rtslib

pygame.init()

icon = pygame.image.load("resources/icon.png")
pygame.display.set_icon(icon)
pygame.display.set_caption("Save Our City")
screen = pygame.display.set_mode([1280,720])

rtslib.common.loadAll(screen)

state = "menu"

Menu = rtslib.menu()
Game = rtslib.game()

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
				if fullscreen:
					fullscreen = False
					screen = pygame.display.set_mode([1280,720])
				else:
					sys.exit()
			if event.key == pygame.K_F1:
				if not fullscreen:
					fullscreen = True
					screen = pygame.display.set_mode([1280,720], pygame.FULLSCREEN)
	out = {}
	if state == "menu":
		out = Menu.update(events)
		Menu.draw(screen)
	elif state == "game":
		out = Game.update(events)
		Game.draw(screen)
	
	if "state" in out:
		print "Setting state to "+out["state"]
		state = out["state"]
	
	if "newgame" in out:
		print "Resetting game"
		Game = rtslib.game()
		
	if "title" in out:
		pygame.display.set_caption(out["title"])
		
	if "exit" in out:
		sys.exit()

	clock.tick(60) # 60 frames per second???
	pygame.display.flip()