import pygame
from pygame.rect import Rect
import json
import os, sys
current_dir = os.path.dirname(__file__)
sys.path.append(current_dir)
from button import Button

class InventoryManager:
    def __init__(self):
        #gets resouce frolder set up 
        currentDir = os.path.dirname(__file__)
        resPath = os.path.join(currentDir, "..GUI\\res\\")

        #reads dictionary data from text file
        #todo

        #testing data 
        #represent each item in players inventory as element in dictionary
        self.items = [{
            "category": "frame",
            "name": "big block",
            "imagePath": f"{resPath}\\parts\\frame\\bigBlock.png"
        }, {
            "category": "frame",
            "name": "thunderdome",
            "imagePath": f"{resPath}\\parts\\frame\\thunderdome.png"
        }]

        self.write()

    def write(self):
        with open("Inventory\\inventory.json", "w") as outfile: 
            for item in self.items:
                json.dump(item, outfile) 
                outfile.write("\n")