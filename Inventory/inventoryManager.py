import pygame
from pygame.rect import Rect
import json
import os, sys
current_dir = os.path.dirname(__file__)
sys.path.append(current_dir)

class Bike:
    bikeItems = {
        "subframe": "big block subframe",
        "stem": "used alloy stem",
        "bar": "flat",
        "seatpost": "used alloy post",
        "saddle": "powercomp",
        "hubs": "formula track",
        "rims": "alex DH19",
        "tires": "gatorskins",
        "frame": "big block",
        "chainring": "used alloy chainring",
        "chain": "standard chain",
        "crankset": "used alloy crankset",
        "pedals": "flats",
        "front gearing": "46",
        "rear gearing": "17"
    }

    def setPart(self, part):
        self.bikeItems[part.get("category")] = part.get("name")

    def getPartName(self, cat):
        return self.bikeItems[cat]
    
    def getDict(self):
        return self.bikeItems
        
class InventoryManager:

    jsonFilePath = "Inventory/inventory.json"
    itemFilePath = "Inventory/items.json"

    def __init__(self):
        #pulls items from inventory json file
        self.updateItems()

        with open(self.itemFilePath, "r") as infile:
            self.allItems = json.load(infile)

        #sets up current bike object for current config
        self.bike = Bike()

    def updateItems(self):
        #reads dictionary data from json file into self.items
        with open(self.itemFilePath, "r") as infile:
            self.items = json.load(infile)

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
    def addItem(self, cat, name, weight, path):
        self.items.append({
            "category": cat,
            "name": name,
            "weight": weight,
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