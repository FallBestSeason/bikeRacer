import pygame
from pygame.rect import Rect
import json
import os, sys
current_dir = os.path.dirname(__file__)
sys.path.append(current_dir)

class Bike:
    items = {
        "frame": "big block",
        "subframe": "big block subframe",
        "stem": "",
        "bar": "",
        "tape": "",
        "saddle": "",
        "seatpost": "",
        "crankset": "",
        "chainring": "",
        "chains": "",
        "pedals": "",
        "cog": "",
        "hubs": "",
        "spokes": "",
        "rims": "",
        "tires": "",
    }

    def setPart(self, part):
        self.items[part.get("category")] = part.get("name")

    def getPartName(self, cat):
        return self.items[cat]
        

class InventoryManager:

    jsonFilePath = "Inventory/inventory.json"
    itemFilePath = "Inventory/items.json"

    def __init__(self):
        #pulls items from inventory json file
        self.updateItems()

        with open(self.itemFilePath, "r") as infile:
            self.allItems = json.load(infile)
        #self.addItem(self.getAllItemByName("big block subframe"))
        #self.addItem(self.getAllItemByName("thunderdome subframe"))

        #sets up current bike object for current config
        self.bike = Bike()

    def updateItems(self):
        #reads dictionary data from json file into self.items
        with open(self.jsonFilePath, "r") as infile:
            self.items = json.load(infile)

        #todo remove once not needed for testing
        """
        self.items = [{
            "category": "frame",
            "name": "big block",
            "imagePath": "parts\\frame\\bigBlock.png"
            }, {
            "category": "frame", 
            "name": "thunderdome", 
            "imagePath": "\\parts\\frame\\thunderdome.png"
            }]
        """

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

    #appends item to self.items, writes file with items
    def addItem(self, cat, name, path):
        self.items.append({
            "category": cat,
            "name": name,
            "filePath": path
        })
        self.write()

    def addItem(self, item):
        self.items.append(item)
        self.write()

    #removes item with given name
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

    def getSubFrame(self, frameName):
        for item in self.items:
            if f"{frameName} subframe" == item.get("name"):
                return item