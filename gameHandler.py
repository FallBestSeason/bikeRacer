from GUI.mainMenu import MainMenu
from GUI.bikeShop import BikeShop

#state handler class
#instances GUI classes as self.gui and updates this state based on user input
class GameHandler:
    def __init__(self, screenSize, pygame, screen):
        self.gui = MainMenu(screenSize)
        self.screenSize = screenSize
        self.pygame = pygame
        self.screen = screen

    def draw(self):
        self.gui.draw(self.pygame, self.screen)


    def clicked(self, click):
        clicked = self.gui.buttonClickCheck(click)
        if clicked == "QUIT":
            return False
        elif clicked == "ENTER SHOP":
            self.screen.fill((0, 0, 0))
            self.gui = BikeShop(self.screenSize)
        elif clicked == "BACK TO MENU":
            self.screen.fill((0, 0, 0))
            self.gui = MainMenu(self.screenSize)
        elif clicked == "CREDITS":
            return True

        #must return true as it's used to check for running
        return True