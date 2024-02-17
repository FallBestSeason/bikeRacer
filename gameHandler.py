from viewable.mainMenu import MainMenu
from viewable.bikeShop import BikeShop
from viewable.raceInstance import RaceInstance

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

    def event(self, event):
        if event.type == self.pygame.QUIT:
                return False
        elif event.type == self.pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                return self.clicked(self.pygame.mouse.get_pos())
        elif event.type == self.pygame.KEYDOWN:
            if isinstance(self.gui, RaceInstance):
                self.gui.keyDown(event)
        elif event.type == self.pygame.KEYUP:
            if isinstance(self.gui, RaceInstance):
                self.gui.keyUp(event)
        
        #must return true as it's used to check for running
        return True

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
        elif clicked == "GO RACE!":
            self.screen.fill((0, 0, 0))
            self.gui = RaceInstance(self.screenSize)
        elif clicked == "CREDITS":
            return True

        #must return true as it's used to check for running
        return True