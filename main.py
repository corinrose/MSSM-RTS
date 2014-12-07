import pygame, sys
import rtslib

pygame.init()

screen = pygame.display.set_mode([1280,720])

state = "menu"

Menu = rtslib.menu()
Game = rtslib.game()

clock = pygame.time.Clock()

while True:
	events = pygame.event.get()
	for event in events:
		if event.type == pygame.QUIT:
			sys.exit()
	
	out = {}
	if state == "menu":
		out = Menu.update(events)
		Menu.draw(screen)
	if state == "game":
		out = Game.update(events)
		Game.draw(screen)
	
	if "state" in out:
		state = out["state"]
		
	if "title" in out:
		pygame.display.set_caption(out["title"])
	
	clock.tick(60)
	pygame.display.flip()