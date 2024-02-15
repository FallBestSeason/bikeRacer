import pygame
from pygame.rect import Rect
import os, sys
current_dir = os.path.dirname(__file__)
sys.path.append(current_dir)
from button import Button
from slider import Slider
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
    BG_COLOR = (100, 100, 100)
    NAV_BUTTON_SIZE = (150, 45)
    #Strings for text elements. may be refactored into textures later
    BUTTON_STRINGS = ["frame & gearing", "saddle", "drivetrain", "wheels", "cockpit"]
    SECONDARY_OPTIONS = [["frame", "front gearing", "rear gearing"], ["saddle", "seatpost"], 
                         ["crankset", "chainring", "chain", "pedals"], 
                         ["hubs", "rims", "tires"], ["stem", "bar", "bar tape"]]
    NAV_STRINGS = ["BACK TO MENU", "GO RACE!"]

    #boolean control vars for branching menu state
    isOpen = [False, False, False, False, False]
    clickedButton = ""

    #other mutable vars
    buttons = []
    secondaryButtons = []
    tertiaryButtons = []
    navButtons = []

    def __init__(self, screenSize):
        #gets resouce frolder set up 
        currentDir = os.path.dirname(__file__)
        self.resPath = os.path.join(currentDir, "res\\")
        #import screensize from method
        self.screenSize = screenSize
        #clears button arrays
        self.buttons = []
        #set up lower stripe that acts as background for buttons
        lowerBgHeight = screenSize[1] // 5
        self.lowerBg = Rect(0, lowerBgHeight * 4, screenSize[0], lowerBgHeight)

        #generates lower main buttons
        self.generateNavButtons()
        #generates rects and objects for buttons
        self.generatePrimaryButtons()

        #sets up inventory manager
        self.inv = InventoryManager()

        #set up sliders and clipboard elements
        self.clipboardRect = (780, -80, 400, 300)
        self.sliders = [
            Slider(Rect(790, 400, 480, 62), 0, 2.43, 3.87, 0),
            Slider(Rect(790, 504, 480, 62), 0, -3.87, -2.43, 0)
        ]
        self.chainRingTextRects = [
            (860, 185, 100, 100), 
            (1130, 185, 100, 100)
        ]
        self.chainRingFont = pygame.font.Font(self.resPath+"font.ttf", 40)
        self.renderedChainRingTexts = []

        #set up scale and scale elements
        self.scaleRect = (340, 7, 200, 200)
        self.scaleTextRect = (396, 64, 100, 100)
        self.scaleFont = pygame.font.Font(self.resPath+"font.ttf", 30)
        self.renderedScaleText = ""

    #draws all elements of class to backside (called each tick)
    def draw(self, pygame, screen):
        screen.fill(self.BG_COLOR)

        #draws bike visualization that sits center screen
        self.drawBikeVisualization(pygame, screen)

        #draws scale background to screen
        scaleImage = pygame.image.load(f"{self.resPath}\\scale.png")
        screen.blit(scaleImage, self.scaleRect)

        #draws clipboard background to screen
        sliderLabelImage = pygame.image.load(f"{self.resPath}\\clipboard.png")
        sliderLabelImage = pygame.transform.scale(sliderLabelImage, (500, 666))
        screen.blit(sliderLabelImage, self.clipboardRect)
        
        #updates, then draws clipboard elements
        self.updateClipboard(self.sliders)
        for i, renderedText in enumerate(self.renderedChainRingTexts):
            screen.blit(renderedText, self.chainRingTextRects[i])
        for slider in self.sliders:
            slider.draw(pygame, screen)
        screen.blit(self.renderedScaleText, self.scaleTextRect)

        #draws nav buttons
        for button in self.navButtons:
            button.draw(pygame, screen)

        #draw lower bar buttons sit on
        pygame.draw.rect(screen, self.LOWERBG_COLOR, self.lowerBg)
        #draws each button in list
        for button in self.buttons:
            button.draw(pygame, screen)
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
        for key, value in self.inv.bike.getDict().items():
            if value != '':
                namedItem = self.inv.getItem(value)
                #make sure clicked item isn't a gearing, which have no path
                if "gearing" not in namedItem.get("category"):
                    currentImage = pygame.image.load(f"{self.resPath}{namedItem.get("imagePath")}")
                    currentImage = pygame.transform.scale(currentImage, (800, 800))
                    imageRect = currentImage.get_rect()
                    imageRect[0] += -5
                    imageRect[1] += 0
                    screen.blit(currentImage, imageRect)

    #updates data in slider objects given player setup
    def updateClipboard(self, sliders):
        #reset important values
        self.renderedChainRingTexts = []

        weight = self.inv.getWeight()
        self.renderedScaleText = self.scaleFont.render(str(weight), True, (0, 0, 0))

        #get info from current bike setup
        currentTeeth = [0, 0]
        ratio = 0
        for key, value in self.inv.bike.getDict().items():
            if value != '':
                currentTeeth[0] = float(self.inv.bike.getPartName("front gearing"))
                currentTeeth[1]  = float(self.inv.bike.getPartName("rear gearing"))
                ratio = currentTeeth[0] / currentTeeth[1]

        #update sliders at bottom of clipboard
        sliders[0].update(ratio)
        sliders[1].update(-ratio)

        #update text in chainring blanks
        self.renderedChainRingTexts.append(self.chainRingFont.render(str(int(currentTeeth[0])), True, (0, 0, 0)))
        self.renderedChainRingTexts.append(self.chainRingFont.render(str(int(currentTeeth[1])), True, (0, 0, 0)))

    #populates array of nav button objects
    def generateNavButtons(self):
        backButtonRect = (0, 0, self.NAV_BUTTON_SIZE[0], self.NAV_BUTTON_SIZE[1])
        raceButtonRect = (
            self.screenSize[0] - self.NAV_BUTTON_SIZE[0], 0, 
            self.NAV_BUTTON_SIZE[0], self.NAV_BUTTON_SIZE[1])
        self.navButtons.append(Button(
                backButtonRect, self.FONT_SIZE, self.FONT_SPACING,
                self.BUTTON_COLOR, self.FONT_COLOR, self.NAV_STRINGS[0]))
        self.navButtons.append(Button(
                raceButtonRect, self.FONT_SIZE, self.FONT_SPACING,
                self.BUTTON_COLOR, self.FONT_COLOR, self.NAV_STRINGS[1]))

    #generates array of primary buttons
    def generatePrimaryButtons(self):
        #represents the total box available for the primary buttons
        self.buttonRange = Rect(
            self.lowerBg[0] + self.BUTTON_SPACING, 
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
            buttonRect = Rect(
                self.buttonRange[0] + buttonOffset, self.buttonRange[1], 
                self.buttonWidth, self.buttonRange[3])
            self.buttons.append(Button(
                buttonRect, self.FONT_SIZE, self.FONT_SPACING,
                self.BUTTON_COLOR, self.FONT_COLOR, self.BUTTON_STRINGS[i]))
            buttonOffset += self.buttonWidth + self.BUTTON_SPACING

    #generates and builds array of secondary buttons off of button that was clicked
    def generateSecondaryButtons(self, ind):
        self.secondaryButtons = []
        buttonOffset = 0
        for i, string in enumerate(self.SECONDARY_OPTIONS[ind]):
            buttonRect = (
                self.buttonRange[0] + ((self.buttonWidth + self.BUTTON_SPACING) * ind), 
                self.buttonRange[1] - self.SECONDARY_BUTTON_HEIGHT - self.BUTTON_SPACING + buttonOffset,
                self.buttonWidth, self.SECONDARY_BUTTON_HEIGHT)
            self.secondaryButtons.append(Button(
                buttonRect, self.FONT_SIZE, self.FONT_SPACING,
                self.BUTTON_COLOR, self.FONT_COLOR, 
                self.SECONDARY_OPTIONS[ind][i]))
            buttonOffset -= self.SECONDARY_BUTTON_HEIGHT + self.BUTTON_SPACING

    #generate tertiary button options given that a subbutton was clicked
    def generateTertiaryButtons(self, ind):
        #ind in secondarybuttons
        self.tertiaryButtons = []
        buttonOffset = 0
        buttonYDirection = 0
        buttonXDirection = 1
        items = self.inv.getAllInCat(self.secondaryButtons[ind].string)

       #check if buttons fit screen going down
        if (self.SECONDARY_BUTTON_HEIGHT + buttonOffset) * len(items) > self.lowerBg[1] - self.secondaryButtons[ind].rect[1]:
            #buttons go up!
            buttonYDirection = -1
        else: #buttons go down!
            buttonYDirection = 1
        if self.isOpen[4]: #if last button, go left
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
            self.tertiaryButtons.append(Button(
                buttonRect, self.FONT_SIZE, self.FONT_SPACING,
                self.BUTTON_COLOR, self.FONT_COLOR, item.get("name")))
            if buttonYDirection == 1:
                buttonOffset += self.SECONDARY_BUTTON_HEIGHT + self.BUTTON_SPACING
            else:
                buttonOffset -= self.SECONDARY_BUTTON_HEIGHT + self.BUTTON_SPACING

    #updates button state control and does behaviour when passed a click
    def buttonClickCheck(self, click):
        #checks if nav buttons have been pressed
        for button in self.navButtons:
            if button.checkClicked(click):
                return button.string

        #if primary button clicked, reset + set state accordingly
        #generate secondary buttons from starting pos of primary
        for i, button in enumerate(self.buttons):
            if button.checkClicked(click):
                self.tertiaryButtons = []
                self.isOpen = [False, False, False, False, False]
                self.isOpen[i] = True
                if self.clickedButton == button:
                    self.secondaryButtons = []
                else:
                    self.generateSecondaryButtons(i)
                    self.clickedButton = ""
                self.clickedButton = button

        #if secondary button clicked, generate tertiary buttons
        #generation uses location of button clicked
        if len(self.secondaryButtons) != 0:
            for i, button in enumerate(self.secondaryButtons):
                if button.checkClicked(click):
                    self.tertiaryButtons = []
                    self.generateTertiaryButtons(i)

        #updates bike object in invmanager if tertiary button is clicked
        #calls screen to update drawing of bike too
        if len(self.tertiaryButtons) != 0:
            for i, button in enumerate(self.tertiaryButtons):
                if button.checkClicked(click):
                    clickedPart = self.inv.getItem(button.string)
                    self.inv.bike.setPart(clickedPart)
                    if clickedPart.get("category") == "frame":
                        test = self.inv.getSubFrame(button.string)
                        self.inv.bike.setPart(self.inv.getSubFrame(button.string))
                    self.tertiaryButtons = []