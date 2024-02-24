import pygame
from pygame.rect import Rect
import json
import os, sys
current_dir = os.path.dirname(__file__)
sys.path.append(current_dir)

#instance class, represents one bike object
class Bike:
    #category and name of items in default bike
    bikeItems = {
        "subframe": "big block subframe",
        "stem": "oem stem",
        "bar": "flat",
        "seatpost": "oem post",
        "saddle": "powercomp",
        "hubs": "formula track",
        "rims": "alex DH19",
        "tires": "gatorskins",
        "frame": "big block",
        "chainring": "oem ring",
        "chain": "1/8th\" chain",
        "crankset": "oem cranks",
        "pedals": "flats",
        "front gearing": "46",
        "rear gearing": "17"
    }

    def setPart(self, part):
        self.bikeItems[part.get("category")] = part.get("name")

    #takes a category and returns the current part
    def getPartName(self, cat):
        return self.bikeItems[cat]
    
    def getDict(self):
        return self.bikeItems
        
#GUI class
class InventoryManager:
    itemFilePath = "Inventory/items.json"

    def __init__(self):
        #pulls items from inventory json file
        self.updateItems()

        with open(self.itemFilePath, "r") as infile:
            self.allItems = json.load(infile)

        #sets up current bike object for current config
        self.bike = Bike()

        self.money = 1000

    #updates items dict with document containing all items and attributes
    def updateItems(self):
        with open(self.itemFilePath, "r") as infile:
            self.items = json.load(infile)

    #updates items dict- element with name, at category.
    def updateItem(self, name, cat, value):
        for i, item in enumerate(self.items):
            if item.get("name") == name:
                print(self.items[i])
                self.items[i][cat] = value
                self.write()

    #writes current content of self.items to json file
    def write(self):
        with open(self.itemFilePath, "w") as outfile:
            outfile.write("[")
            for i, item in enumerate(self.items):
                json.dump(item, outfile)
                if i < len(self.items) - 1:
                    outfile.write(",\n")
            outfile.write("]")
        #always updates items dict to match file
        self.updateItems()

    #adds item to dict and updates document with dict
    def addItem(self, item):
        self.items.append(item)
        self.write()

    #removes item with given name from dict and updates doc
    def removeItem(self, name):
        rebuild = []
        for item in self.items:
            if item.get("name") != name:
                rebuild.append(item)
        self.items = rebuild
        self.write()

    #returns given item within inventory
    def getItem(self, name):
        for item in self.items:
            if item.get("name") == name:
                return item

    #returns item reference from list of all items given name
    def getAllItemByName(self, name):
        for item in self.allItems:
            if item.get("name") == name:
                return item

    #returns list of dict entries containing same category as passed in
    def getAllInCat(self, cat):
        inCat = []
        for item in self.items:
            if item is not None and item.get("category") == cat:
               inCat.append(item) 
        return inCat

    #returns subframe. used for drawing 2 layered effect.
    def getSubFrame(self, frameName):
        for item in self.items:
            if f"{frameName} subframe" == item.get("name"):
                return item

    #returns sum of parts in bike instance
    def getWeight(self):
        weight = 0
        bikeDict = self.bike.getDict()
        for name in bikeDict:
            if name != '':
                itemName = bikeDict.get(name)
                for item in self.items:
                    if item.get("name") == itemName:
                        weight += item.get("weight")
        return round(weight, 2)