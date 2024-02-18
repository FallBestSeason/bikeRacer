import pygame
import math
import random
import os, sys
current_dir = os.path.dirname(__file__)
sys.path.append(current_dir)

class ParticleNode:

    XSPREAD = (50, 60)
    YSPREAD = (10, 80)

    PARTICLE_COLOR = (61, 92, 92)
    PARTICLE_SIZE = 3

    particles = []

    def __init__(self, numParticles, particleLifeSpan):
        self.numParticles = numParticles
        self.particleLifeSpan = particleLifeSpan

        for _ in range(numParticles):
            self.particles.append(Particle(
                [100, 100], 3, 300,
                [random.randint(self.XSPREAD[0], self.XSPREAD[1]),
                random.randint(self.YSPREAD[0], self.YSPREAD[1])]
            ))

    def draw(self, pygame, screen, offset):
        for particle in self.particles:
            pygame.draw.rect(screen, self.PARTICLE_COLOR, particle.getRect())

    def containsAlive(self):
        for i, particle in enumerate(self.particles):
            if particle.getAlive():
                return True
        return False
            
class Particle:
    maxSpeed = 10
    acceleration = [0, 0]
    deceleration = 1
    gravity = 0.5
    age = 0

    def __init__(self, pos, size, lifeSpan, initAccel):
        self.pos = pos
        self.size = size
        self.lifeSpan = lifeSpan
        self.acceleration[0] = initAccel[0]
        self.acceleration[1] = initAccel[1]

    def updatePhysics(self):
        self.acceleration[0] += -1 if self.acceleration[0] > 0 else 1 if self.acceleration[0] < 0 else 0
        self.acceleration[1] += -1 if self.acceleration[1] > 0 else 1 if self.acceleration[1] < 0 else 0

        #gravity
        self.acceleration[1] += self.gravity

        #update pos from accel
        self.pos[0] += self.acceleration[0]
        self.pos[1] += self.acceleration[1]

        #vibe check speed
        self.acceleration[0] = min(self.maxSpeed, max(-self.maxSpeed, self.acceleration[0]))
        self.acceleration[1] = min(self.maxSpeed, max(-self.maxSpeed, self.acceleration[1]))

        self.age += 1

    def getRect(self):
        self.updatePhysics()
        testRect = [self.pos[0], self.pos[1], self.size, self.size]
        return testRect

    def GetAlive(self):
        if self.age >= self.lifeSpan:
            return False
        return True