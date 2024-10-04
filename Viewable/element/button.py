import pygame
import os, sys
current_dir = os.path.dirname(__file__)
sys.path.append(current_dir)

from textbox import TextBox

#abstract instance module, handles data and math for making buttons
#notably has mehtod to check if a click's coordinate is within a button
class Button:
    #init for using button with text
    def __init__(self, rect, fontSize, fontSpacing, bgColor, fontColor, string):
        #take imported data from parent
        self.rect = rect
        self.bgColor = bgColor
        self.string = string
        self.textBox = TextBox(rect, string, fontSize, "joystix.otf")

    #adds elements of button to backside
    def draw(self, pygame, screen):
        pygame.draw.rect(screen, self.bgColor, self.rect)
        self.textBox.draw(pygame, screen)

    #check if the click position is within the button's bounds
    def checkClicked(self, click):
        buttonX, buttonY = self.rect[:2]
        buttonWidth, buttonHeight = self.rect[2], self.rect[3]
        mouseX, mouseY = click

        if buttonX < mouseX < buttonX + buttonWidth and buttonY < mouseY < buttonY + buttonHeight:
            return True
        return False