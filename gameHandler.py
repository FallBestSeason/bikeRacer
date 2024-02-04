from GUI.mainMenu import MainMenu

class GameHandler:
    def __init__(self):
        self.state = "mainMenu"

    def updateUI(self, pygame, screen, screenSize):
        if self.state == "mainMenu":
            gui = MainMenu(screenSize)
            gui.draw(pygame, screen)
        #todo draw mainmenu screen