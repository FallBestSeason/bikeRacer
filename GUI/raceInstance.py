import pygame
from pygame.rect import Rect
import math
import os, sys
current_dir = os.path.dirname(__file__)
sys.path.append(current_dir)
from button import Button
from Inventory.inventoryManager import InventoryManager

class RaceInstance:
    #constants for UI stuff

    #constants for race stuff
    #max speed and accel for player
    PLAYER_SPEED_MAX = 6
    PLAYER_ACCELERATION = 1
    PLAYER_DECELERATION = -0.01
    SKID_DECEL = -0.03
    #rate at which playerLeanAmount is changed
    PLAYER_LEAN_DELTA = 2
    #each range represents a state leanAmount can occupy
    SMALL_LEAN_RANGE = (25, 75)
    LARGE_LEAN_RANGE = (75, 125)
    #offset amounts for rotating player
    PLAYER_SMALL_DELTA_ROTATION = 1
    PLAYER_LARGE_DELTA_ROTATION = 1.5
    PLAYER_SKID_ROTATION = 70
    #paths for player sprites
    PLAYER_SPRITE_PATH_CENTER = "\\player\\player0.png"
    PLAYER_SPRITE_PATH_SMALL = "\\player\\player1.png"
    PLAYER_SPRITE_PATH_LARGE = "\\player\\player2.png"
    PLAYER_SPRITE_PATH_SKID = "\\player\\player3.png"
    BG_SPRITE_PATH = "\\maps\\map1.png"

    #mutable vars
    #arbitrary number, represents range player can lean in
    playerLeanAmount = 0
    #note: rotation utility turns counterclockwise!
    playerRotation = 0
    #current player speed
    playerSpeed = 0.0

    #state of movement
    acceleratingForward = False
    leaningRight = False
    leaningLeft = False
    skidding = False
    skidNotStarted = True
    SkiddingLeft = False

    #represents delta x, y to offset background
    #creates illusion of scrolling world
    camera = (0, 0)

    def __init__(self, screenSize):
        #gets resouce frolder set up 
        currentDir = os.path.dirname(__file__)
        self.resPath = os.path.join(currentDir, "res\\")

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
            self.skidNotStarted = True
            if self.skiddingLeft:
                self.playerRotation += self.PLAYER_SKID_ROTATION
            else:
                self.playerRotation -= self.PLAYER_SKID_ROTATION

    def draw(self, pygame, screen):
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
            playerSprite = pygame.image.load(self.resPath + self.PLAYER_SPRITE_PATH_SMALL)
            self.playerRotation -= self.PLAYER_SMALL_DELTA_ROTATION
        elif -self.SMALL_LEAN_RANGE[0] >= self.playerLeanAmount > -self.SMALL_LEAN_RANGE[1]:
            #slightly leaned left
            playerSprite = pygame.image.load(self.resPath + self.PLAYER_SPRITE_PATH_SMALL)
            playerSprite = pygame.transform.flip(playerSprite, True, False)
            self.playerRotation += self.PLAYER_SMALL_DELTA_ROTATION
        elif self.LARGE_LEAN_RANGE[0] <= self.playerLeanAmount:
            #full leaned right
            playerSprite = pygame.image.load(self.resPath + self.PLAYER_SPRITE_PATH_LARGE)
            self.playerRotation -= self.PLAYER_LARGE_DELTA_ROTATION
        elif -self.LARGE_LEAN_RANGE[0] >= self.playerLeanAmount:
            #full leaned left
            playerSprite = pygame.image.load(self.resPath + self.PLAYER_SPRITE_PATH_LARGE)
            playerSprite = pygame.transform.flip(playerSprite, True, False)
            self.playerRotation += self.PLAYER_LARGE_DELTA_ROTATION
        else:
            #centered 
            playerSprite = pygame.image.load(self.resPath + self.PLAYER_SPRITE_PATH_CENTER)

        #then, accelerate the player forward if applicable
        if self.acceleratingForward and not self.skidding:
            #accelerate
            self.playerSpeed += self.PLAYER_ACCELERATION
        else: #not moving forward, reduce speed
            if self.playerSpeed > 0:
                self.playerSpeed += self.PLAYER_DECELERATION

        #then, check if we are skidding
        if self.skidding:
            #deccelerate
            self.playerSpeed += self.SKID_DECEL
            #change sprite to skid
            playerSprite = pygame.image.load(self.resPath + self.PLAYER_SPRITE_PATH_SKID)
            if not self.skiddingLeft:
                #flips sprite for right skids
                playerSprite = pygame.transform.flip(playerSprite, True, True)

        #speed limit check
        if self.playerSpeed > self.PLAYER_SPEED_MAX:
            self.playerSpeed = self.PLAYER_SPEED_MAX
        elif self.playerSpeed < 0: 
            self.playerSpeed = 0

        #rotate player sprite 
        rotatedSprite = pygame.transform.rotate(playerSprite, self.playerRotation)
        #center it on the existing sprite
        rotatedSprite.get_rect().center = playerSprite.get_rect().center
        playerSprite = rotatedSprite
            
        #update camera with difference in x, y given rotation and speed
        self.cameraDelta = getCameraDelta(self.camera[0], self.camera[1], self.playerRotation, self.playerSpeed)
        self.camera = self.camera[0] + self.cameraDelta[0], self.camera[1] + self.cameraDelta[1]
        
        #draw everything to screen
        #fill w black
        screen.fill((0, 0, 0))

        #add camera to background as "offset"
        self.bgRect = self.bgImage.get_rect()
        self.bgRect.topleft = self.bgRect.top + self.camera[0], self.bgRect.left + self.camera[1]
        #draw bg to screen
        screen.blit(self.bgImage, self.bgRect)

        #set up player rect to be centered on screen
        playerRect = ((self.screenSize[0] // 2) - (playerSprite.get_rect().left // 2),
                      (self.screenSize[1] // 2) - (playerSprite.get_rect().top // 2),
                      #self.PLAYER_SIZE[0], self.PLAYER_SIZE[1])
                       playerSprite.get_rect().width, playerSprite.get_rect().height)
        #draw player sprite to screen
        screen.blit(playerSprite, playerRect)

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