import pygame
from pygame.rect import Rect
import json
import os, sys
current_dir = os.path.dirname(__file__)
sys.path.append(current_dir)

class InventoryManager:
    def __init__(self):
        #gets resouce frolder set up 
        currentDir = os.path.dirname(__file__)
        resPath = os.path.join(currentDir, "..GUI\\res\\")

        self.updateItems()

        self.write()

    def write(self):
        with open("Inventory\\inventory.json", "w") as outfile: 
            json.dump(self.items, outfile)
        #always updates items dict to match file
        self.updateItems()

    def updateItems(self):
        #reads dictionary data from text file
        #category: frame, crankset, rim, etc
        #name: name, imagePath: path to image
        with open("Inventory\\inventory.json", "r") as infile:
            self.items = json.load(infile)

    #todo add and remove itemss