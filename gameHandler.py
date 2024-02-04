from GUI.mainMenu import MainMenu

#state handler class
#instances GUI classes as self.gui and updates this state based on user input
class GameHandler:
    def __init__(self, screenSize):
        self.state = "mainMenu"
        self.gui = MainMenu(screenSize)

    def draw(self, pygame, screen):
        if self.state == "mainMenu":
            self.gui.draw(pygame, screen)

    def clicked(self, click):
        clicked = self.gui.buttonClickCheck(click)
        if clicked == "QUIT":
            return False
        elif clicked == "ENTER SHOP":
            self.state = "shop"
        elif clicked == "CREDITS":
            self.state = "credits"

        #must return true as it's used to check for running
        return True