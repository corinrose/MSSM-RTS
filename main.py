import pygame, sys
import game, menu

pygame.init()

screen = pygame.display.set_mode([500,500])

state = "menu"

Menu = menu.menu()
Game = game.game()

while True:
	events = pygame.event.get()
	for event in events:
		if event.type == pygame.QUIT:
			sys.exit()
	
	if state == "menu":
		Menu.update(events)
		Menu.draw(screen)
	if state == "game":
		Game.update(events)
		Game.draw(screen)
		
	pygame.display.flip()