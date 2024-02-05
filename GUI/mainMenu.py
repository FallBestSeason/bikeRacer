import pygame
from pygame.rect import Rect
import os, sys
current_dir = os.path.dirname(__file__)
sys.path.append(current_dir)
from button import Button

class MainMenu:
    #constants for ui stuff
    BUTTON_SIZE = 400, 100                                                        
    BUTTON_SPACING = 30
    BUTTON_FONT_SIZE = 40
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
        logoFontSize = 15
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

        self.screenSize = screenSize

        #set up button objects
        self.buttons = []
        rect = (self.BUTTON_SPACING, screenSize[1] // 2 - self.BUTTON_SIZE[1] // 2,
                self.BUTTON_SIZE[0], self.BUTTON_SIZE[1])
        self.buttons.append(Button(rect, self.BUTTON_FONT_SIZE, self.BUTTON_FONT_SPACING,
                                 self.BUTTON_COLOR, self.BUTTON_TEXT_COLOR, 
                                 self.GARAGE_BUTTON_STRING))
        rect = (self.BUTTON_SPACING, screenSize[1] // 2 - self.BUTTON_SIZE[1] // 2 +
                self.BUTTON_SIZE[1] + self.BUTTON_SPACING,
                self.BUTTON_SIZE[0], self.BUTTON_SIZE[1])
        self.buttons.append(Button(rect, self.BUTTON_FONT_SIZE, self.BUTTON_FONT_SPACING,
                                    self.BUTTON_COLOR, self.BUTTON_TEXT_COLOR, 
                                    self.CREDITS_BUTTON_STRING))
        rect = (self.BUTTON_SPACING, screenSize[1] // 2 - self.BUTTON_SIZE[1] // 2 +
                (2 * self.BUTTON_SIZE[1]) + (2 * self.BUTTON_SPACING), 
                self.BUTTON_SIZE[0], self.BUTTON_SIZE[1])
        self.buttons.append(Button(rect, self.BUTTON_FONT_SIZE, self.BUTTON_FONT_SPACING,
                                   self.BUTTON_COLOR, self.BUTTON_TEXT_COLOR, 
                                   self.QUIT_BUTTON_STRING))

        #rectangle to define "text box" for logo ascii
        self.logoRect = Rect(self.BUTTON_SPACING, self.BUTTON_SPACING, 
                             screenSize[0] - self.BUTTON_SPACING * 2, 400)

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
        
        #buttons
        for button in self.buttons:
            button.draw(pygame, screen)

    #checks if buttons have been clicked, returns text on button if so
    def buttonClickCheck(self, click):
        for button in self.buttons:
            if button.checkClicked(click):
                return button.string