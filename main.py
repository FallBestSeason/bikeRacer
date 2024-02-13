import pygame
from gameHandler import GameHandler
import os, sys
current_dir = os.path.dirname(__file__)
sys.path.append(current_dir)

def main():
    #varss
    running = True
    screenSize = (1280, 720)

    #set up pygame
    pygame.init()
    pygame.display.set_caption("BIKERACER!")
    screen = pygame.display.set_mode(screenSize)

    #gamehandler object represents game states
    #handles logic for which UI to draw
    #and starting and ending races
    gh = GameHandler(screenSize, pygame, screen)

    while running:
        for event in pygame.event.get():
            running = gh.event(event)
                        
        #game tick 
        #draws current UI
        gh.draw()

        #puts frame in memory on screen
        pygame.display.flip()

if __name__=="__main__":
    main()