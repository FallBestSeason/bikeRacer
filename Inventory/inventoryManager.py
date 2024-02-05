import pygame
from pygame.rect import Rect
import json
import os, sys
current_dir = os.path.dirname(__file__)
sys.path.append(current_dir)

class InventoryManager:

    jsonFilePath = "Inventory/inventory.json"

    def __init__(self):
        #pulls items from inventory json file
        self.updateItems()

    #writes current content of self.items to json file
    def write(self):
        with open(self.jsonFilePath, "w") as outfile:
            outfile.write("[")
            for i, item in enumerate(self.items):
                json.dump(item, outfile)
                if i < len(self.items) - 1:
                    outfile.write(",\n")
            outfile.write("]")
        #always updates items dict to match file
        self.updateItems()

    def updateItems(self):
        #reads dictionary data from json file into self.items
        with open("Inventory\\inventory.json", "r") as infile:
            self.items = json.load(infile)

        #todo remove once not needed for testing
        """
        self.items = [{
            "category": "frame",
            "name": "big block",
            "imagePath": "C:\\Users\\Alex\\Desktop\\pyhton stuff\\bikeRacer\\bikeRacer\\Inventory\\..GUI\\res\\\\parts\\frame\\bigBlock.png"
            }, {
            "category": "frame", 
            "name": "thunderdome", 
            "imagePath": "C:\\Users\\Alex\\Desktop\\pyhton stuff\\bikeRacer\\bikeRacer\\Inventory\\..GUI\\res\\\\parts\\frame\\thunderdome.png"
            }]
        """

    #appends item to self.items, writes file with items
    def addItem(self, cat, name, path):
        self.items.append({
            "category": cat,
            "name": name,
            "filePath": path
        })
        self.write()

    #returns list of dict entries containing same category as passed in
    def getAllInCat(self, cat):
        inCat = []
        for item in self.items:
            if item.get("category") == cat:
               inCat.append(item) 
        return inCat