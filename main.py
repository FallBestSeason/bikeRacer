import pygame
from gameHandler import GameHandler

def main():
    #varss
    running = True
    screenSize = (1280, 720)

    #gamehandler object represents game states
    #handles logic for which UI to draw
    #and starting and ending races
    gh = GameHandler()

    #set up pygame
    pygame.init()
    pygame.display.set_caption("BIKERACER!")
    screen = pygame.display.set_mode(screenSize)

    while running:
        for event in pygame.event.get():
            #quits game
            if event.type == pygame.QUIT:
                running = False

            #do keeb stuff here
        #game tick 
                
        #draws current UI
        gh.updateUI(pygame, screen, screenSize)

        #puts frame in memory on screen
        pygame.display.flip()
        

if __name__=="__main__":
    main()