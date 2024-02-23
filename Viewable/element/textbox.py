import pygame
import os, sys
current_dir = os.path.dirname(__file__)
sys.path.append(current_dir)

class TextBox:
    FONT_SPACING = 10
    FONT_COLOR = (0, 0, 0)

    def __init__(self, rect, text, fontSize, fontPath):
        self.rect = rect
        self.text = text
        self.fontSize = fontPath

        self.textRect = (rect[0] + self.FONT_SPACING,
                rect[1] + (rect[3] % fontSize) / 2,
                rect[2] - self.FONT_SPACING,
                rect[3] - self.FONT_SPACING)

        resPath = os.path.join(os.path.dirname(os.path.dirname(__file__)), "res\\")
        font = pygame.font.Font(resPath+fontPath, fontSize)
        self.renderedText = buttonFont.render(text, True, self.FONT_COLOR)

    def draw(self, pygame, screen):
        screen.blit(self.renderedText, self.textRect[:2])