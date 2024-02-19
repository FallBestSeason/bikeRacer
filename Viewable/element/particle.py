import pygame
import math
import random
import os, sys
current_dir = os.path.dirname(__file__)
sys.path.append(current_dir)

class ParticleNode:
    LIFESPAN = 150
    SIZE = 5

    XRANGE = (0, 20)
    YRANGE = (30, 50)
    GRANGE = (8, 12)

    particles = []
    empty = False

    def __init__(self, pos, numParticles):
        self.particles = []
        self.pos = pos

        for i in range(numParticles):
            initAccel = pygame.Vector2(
                random.randint(self.XRANGE[0], self.XRANGE[1]), 
                -random.randint(self.YRANGE[0], self.YRANGE[1])
            )
            self.particles.append(Particle(
                pos,
                self.SIZE,
                self.LIFESPAN,
                initAccel,
                random.randint(self.GRANGE[0], self.GRANGE[1])
            ))

    def draw(self, screen, offset):
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
            
class Particle:
    DECEL = 0.15
    GRAV_ACCEL = 7

    particleColor = (100, 0, 100)

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