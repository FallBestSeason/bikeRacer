import pygame
from pygame.rect import Rect
import os, sys
current_dir = os.path.dirname(__file__)
sys.path.append(current_dir)
from button import Button
from imageButton import ImageButton
from slider import Slider
from textbox import TextBox
from inventory.inventoryManager import InventoryManager

class BikeShop:
    #Constants for UI stuff
    FONT_SIZE = 20
    FONT_SPACING = 10
    BUTTON_SPACING = 10
    SECONDARY_BUTTON_HEIGHT = 40
    NAV_BUTTON_SIZE = (180, 45)
    PRIMARY_BUTTON_SIZE = (244, 122)

    LOWERBG_COLOR = (102, 57, 49)
    BUTTON_COLOR = (120, 120, 120)
    LOCKED_BTN_COLOR = (85, 85, 85)
    FONT_COLOR = (0, 0, 0)
    BG_COLOR = (100, 100, 100)

    BG_PATH = "\\shop elements\\shopBackground.png"
    BUTTON_PATHS = [
        "\\shop elements\\frameAndGearingLabel.png",
        "\\shop elements\\saddleLabel.png",
        "\\shop elements\\drivetrainLabel.png",
        "\\shop elements\\wheelsLabel.png",
        "\\shop elements\\cockpitLabel.png",
    ]
    POPUP_PATH = "\\shop elements\\popupBackground.png"
    BUTTON_STRINGS = ["frame & gearing", "saddle", "drivetrain", "wheels", "cockpit"]
    SECONDARY_OPTIONS = [["frame", "front gearing", "rear gearing"], ["saddle", "seatpost"], 
                         ["crankset", "chainring", "chain", "pedals"], 
                         ["hubs", "rims", "tires"], ["stem", "bar", "bar tape"]]
    NAV_STRINGS = ["MAIN MENU", "GO RACE!"]

    #clipboard stuff
    CLIPBOARD_RECT = (780, -80, 400, 300)
    RATIO_TXT_RECTS = [
        (860, 185, 100, 100), 
        (1130, 185, 100, 100)
    ]
    CB_SLIDERS = [
        Slider(Rect(790, 400, 480, 62), 0, 2.43, 3.87, 0),
        Slider(Rect(790, 504, 480, 62), 0, -3.87, -2.43, 0)
    ]
    #scale stuff
    SCALE_RECT = (340, 7, 200, 200)
    SCALE_TEXT_RECT = (396, 64, 100, 100)
    #purchase popup stuff
    POPUP_SIZE = 400, 400
    #money indicator things
    MONEY_RECT = (0, 50, 100, 20)

    #boolean control vars for branching menu state
    isOpen = [False, False, False, False, False]
    popup = False

    buttons = []
    secondaryButtons = []
    tertiaryButtons = []
    navButtons = []

    popupElements = []
    popupItem = ""
    renderedChainRingTexts = []
    renderedScaleText = ""

    def __init__(self, screenSize):
        self.buttons = []

        currentDir = os.path.dirname(__file__)
        self.resPath = os.path.join(currentDir, "res\\")
        self.screenSize = screenSize

        #set up lower stripe that acts as background for buttons
        lowerBgHeight = screenSize[1] // 5
        self.lowerBg = Rect(0, lowerBgHeight * 4, screenSize[0], lowerBgHeight)

        self.generateNavButtons()
        self.generatePrimaryButtons()
        self.inv = InventoryManager()

        self.chainRingFont = pygame.font.Font(self.resPath+"joystix.otf", 40)
        self.scaleFont = pygame.font.Font(self.resPath+"joystix.otf", 23)

        self.moneyBox = TextBox(self.MONEY_RECT, f"balance: ${self.inv.money}", 20, "joystix.otf")

    #draws all elements of class to backside (called each tick)
    def draw(self, pygame, screen, dTime):
        #draws background
        screen.fill(self.BG_COLOR)
        bgImage = pygame.image.load(self.resPath + self.BG_PATH)
        bgImage = pygame.transform.scale(bgImage, (2500, 1406))
        bgImageRect = Rect(
            -400,
            -400,
            bgImage.get_rect().width,
            bgImage.get_rect().height
        )
        screen.blit(bgImage, bgImageRect)

        #draws bike visualization that sits center screen
        self.drawBikeVisualization(pygame, screen)

        #draws scale background to screen
        scaleImage = pygame.image.load(f"{self.resPath}shop elements\\scale.png")
        screen.blit(scaleImage, self.SCALE_RECT)

        #draws clipboard background to screen
        sliderLabelImage = pygame.image.load(f"{self.resPath}shop elements\\clipboard.png")
        sliderLabelImage = pygame.transform.scale(sliderLabelImage, (500, 666))
        screen.blit(sliderLabelImage, self.CLIPBOARD_RECT)
        
        #updates, then draws clipboard elements
        self.updateClipboard(self.CB_SLIDERS)
        for i, renderedText in enumerate(self.renderedChainRingTexts):
            screen.blit(renderedText, self.RATIO_TXT_RECTS[i])
        for slider in self.CB_SLIDERS:
            slider.draw(pygame, screen)
        screen.blit(self.renderedScaleText, self.SCALE_TEXT_RECT)

        #draws nav buttons
        for button in self.navButtons:
            button.draw(pygame, screen)

        #draw lower bar buttons sit on
        pygame.draw.rect(screen, self.LOWERBG_COLOR, self.lowerBg)
        for button in self.buttons:
            button.draw(pygame, screen)

        #draw sub buttons if applicable
        for bool in self.isOpen:
            if bool:
                for button in self.secondaryButtons:
                    button.draw(pygame, screen)

        #draw tertiary buttons if nessecary
        for button in self.tertiaryButtons:
            button.draw(pygame, screen)

        #updates, draws money indicator 
        self.moneyBox.updateText(f"balance: ${self.inv.money}")
        self.moneyBox.draw(pygame, screen)

        #draw popup elements if needed
        if self.popupItem != "":
            popupBGImage = pygame.image.load(f"{self.resPath}{self.POPUP_PATH}")
            screen.blit(popupBGImage, (self.screenSize[0] // 2 - 200, self.screenSize[1] // 2 - 200, 400, 400))
            for element in self.popupElements:
                element.draw(pygame, screen)  

    #updates button state control and does behaviour when passed a click
    def buttonClickCheck(self, click):
        #checks if nav buttons have been pressed
        for button in self.navButtons:
            if button.checkClicked(click):
                return button.string

        #checks if popup buttons have been pressed
        for element in self.popupElements:
            try:
                if element.checkClicked(click):
                    if element.string == "YES":
                        selectedPart = self.inv.getItem(self.popupItem)
                        if self.inv.money >= selectedPart.get("cost"):
                            self.inv.money -= selectedPart.get("cost")
                            self.inv.bike.setPart(selectedPart)
                            if selectedPart.get("category") == "frame":
                                self.inv.bike.setPart(self.inv.getSubFrame(self.popupItem))
                            self.inv.updateItem(self.popupItem, "unlocked", "True")
                    self.tertiaryButtons = []
                    self.secondaryButtons = []
                    self.popupElements = []
                    self.popupItem = ""
            except:
                print("you know the spot")

        #if primary button clicked, reset + set state accordingly
        #generate secondary buttons from starting pos of primary
        for i, button in enumerate(self.buttons):
            if button.checkClicked(click):
                self.tertiaryButtons = []
                if self.isOpen[i]:
                    self.secondaryButtons = []
                    self.isOpen = [False, False, False, False, False]
                else:
                    self.generateSecondaryButtons(i)
                    self.isOpen = [False, False, False, False, False]
                    self.isOpen[i] = True

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
                    if clickedPart.get("unlocked") == "True":
                        self.inv.bike.setPart(clickedPart)
                        if clickedPart.get("category") == "frame":
                            self.inv.bike.setPart(self.inv.getSubFrame(button.string))
                        self.tertiaryButtons = []
                    else:
                        self.generatePopupElements(
                            clickedPart.get("name"), 
                            clickedPart.get("cost")
                        )           

    #draws bike to screen
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
        self.renderedChainRingTexts.append(
            self.chainRingFont.render(str(int(currentTeeth[0])), True, (0, 0, 0))
        )
        self.renderedChainRingTexts.append(
            self.chainRingFont.render(str(int(currentTeeth[1])), True, (0, 0, 0))
        )

    #populates array of nav button objects
    def generateNavButtons(self):
        backButtonRect = (0, 0, self.NAV_BUTTON_SIZE[0], self.NAV_BUTTON_SIZE[1])
        raceButtonRect = (
            self.screenSize[0] - self.NAV_BUTTON_SIZE[0], 0, 
            self.NAV_BUTTON_SIZE[0], self.NAV_BUTTON_SIZE[1]
        )
        self.navButtons.append(
            Button(
                backButtonRect, 
                self.FONT_SIZE, 
                self.FONT_SPACING,
                self.BUTTON_COLOR, 
                self.FONT_COLOR, 
                self.NAV_STRINGS[0]
            )
        )
        self.navButtons.append(
            Button(
                raceButtonRect, 
                self.FONT_SIZE, 
                self.FONT_SPACING,
                self.BUTTON_COLOR, 
                self.FONT_COLOR, 
                self.NAV_STRINGS[1]
            )
        )

    #generates array of primary buttons
    def generatePrimaryButtons(self):
        #represents the total box available for the primary buttons
        self.buttonRange = Rect(
            self.lowerBg[0] + self.BUTTON_SPACING, 
            self.lowerBg[1] + self.BUTTON_SPACING,
            self.lowerBg[2] - 2 * self.BUTTON_SPACING,
            self.lowerBg[3] - 2 * self.BUTTON_SPACING)

        #loops through each button, builds object, and adds it to array.
        #offset is for moving buttons across screen without gaps or overlap.
        buttonOffset = 0
        for i in range(5):
            currentImage = pygame.image.load(self.resPath+self.BUTTON_PATHS[i])
            buttonRect = Rect(
                self.buttonRange[0] + buttonOffset, self.buttonRange[1], 
                self.PRIMARY_BUTTON_SIZE[0], self.PRIMARY_BUTTON_SIZE[1])
            self.buttons.append(ImageButton(buttonRect, currentImage, self.BUTTON_STRINGS[i]))
            buttonOffset += self.PRIMARY_BUTTON_SIZE[0] + self.BUTTON_SPACING

    #generates and builds array of secondary buttons off of button that was clicked
    def generateSecondaryButtons(self, ind):
        self.secondaryButtons = []
        buttonOffset = 0
        for i, string in enumerate(self.SECONDARY_OPTIONS[ind]):
            buttonRect = (
                self.buttonRange[0] + ((self.PRIMARY_BUTTON_SIZE[0] + self.BUTTON_SPACING) * ind), 
                self.buttonRange[1] - self.SECONDARY_BUTTON_HEIGHT - self.BUTTON_SPACING + buttonOffset,
                self.PRIMARY_BUTTON_SIZE[0], self.SECONDARY_BUTTON_HEIGHT)
            self.secondaryButtons.append(Button(
                buttonRect, self.FONT_SIZE, self.FONT_SPACING,
                self.BUTTON_COLOR, self.FONT_COLOR, 
                self.SECONDARY_OPTIONS[ind][i]))
            buttonOffset -= self.SECONDARY_BUTTON_HEIGHT + self.BUTTON_SPACING

    #generate tertiary button options given that a subbutton was clicked
    def generateTertiaryButtons(self, ind):
        self.tertiaryButtons = []
        buttonOffset = 0
        buttonYDirection = 0
        buttonXDirection = 1
        items = self.inv.getAllInCat(self.secondaryButtons[ind].string)

        if (self.SECONDARY_BUTTON_HEIGHT + buttonOffset) * len(items) > self.lowerBg[1] - self.secondaryButtons[ind].rect[1]:
            buttonYDirection = -1
        else: #buttons go down if they don't fit
            buttonYDirection = 1
        if self.isOpen[4]: #if last button, go left
            buttonXDirection = -1 

        #calculate position of each button and put it into 
        #tertiaryButtons as a rect (foreach item in list in category)
        for item in items:
            if item.get("unlocked") == "False":
                buttonColor = self.LOCKED_BTN_COLOR
            else:
                buttonColor = self.BUTTON_COLOR
            buttonRect = Rect(
                self.secondaryButtons[ind].rect[0] + self.PRIMARY_BUTTON_SIZE[0] + self.BUTTON_SPACING,
                self.secondaryButtons[ind].rect[1] + buttonOffset,
                self.PRIMARY_BUTTON_SIZE[0],
                self.SECONDARY_BUTTON_HEIGHT
            )
            if buttonXDirection == -1:
                buttonRect[0] -= 2 * (self.PRIMARY_BUTTON_SIZE[0] + self.BUTTON_SPACING)
            self.tertiaryButtons.append(Button(
                buttonRect, self.FONT_SIZE, self.FONT_SPACING,
                buttonColor, self.FONT_COLOR, item.get("name")))
            if buttonYDirection == 1:
                buttonOffset += self.SECONDARY_BUTTON_HEIGHT + self.BUTTON_SPACING
            else:
                buttonOffset -= self.SECONDARY_BUTTON_HEIGHT + self.BUTTON_SPACING
    
    def generatePopupElements(self, itemName, amount):
        self.popupElements = []
        self.popupItem = itemName
        popupSize = (400, 400)
        offset = (self.screenSize[0] // 2, self.screenSize[1] // 2)
        self.popupElements.append(
            TextBox(
                (
                    offset[0] - popupSize[0] // 2, 
                    offset[1] - popupSize[1] // 2, 
                    200,
                    100
                ), 
            "Purchase",
            20,
            "joystix.otf"
            )
        )
        self.popupElements.append(
            TextBox(
                (
                    offset[0] - popupSize[0] // 2, 
                    offset[1] - popupSize[1] // 2 + 50, 
                    200,
                    100
                ), 
            f"{itemName} for {amount}?",
            20,
            "joystix.otf"
            )
        )
        self.popupElements.append(
            Button(
                (
                    offset[0] - popupSize[0] // 2 + 10, 
                    offset[1] - popupSize[1] // 2 + 100, 
                    80,
                    50
                ),
                15, 
                10, 
                self.BUTTON_COLOR,
                self.FONT_COLOR,
                "YES"
            )
        )
        self.popupElements.append(
            Button(
                (
                    offset[0] - popupSize[0] // 2 + 110, 
                    offset[1] - popupSize[1] // 2 + 100, 
                    80,
                    50
                ),
                15, 
                10, 
                self.BUTTON_COLOR,
                self.FONT_COLOR,
                "NO"
            )
        )