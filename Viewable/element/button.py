import pygame
import os, sys
current_dir = os.path.dirname(__file__)
sys.path.append(current_dir)

#abstract instance module, handles data and math for making buttons
#notably has mehtod to check if a click's coordinate is within a button
class Button:
    #init for using button with text
    def __init__(self, rect, fontSize, fontSpacing, bgColor, fontColor, string):
        #take imported data from parent
        self.rect = rect
        self.bgColor = bgColor
        self.string = string

        #generate location and size of text box
        self.textRect = self.generateTextRect(rect, fontSpacing, fontSize)

        #set up resource path for getting files
        resPath = os.path.join(os.path.dirname(os.path.dirname(__file__)), "res\\")

        #set up font object for rendering text
        buttonFont = pygame.font.Font(resPath+"font.ttf", fontSize)
        self.renderedText = buttonFont.render(string, True, fontColor)

    #init for using button with image
    def __init__(self, rect, image, string):
        self.rect = rect
        self.image = image
        self.string = string

    #generates location and size of text box. reduces complexity in init
    def generateTextRect(self, rect, fontSpacing, fontSize):
        return (rect[0] + fontSpacing,
                rect[1] + rect[3] // 2 - fontSize,
                rect[2] - fontSpacing,
                rect[3] - fontSpacing)

    #adds elements of button to backside
    def draw(self, pygame, screen):
        if self.image != '':
            screen.blit(self.image, self.rect)
        else:
            pygame.draw.rect(screen, self.bgColor, self.rect)
            screen.blit(self.renderedText, self.textRect[:2])

    #check if the click position is within the button's bounds
    def checkClicked(self, click):
        buttonX, buttonY = self.rect[:2]
        buttonWidth, buttonHeight = self.rect[2], self.rect[3]
        mouseX, mouseY = click

        if buttonX < mouseX < buttonX + buttonWidth and buttonY < mouseY < buttonY + buttonHeight:
            return True
        return False
