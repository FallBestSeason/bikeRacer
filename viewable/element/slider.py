import pygame
from pygame import Rect
import os, sys
current_dir = os.path.dirname(__file__)
sys.path.append(current_dir)

#abstract instance module
#used to represent slider in GUI class
class Slider:
    #colors
    BG_COLOR = (80, 80, 80)
    FG_COLOR = (120, 120, 120)
    FILL_COLOR = (68, 106, 175)

    def __init__(self, bgRect, padding, minVal, maxVal, init):
        self.bgRect = bgRect
        self.padding = padding
        self.min = minVal
        self.max = maxVal
        self.init = init

        self.foregroundBox = self.generateForegroundBox(bgRect, padding)
        self.fillBox = self.generateFillBox(self.foregroundBox, minVal, maxVal, init)

    #returns rect that is smaller than one passed in by amount padding on each side
    def generateForegroundBox(self, rect, padding):
        return Rect(
            rect.left + padding,
            rect.top + padding,
            rect.width - 2 * padding,
            rect.height - 2 * padding
        )

    #returns rect representing value in slider
    def generateFillBox(self, rect, minVal, maxVal, val):
        return Rect(
            rect.left, rect.top,
            rect.width * ((val - minVal) / (maxVal - minVal)),
            rect.height
        )

    #update held value in slider
    def update(self, val):
        self.fillBox = self.generateFillBox(self.foregroundBox, self.min, self.max, val)

    #draws all boxes to screen
    def draw(self, pygame, screen):
        pygame.draw.rect(screen, self.BG_COLOR, self.bgRect)
        pygame.draw.rect(screen, self.FG_COLOR, self.foregroundBox)
        pygame.draw.rect(screen, self.FILL_COLOR, self.fillBox)