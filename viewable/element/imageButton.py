import pygame
import os, sys
current_dir = os.path.dirname(__file__)
sys.path.append(current_dir)

#abstract instance module, handles data and math for making buttons with images on them
#very similar to button.py, but overloading increased complexity too much
class ImageButton:
    #init for using button with image
    def __init__(self, rect, image, string):
        self.rect = rect
        self.image = image
        self.string = string

    def draw(self, pygame, screen):
        if self.image != '':
                screen.blit(self.image, self.rect)

    #check if the click position is within the button's bounds
    def checkClicked(self, click):
        buttonX, buttonY = self.rect[:2]
        buttonWidth, buttonHeight = self.rect[2], self.rect[3]
        mouseX, mouseY = click

        if buttonX < mouseX < buttonX + buttonWidth and buttonY < mouseY < buttonY + buttonHeight:
            return True
        return False