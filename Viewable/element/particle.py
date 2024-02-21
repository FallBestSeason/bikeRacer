import pygame
import math
import random
import os, sys
current_dir = os.path.dirname(__file__)
sys.path.append(current_dir)

class ParticleNode:
    LIFESPAN = 300
    SIZE = 6

    rangeX = [-10, 10]
    rangeY = [10, 20]
    GRANGE = (0, 0)

    particles = []
    empty = False

    def __init__(self, pos, camera, rotation, numParticles):
        self.particles = []
        self.pos = pos
        self.cameraPos = (self.pos[0] - camera[0], self.pos[1] - camera[1])
        minXY = self.rotateRange((self.rangeX[0], self.rangeY[0]), -rotation)
        maxXY = self.rotateRange((self.rangeX[1], self.rangeY[1]), -rotation)
        self.rangeX = [int(minXY[0]), int(maxXY[0])]
        self.rangeY = [int(minXY[0]), int(maxXY[1])]

        for i in range(numParticles):
            if self.rangeX[0] > self.rangeX[1]:
                randX = -random.randint(self.rangeX[1], self.rangeX[0])
            else:
                randX = -random.randint(self.rangeX[0], self.rangeX[1])
            if self.rangeY[0] > self.rangeY[1]:
                randY = -random.randint(self.rangeY[1], self.rangeY[0])
            else:
                randY = -random.randint(self.rangeY[0], self.rangeY[1])

            initAccel = pygame.Vector2(
                randX, 
                randY
            )
            self.particles.append(Particle(
                self.cameraPos,
                self.SIZE,
                self.LIFESPAN,
                initAccel,
                random.randint(self.GRANGE[0], self.GRANGE[1])
            ))

    def draw(self, screen, offset):
        pygame.draw.rect(screen, (100, 0, 0), (self.pos[0], self.pos[1], 2, 2))
        drawnParticles = []
        for particle in self.particles:
            particle.draw(screen, offset)
            particle.lifespan -= 1
            if particle.lifespan >= 0:
                drawnParticles.append(particle)
        self.particles = drawnParticles

    def isNotEmpty(self):
        if not self.particles:
            return False
        return True

    def rotateRange(self, xy, deg):
        #get angle sanitized
        deg -= 90
        deg %= 360
        angleRad = math.radians(deg)

        newX = xy[0] * math.cos(angleRad) - xy[1] * math.sin(angleRad)
        newY = xy[0] * math.sin(angleRad) + xy[1] * math.cos(angleRad)

        return newX, newY
            
class Particle:
    DECEL = 0.15
    GRAV_ACCEL = 5

    particleColor = (85, 92, 96)

    def __init__(self, pos, size, lifespan, initAccel, gravOffset):
        self.pos = pygame.Vector2(pos)
        self.size = size
        self.lifespan = lifespan
        self.accel = pygame.Vector2(initAccel[0], initAccel[1])
        self.gravMax = pos[1] + gravOffset

    def draw(self, screen, offset):
        #do grav if applicable
        if self.pos[1] <= self.gravMax:
            self.pos[1] += self.GRAV_ACCEL
        #update position
        self.pos += self.accel
        #generate rect
        rect = pygame.Rect(
            self.pos[0] + offset[0], 
            self.pos[1] + offset[1],
            self.size, self.size
        )
        #draw
        pygame.draw.rect(screen, self.particleColor, rect)
        #decelerate
        self.accel *= (1 - self.DECEL)