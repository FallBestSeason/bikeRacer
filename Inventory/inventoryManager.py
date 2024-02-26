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
    moneyFilePath = "Inventory/money.json"

    def __init__(self):
        #pulls items from inventory json file
        self.read()

        self.bike = Bike()

        self.readMoney()

    def readMoney(self):
        with open(self.moneyFilePath, "r") as infile:
            self.money = json.load(infile)

    def writeMoney(self):
        with open(self.moneyFilePath, "w") as outfile:
            json.dump(self.money, outfile)

    #reads items dict from file
    def read(self):
        with open(self.itemFilePath, "r") as infile:
            self.items = json.load(infile)

    #writes current content of self.items to json file
    def write(self):
        with open(self.itemFilePath, "w") as outfile:
            outfile.write("[")
            for i, item in enumerate(self.items):
                json.dump(item, outfile)
                if i < len(self.items) - 1:
                    outfile.write(",\n")
            outfile.write("]")

    def updateMoney(self, amount):
        self.money["moneyAmount"] += amount
        self.writeMoney()

    def getMoney(self):
        return self.money["moneyAmount"]

    #updates items dict- element with name, at category.
    def updateItem(self, name, cat, value):
        for i, item in enumerate(self.items):
            if item.get("name") == name:
                print(self.items[i])
                self.items[i][cat] = value
                self.write()

    #adds item to dict, updates file
    def addItem(self, item):
        self.items.append(item)
        self.write()

    #removes item with given name from dict, updates file
    def removeItem(self, name):
        rebuild = []
        for item in self.items:
            if item.get("name") != name:
                rebuild.append(item)
        self.items = rebuild
        self.write()

    #returns named item
    def getItem(self, name):
        for item in self.items:
            if item.get("name") == name:
                return item

    #returns list of dict entries w matching category
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

    #returns sum of weight of parts in bike instance, roudned to 2 decimals
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