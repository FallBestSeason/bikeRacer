import pygame
from pygame.rect import Rect
import math
import os, sys
current_dir = os.path.dirname(__file__)
sys.path.append(current_dir)
from particle import ParticleNode
from inventory.inventoryManager import InventoryManager

class RaceInstance:
    #constants for UI stuff
    DEBUG_ENABLED = True

    #constants for race stuff
    SKID_BOOST_TIME = 30
    SKID_BOOST_MAX = 12
    SKID_BOOST_ACCEL = 0.4
    #max speed and accel for player
    PLAYER_SPEED_MAX = 8
    PLAYER_ACCELERATION = 0.1
    PLAYER_DECELERATION = -0.05
    SKID_DECEL = -0.03
    #rate at which playerLeanAmount is changed
    PLAYER_LEAN_DELTA = 4.5
    SMALL_LEAN_RANGE = (25, 75)
    LARGE_LEAN_RANGE = (75, 125)
    #offset amounts for rotating player
    PLAYER_SMALL_DELTA_ROTATION = 1
    PLAYER_LARGE_DELTA_ROTATION = 1.5
    PLAYER_SKID_ROTATION = 90
    #paths for player sprites
    PLAYER_SPRITE_PATH_CENTER = "\\player\\player0.png"
    PLAYER_SPRITE_PATH_SMALL = "\\player\\player1.png"
    PLAYER_SPRITE_PATH_LARGE = "\\player\\player2.png"
    PLAYER_SPRITE_PATH_SKID = "\\player\\player3.png"
    BG_SPRITE_PATH = "\\maps\\map1.png"

    #mutable vars
    debugStrings = []
    particleNodes = []

    #arbitrary number, represents range player can lean in
    playerLeanAmount = 0
    #note: rotation utility turns counterclockwise!
    playerRotation = 0
    playerSpeed = 0.0
    playerSprite = ''

    #state of movement
    acceleratingForward = False
    leaningRight = False
    leaningLeft = False
    skidding = False
    skidNotStarted = True
    SkiddingLeft = False
    skidBoostTimer = 0

    #represents delta x, y to offset background
    camera = (0, 0)

    def __init__(self, screenSize):
        #gets resouce frolder set up 
        currentDir = os.path.dirname(__file__)
        self.resPath = os.path.join(currentDir, "res\\")

        #set up font for debug
        if self.DEBUG_ENABLED:
            self.debugFont = pygame.font.Font(self.resPath+"font.ttf", 10)

        #import screensize from method
        self.screenSize = screenSize

        #set up background image
        self.bgImage = pygame.image.load(self.resPath + self.BG_SPRITE_PATH)

    #handles key presses
    def keyDown(self, event):
        if event.key == pygame.K_w: #w pressed
            self.acceleratingForward = True
        if event.key == pygame.K_d: #d pressed
            self.leaningRight = True
        if event.key == pygame.K_a: #a pressed
            self.leaningLeft = True
        if event.key == pygame.K_SPACE: #space pressed
            self.skidding = True
            self.skidNotStarted = False
            if self.leaningLeft:
                self.skiddingLeft = True
            else:
                self.skiddingLeft = False

    #handles key releases
    def keyUp(self, event):
        if event.key == pygame.K_w: #w released
            self.acceleratingForward = False
        if event.key == pygame.K_d: #d released
            self.leaningRight = False
        if event.key == pygame.K_a: #a released
            self.leaningLeft = False
        if event.key == pygame.K_SPACE: #space released
            self.skidding = False
            if self.skiddingLeft:
                self.playerRotation += self.PLAYER_SKID_ROTATION
            else:
                self.playerRotation -= self.PLAYER_SKID_ROTATION

    def draw(self, pygame, screen, dTime):
        self.updatePlayer()
        self.updateDebug(dTime)
        
        #fill w black
        screen.fill((40, 40, 40))

        #add camera to background as "offset"
        self.bgRect = self.bgImage.get_rect()
        self.bgRect.topleft = self.bgRect.top + self.camera[0], self.bgRect.left + self.camera[1]

        #draw background to screen
        screen.blit(self.bgImage, self.bgRect)

        self.particleNodes.append(ParticleNode((640 - self.camera[0], 360 - self.camera[1]), 10))

        #draw particles to screen
        drawnNodes = []
        for node in self.particleNodes:
            if node.isNotEmpty():
                drawnNodes.append(node)
                node.draw(screen, self.camera)
        self.particleNodes = drawnNodes

        #draw player to screen
        screen.blit(self.playerSprite, self.playerRect)

        #draw debug elements to screen
        debugOffset = 0
        for line in self.debugStrings:
            renderedLine = self.debugFont.render(line, True, (0, 0, 0))
            debugRect = (0, debugOffset, 100, 10)
            screen.blit(renderedLine, debugRect)
            debugOffset += 12
            
    def updateDebug(self, dTime):
        self.debugStrings = []
        self.debugStrings.append(f"speed: {round(self.playerSpeed, 2)}")
        self.debugStrings.append(f"playerLean: {self.playerLeanAmount}")
        self.debugStrings.append(f"boostTimer: {self.skidBoostTimer}")
        self.debugStrings.append(f"particleNodes: {len(self.particleNodes)}")
        self.debugStrings.append(f"frameTime: {dTime}")

    #updates player rotation and sprite given the current state vars
    def updatePlayer(self):
        #do stuff based on state from checking keys
        #first, increment or decrement player lean
        if self.leaningRight:
            self.playerLeanAmount += self.PLAYER_LEAN_DELTA
        elif self.leaningLeft:
            self.playerLeanAmount -= self.PLAYER_LEAN_DELTA
        else: #not pressing lean key, decrease lean amount
            if self.playerLeanAmount > 0:
                self.playerLeanAmount -= 2 * self.PLAYER_LEAN_DELTA
            if self.playerLeanAmount < 0:
                self.playerLeanAmount += 2 * self.PLAYER_LEAN_DELTA

        #make sure lean hasn't escaped good range
        if self.playerLeanAmount > self.LARGE_LEAN_RANGE[1]:
            self.playerLeanAmount = self.LARGE_LEAN_RANGE[1]
        elif self.playerLeanAmount < -self.LARGE_LEAN_RANGE[1]:
            self.playerLeanAmount = -self.LARGE_LEAN_RANGE[1]

        #next, if lean is within ranges, rotate + update player sprite
        if self.SMALL_LEAN_RANGE[0] <= self.playerLeanAmount < self.SMALL_LEAN_RANGE[1]:
            #slightly leaned right
            self.playerSprite = pygame.image.load(self.resPath + self.PLAYER_SPRITE_PATH_SMALL)
            self.playerRotation -= self.PLAYER_SMALL_DELTA_ROTATION
        elif -self.SMALL_LEAN_RANGE[0] >= self.playerLeanAmount > -self.SMALL_LEAN_RANGE[1]:
            #slightly leaned left
            self.playerSprite = pygame.image.load(self.resPath + self.PLAYER_SPRITE_PATH_SMALL)
            self.playerSprite = pygame.transform.flip(self.playerSprite, True, False)
            self.playerRotation += self.PLAYER_SMALL_DELTA_ROTATION
        elif self.LARGE_LEAN_RANGE[0] <= self.playerLeanAmount:
            #full leaned right
            self.playerSprite = pygame.image.load(self.resPath + self.PLAYER_SPRITE_PATH_LARGE)
            self.playerRotation -= self.PLAYER_LARGE_DELTA_ROTATION
        elif -self.LARGE_LEAN_RANGE[0] >= self.playerLeanAmount:
            #full leaned left
            self.playerSprite = pygame.image.load(self.resPath + self.PLAYER_SPRITE_PATH_LARGE)
            self.playerSprite = pygame.transform.flip(self.playerSprite, True, False)
            self.playerRotation += self.PLAYER_LARGE_DELTA_ROTATION
        else: #centered 
            self.playerSprite = pygame.image.load(self.resPath + self.PLAYER_SPRITE_PATH_CENTER)

        #then, accelerate the player
        if self.acceleratingForward and not self.skidding: #accelerate
            self.playerSpeed += self.PLAYER_ACCELERATION
        else: #not moving forward, reduce speed slightly
            if self.playerSpeed > 0:
                self.playerSpeed += self.PLAYER_DECELERATION

        #if we are skidding, update sprite and player movement
        if self.skidding:
            self.playerSpeed += self.SKID_DECEL
            #change sprite to skid
            self.playerSprite = pygame.image.load(self.resPath + self.PLAYER_SPRITE_PATH_SKID)
            self.playerSprite = pygame.transform.flip(self.playerSprite, False, True)
            if not self.skiddingLeft: #flips sprite for right skids
                self.playerSprite = pygame.transform.flip(self.playerSprite, True, False)
            #set timer for skid speed boost
            self.skidBoostTimer = 30

        #speed limit check
        if self.skidBoostTimer > 0: #we are skidding
            if self.playerSpeed > self.SKID_BOOST_MAX:
                self.playerSpeed = self.SKID_BOOST_MAX
            elif self.playerSpeed < 0: 
                self.playerSpeed = 0
            self.skidBoostTimer -= 1
        else: #we are not skidding
            if self.playerSpeed > self.PLAYER_SPEED_MAX:
                self.playerSpeed = self.PLAYER_SPEED_MAX
            elif self.playerSpeed < 0: 
                self.playerSpeed = 0

        #rotate player sprite and maintain position
        rotatedSprite = pygame.transform.rotate(self.playerSprite, self.playerRotation)
        rotatedSprite.get_rect().center = self.playerSprite.get_rect().center
        self.playerSprite = rotatedSprite
            
        #update camera with difference in x, y given rotation and speed
        self.cameraDelta = getCameraDelta(self.camera[0], self.camera[1], self.playerRotation, self.playerSpeed)
        self.camera = self.camera[0] + self.cameraDelta[0], self.camera[1] + self.cameraDelta[1]

        #set up player rect to be centered on screen
        self.playerRect = ((self.screenSize[0] // 2) - (self.playerSprite.get_rect().left // 2),
                      (self.screenSize[1] // 2) - (self.playerSprite.get_rect().top // 2),
                       self.playerSprite.get_rect().width, self.playerSprite.get_rect().height)

def getCameraDelta(x, y, angle, length):
    #get angle sanitized
    angle -= 90
    angle %= 360
    angleRad = math.radians(angle)

    #crunch distance to endpoint of theoretical line
    deltaX = length * math.cos(angleRad)
    deltaY = length * math.sin(angleRad)

    #return these offsets as a tuple
    return deltaX, -deltaY