import pygame
from pygame.rect import Rect
import os

class MainMenu:
    #constants for ui stuff
    BUTTON_SIZE = 400, 100
    BUTTON_SPACING = 30
    BUTTON_FONT_SIZE = 20
    BUTTON_FONT_SPACING = 10    
    BACKGROUND_COLOR = (0, 80, 100)
    BUTTON_COLOR = (120, 120, 120)
    BUTTON_TEXT_COLOR =(0, 0, 0)

    #strings for text elements that don't need a resource
    #will probably be refactored out later in support of button textures
    GARAGE_BUTTON_STRING = "ENTER SHOP"
    CREDITS_BUTTON_STRING = "CREDITS"
    QUIT_BUTTON_STRING = "QUIT"
    
    def __init__(self, screenSize):
        #gets resouce frolder set up 
        currentDir = os.path.dirname(__file__)
        resPath = os.path.join(currentDir, "res\\")

        #set up text renderer
        logoFontSize = 10
        logoFont = pygame.font.Font(resPath+"font.ttf", logoFontSize)

        #read logo files from res
        with open(resPath+"logo.txt") as f:
            logo = f.read()
        #Split logo text into lines
        logoLines = logo.split('\n')
        #Render each line of the logo text
        self.logoRendered = []
        for line in logoLines:
            self.logoRendered.append(logoFont.render(line, True, (255, 255, 255)))

        #set up rectangles for each UI element
        self.screenSize = screenSize
        self.garageButton = (self.BUTTON_SPACING, 
                             screenSize[1] // 2 - self.BUTTON_SIZE[1] // 2,
                             self.BUTTON_SIZE[0], self.BUTTON_SIZE[1])
        self.garageButtonText = self.getTextBoxForButton(self.garageButton)
        self.creditsButton = (self.BUTTON_SPACING,
                              screenSize[1] // 2 - self.BUTTON_SIZE[1] // 2+
                              self.BUTTON_SIZE[1] + self.BUTTON_SPACING,
                              self.BUTTON_SIZE[0], self.BUTTON_SIZE[1])
        self.creditsButtonText = self.getTextBoxForButton(self.creditsButton)
        self.quitButton = (self.BUTTON_SPACING,
                           screenSize[1] // 2 - self.BUTTON_SIZE[1] // 2+
                           (2 * self.BUTTON_SIZE[1]) + (2 * self.BUTTON_SPACING),
                           self.BUTTON_SIZE[0], self.BUTTON_SIZE[1])
        self.quitButtonText = self.getTextBoxForButton(self.quitButton)
        self.logoRect = Rect(self.BUTTON_SPACING, self.BUTTON_SPACING, 
                             screenSize[0] - self.BUTTON_SPACING * 2, 400)
        
        #sets up rendered buttons for drawing
        buttonFont = pygame.font.Font(resPath+"font.ttf", self.BUTTON_FONT_SIZE)
        self.garageButtonRendered = buttonFont.render(self.GARAGE_BUTTON_STRING, True, self.BUTTON_TEXT_COLOR)
        self.creditsButtonRendered = buttonFont.render(self.CREDITS_BUTTON_STRING, True, self.BUTTON_TEXT_COLOR)
        self.quitButtonRendered = buttonFont.render(self.QUIT_BUTTON_STRING, True, self.BUTTON_TEXT_COLOR)
        
    #functional, just retuns a box that is slightly smaller
    def getTextBoxForButton(self, rect):
        return (rect[0] + self.BUTTON_FONT_SPACING,
                rect[1] + self.BUTTON_FONT_SPACING,
                rect[2] - self.BUTTON_FONT_SPACING,
                rect[3] - self.BUTTON_FONT_SPACING)

    #draws all ui elements in to memory
    def draw(self, pygame, screen):

        #background
        pygame.draw.rect(screen, self.BACKGROUND_COLOR, 
                         (0, 0, self.screenSize[0], self.screenSize[1]))
        
        #logo
        y_offset = self.logoRect[1]
        for textSurface in self.logoRendered:
            screen.blit(textSurface, (self.logoRect[0], y_offset))
            y_offset += textSurface.get_height()
        
        #button rectangles
        pygame.draw.rect(screen, self.BUTTON_COLOR, self.garageButton)
        pygame.draw.rect(screen, self.BUTTON_COLOR, self.creditsButton)
        pygame.draw.rect(screen, self.BUTTON_COLOR, self.quitButton)

        #button text
        screen.blit(self.garageButtonRendered, 
                    (self.garageButtonText[0], self.garageButtonText[1]))
        screen.blit(self.creditsButtonRendered, 
                    (self.creditsButtonText[0], self.creditsButtonText[1]))
        screen.blit(self.quitButtonRendered, 
                    (self.quitButtonText[0], self.quitButtonText[1]))