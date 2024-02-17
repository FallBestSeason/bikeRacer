import pygame
import math
import random
import os, sys
current_dir = os.path.dirname(__file__)
sys.path.append(current_dir)

class ParticleNode:
    ARC_SLOPE = 0.005
    ARC_OFFSET_X = 100

    ARC_SLOPE_RAND_RANGE = (-0.002, 0.002)
    ARC_OFFSET_RAND_RANGE = (-20, 20)

    PARTICLE_COLOR = (0, 0, 0)
    PARTICLE_SIZE = 10

    particles = []

    def __init__(self, numParticles, particleLifeSpan):
        self.numParticles = numParticles
        self.particleLifeSpan = particleLifeSpan

        for _ in range(numParticles):
            newPart = Particle(
                self.PARTICLE_COLOR, 
                self.PARTICLE_SIZE, 
                particleLifeSpan,
                self.ARC_SLOPE + random.uniform(
                    self.ARC_SLOPE_RAND_RANGE[0],
                    self.ARC_SLOPE_RAND_RANGE[1]
                ),
                self.ARC_OFFSET_X + random.uniform(
                    self.ARC_OFFSET_RAND_RANGE[0],
                    self.ARC_OFFSET_RAND_RANGE[1]
                )
            )
            self.particles.append(newPart)

    def draw(self, pygame, screen, offset):
        updatedParticles = []
        for particle in self.particles:
            if particle.livedTicks < particle.lifespan:
                updatedParticles.append(particle)
            test = particle.getCurrentRect()
            test[0] += offset[0]
            test[1] += offset[1]
            pygame.draw.rect(screen, self.PARTICLE_COLOR, test)
        self.particles = updatedParticles
            
class Particle:
    def __init__(self, color, size, lifespan, arcSlope, arcHeight):
        self.color = color
        self.size = size
        self.lifespan = lifespan
        self.livedTicks = 1
        self.arcSlope = arcSlope
        self.arcHeight = arcHeight

        xWidth = 2 * (math.sqrt(arcHeight) / math.sqrt(arcSlope))
        self.xStep = xWidth / lifespan
 
    def getCurrentRect(self):
        currentX = self.livedTicks * self.xStep
        self.livedTicks += 1
        return [
            currentX,
            ((currentX ** 2) * self.arcSlope) + self.arcHeight,
            self.size, self.size
        ]