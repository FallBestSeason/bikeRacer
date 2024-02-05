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
    BG_COLOR = (80, 80, 80)

    #boolean control vars for branching menu state
    isOpen = [False, False, False, False, False]

    #other mutable vars
    buttons = []
    secondaryButtons = []
    tertiaryButtons = []

    #Strings for text elements. may be refactored into textures later
    BUTTON_STRINGS = ["cockpit", "saddle", "drivetrain", "wheels", "frame"]
    SECONDARY_OPTIONS = [["stem", "handlebar", "bar tape"], ["saddle", "seatpost"], 
                         ["crankset", "chainring", "chain", "pedals"], ["cog", "hubs", "spokes", "rims", "tires"], ["frame"]]

    def __init__(self, screenSize):
        #gets resouce frolder set up 
        currentDir = os.path.dirname(__file__)
        self.resPath = os.path.join(currentDir, "res\\")

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
        self.inv = InventoryManager()
        
    #draws all elements of class to backside (called each tick)
    def draw(self, pygame, screen):
        screen.fill(self.BG_COLOR)

        #draw lower bar buttons sit on
        pygame.draw.rect(screen, self.LOWERBG_COLOR, self.lowerBg)

        #draws each button in lists
        for button in self.buttons:
            button.draw(pygame, screen)

        self.drawBikeVisualization(pygame, screen)

        #draw sub buttons if state requires
        for bool in self.isOpen:
            if bool:
                for button in self.secondaryButtons:
                    button.draw(pygame, screen)

        #draw sub-sub-buttons if nessecary
        for button in self.tertiaryButtons:
            button.draw(pygame, screen)

    #draws bike to screen
    #will be massively rewritten in future!
    def drawBikeVisualization(self, pygame, screen):
        #todo for each element in bike.items
        name = self.inv.bike.getPartName("frame")
        test = self.inv.getItem(name)
        frameImage = pygame.image.load(test.get("imagePath"))
        frameImage = pygame.transform.scale(frameImage, (1024, 1024))
        imageRect = frameImage.get_rect()
        imageRect[0] += 150
        imageRect[1] -= 100
        screen.blit(frameImage, imageRect)

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

    #generate tertiary button options given that a subbutton was clicked
    def generateTertiaryButtons(self, ind):
        #ind in secondarybuttons
        self.tertiaryButtons = []
        buttonOffset = 0
        #1 for positive -1 for negative (weird! screen coords are top left)
        buttonYDirection = 0
        buttonXDirection = 1
        #get list of inventory items given a category (new method in invmanager?)
        items = self.inv.getAllInCat(self.secondaryButtons[ind].string)

        #if height of upcoming buttons is greater than distance between bar and top of current button
        if (self.SECONDARY_BUTTON_HEIGHT + buttonOffset) * len(items) > self.lowerBg[1] - self.secondaryButtons[ind].rect[0]:
            #buttons go up!
            buttonYDirection = -1
        else:
            #buttons go down!
            buttonYDirection = 1

        #if button is the last one
        if ind == len(self.secondaryButtons) - 1:
            #buttons go to the left!
            buttonXDirection = -1

        #calculate position of -each button and put it into tertiaryButtons as a rect (foreach item in list in category)
        for item in items:
            x = self.secondaryButtons[ind].rect[0] + self.buttonWidth + self.BUTTON_SPACING
            y = self.secondaryButtons[ind].rect[1] + buttonOffset
            w = self.buttonWidth
            h = self.SECONDARY_BUTTON_HEIGHT
            buttonRect = Rect(x, y, w, h)
            if buttonXDirection == -1:
                buttonRect[0] -= 2 * (self.buttonWidth + self.BUTTON_SPACING)
            self.tertiaryButtons.append(Button(buttonRect, self.FONT_SIZE, self.FONT_SPACING,
                                                self.BUTTON_COLOR, self.FONT_COLOR, 
                                                item.get("name")))
            if buttonYDirection == 1:
                buttonOffset += self.SECONDARY_BUTTON_HEIGHT + self.BUTTON_SPACING
            else:
                buttonOffset -= self.SECONDARY_BUTTON_HEIGHT + self.BUTTON_SPACING

    #updates button state control and does behaviour when passed a click
    def buttonClickCheck(self, click):
        self.tertiaryButtons = []

        #if primary button clicked, reset + set state accordingly
        #generate secondary buttons from starting pos of primary
        for i, button in enumerate(self.buttons):
            if button.checkClicked(click):
                self.isOpen = [False, False, False, False, False]
                self.isOpen[i] = True
                self.generateSecondaryButtons(i)

        #if secondary button clicked, generate tertiary buttons
        #generation uses location of button clicked
        if len(self.secondaryButtons) != 0:
            for i, button in enumerate(self.secondaryButtons):
                if button.checkClicked(click):
                    self.generateTertiaryButtons(i)

        #updates bike object in invmanager if tertiary button is clicked
        #calls screen to update drawing of bike too
        if len(self.tertiaryButtons) != 0:
            for i, button in enumerate(self.tertiaryButtons):
                if button.checkClicked(click):
                    self.inv.bike.setPart(self.inv.getItem(button.string))
                