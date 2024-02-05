import pygame
from pygame.rect import Rect
import os, sys
current_dir = os.path.dirname(__file__)
sys.path.append(current_dir)
from button import Button
from Inventory.inventoryManager import InventoryManager

class BikeShop:
    #Constants for UI stuff
    FONT_SIZE = 15
    FONT_SPACING = 10
    BUTTON_SPACING = 10
    SECONDARY_BUTTON_HEIGHT = 40
    LOWERBG_COLOR = (0, 80, 100)
    BUTTON_COLOR = (120, 120, 120)
    FONT_COLOR = (0, 0, 0)

    #boolean control vars for branching menu state
    isOpen = [False, False, False, False, False]

    #other mutable vars
    buttons = []
    secondaryButtons = []

    #Strings for text elements. may be refactored into textures later
    BUTTON_STRINGS = ["cockpit", "saddle", "drivetrain", "wheels", "Frame"]
    SECONDARY_OPTIONS = [["stem", "handlebar", "bar tape"], ["saddle", "seatpost"], 
                         ["crankset", "f. chainring", "chain", "pedals"], ["r. cog", "hubs", "spokes", "rims"], ["Frame"]]

    def __init__(self, screenSize):
        #gets resouce frolder set up 
        currentDir = os.path.dirname(__file__)
        resPath = os.path.join(currentDir, "res\\")

        #set up text renderer
        text = pygame.font.Font(resPath+"font.ttf", self.FONT_SIZE)

        self.screenSize = screenSize

        #set up lower stripe that acts as background for buttons
        lowerBgHeight = screenSize[1] // 5
        self.lowerBg = Rect(0, lowerBgHeight * 4, screenSize[0], lowerBgHeight)

        #represents the total box available for the primary buttons
        self.buttonRange = Rect(self.lowerBg[0] + self.BUTTON_SPACING, 
                           self.lowerBg[1] + self.BUTTON_SPACING,
                           self.lowerBg[2] - 2 * self.BUTTON_SPACING,
                           self.lowerBg[3] - 2 * self.BUTTON_SPACING)
        #calculate width of each button
        numButtons = 5
        self.buttonWidth = (self.buttonRange[2] - (numButtons - 1) * self.BUTTON_SPACING) // numButtons

        #loops through each button, builds object, and adds it to array.
        #offset is for moving buttons across screen without gaps or overlap.
        buttonOffset = 0
        for i, _ in enumerate(range(numButtons)):
            buttonRect = Rect(self.buttonRange[0] + buttonOffset, self.buttonRange[1], 
                                self.buttonWidth, self.buttonRange[3])
            self.buttons.append(Button(buttonRect, self.FONT_SIZE, self.FONT_SPACING,
                                self.BUTTON_COLOR, self.FONT_COLOR, self.BUTTON_STRINGS[i]))
            buttonOffset += self.buttonWidth + self.BUTTON_SPACING

        #sets up inventory manager
        inv = InventoryManager()
        
    #draws all elements of class to backside (called each tick)
    def draw(self, pygame, screen):
        screen.fill((0, 0, 0))
        pygame.draw.rect(screen, self.LOWERBG_COLOR, self.lowerBg)

        #draws each button in lists
        for button in self.buttons:
            button.draw(pygame, screen)

        for bool in self.isOpen:
            if bool:
                for button in self.secondaryButtons:
                    button.draw(pygame, screen)

    #generates and builds array of secondary buttons
    #called when a primary button is cliked on
    def generateSecondaryButtons(self, ind):
        self.secondaryButtons = []
        buttonOffset = 0
        for i, string in enumerate(self.SECONDARY_OPTIONS[ind]):
            buttonRect = (self.buttonRange[0] + ((self.buttonWidth + self.BUTTON_SPACING) * ind), 
                          self.buttonRange[1] - self.SECONDARY_BUTTON_HEIGHT - self.BUTTON_SPACING + buttonOffset,
                          self.buttonWidth, self.SECONDARY_BUTTON_HEIGHT)
            self.secondaryButtons.append(Button(buttonRect, self.FONT_SIZE, self.FONT_SPACING,
                                                self.BUTTON_COLOR, self.FONT_COLOR, 
                                                self.SECONDARY_OPTIONS[ind][i]))
            buttonOffset -= self.SECONDARY_BUTTON_HEIGHT + self.BUTTON_SPACING

    #updates button state control and does behaviour when passed a click
    def buttonClickCheck(self, click):
        for i, button in enumerate(self.buttons):
            if button.checkClicked(click):
                self.isOpen = [False, False, False, False, False]
                self.isOpen[i] = True
                self.generateSecondaryButtons(i)