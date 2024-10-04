import pygame
from pygame.rect import Rect
import json
import os, sys
current_dir = os.path.dirname(__file__)
sys.path.append(current_dir)

#this file manages the backend of the game
#handles user money, items, unlocks, etc by interacting with json files

#instance class, represents one bike object made up of many parts
class Bike:
    path = "inventory/bike.json"

    def __init__(self):
        self.read()

    def read(self):
        with open(self.path, "r") as infile:
            self.list = json.load(infile)

    def write(self):
        with open(self.path, "w") as outfile:
            json.dump(self.list, outfile)

    def setPart(self, part):
        self.list[part.get("category")] = part.get("name")
        self.write()

    #takes a category and returns the current part
    def getPartName(self, cat):
        return self.list[cat]
    
    def getDict(self):
        return self.list
        
#GUI class
class InventoryManager:
    itemFilePath = "Inventory/items.json"
    moneyFilePath = "Inventory/money.json"

    def __init__(self):
        #pulls items from inventory json file
        self.read()
        self.bike = Bike()
        self.readMoney()

    #reads player's current money from disk
    def readMoney(self):
        with open(self.moneyFilePath, "r") as infile:
            self.money = json.load(infile)

    #updates player's current money on disk
    def writeMoney(self):
        with open(self.moneyFilePath, "w") as outfile:
            json.dump(self.money, outfile)

    #reads items dict from disk
    def read(self):
        with open(self.itemFilePath, "r") as infile:
            self.items = json.load(infile)

    #writes current content of self.items to disk
    def write(self):
        with open(self.itemFilePath, "w") as outfile:
            outfile.write("[")
            for i, item in enumerate(self.items):
                json.dump(item, outfile)
                if i < len(self.items) - 1:
                    outfile.write(",\n")
            outfile.write("]")

    #wrapper to update money easily from other classes
    def updateMoney(self, amount):
        self.money["moneyAmount"] += amount
        self.writeMoney()

    #wrapper to read money easily from other classes
    #! does not read player's money from disk
    def getMoney(self):
        return self.money["moneyAmount"]

    #updates items dict- element with name, at category.
    #changes the selected item on the bike
    def updateItem(self, name, cat, value):
        for i, item in enumerate(self.items):
            if item.get("name") == name:
                print(self.items[i])
                self.items[i][cat] = value
                self.write()

    #adds item to dict, updates file
    #used when the bike does not already have an item in a given slot,
    #this should only be during setup
    def addItem(self, item):
        self.items.append(item)
        self.write()

    #removes item with given name from dict, updates file
    #removes an item from the bike
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

    #returns sum of weight of parts in bike instance, rounded to 2 decimals
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