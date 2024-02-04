import pygame
import os, sys
current_dir = os.path.dirname(__file__)
sys.path.append(current_dir)

class Button:
    def __init__(self, rect, fontSize, fontSpacing, bgColor, fontColor, string):
        #take imported data from parent
        self.rect = rect
        self.bgColor = bgColor
        self.string = string

        #generate location and size of text box
        self.textRect = self.generateTextRect(rect, fontSpacing, fontSize)

        #set up resource path for getting files
        resPath = os.path.join(os.path.dirname(__file__), "res\\")

        #set up font object for rendering text
        buttonFont = pygame.font.Font(resPath+"font.ttf", fontSize)
        self.renderedText = buttonFont.render(string, True, fontColor)

    def draw(self, pygame, screen):
        pygame.draw.rect(screen, self.bgColor, self.rect)
        screen.blit(self.renderedText, self.textRect[:2])

    #generates location and size of text box
    def generateTextRect(self, rect, fontSpacing, fontSize):
        return (rect[0] + fontSpacing,
                rect[1] + rect[3] // 2 - fontSize,
                rect[2] - fontSpacing,
                rect[3] - fontSpacing)

    #Check if the click position is within the button's bounds, returns text on button
    def checkClicked(self, click):
        buttonX, buttonY = self.rect[:2]
        buttonWidth, buttonHeight = self.rect[2], self.rect[3]
        mouseX, mouseY = click

        if buttonX < mouseX < buttonX + buttonWidth and buttonY < mouseY < buttonY + buttonHeight:
            return True
        return False
