import pygame
import math
import os, sys
current_dir = os.path.dirname(__file__)
sys.path.append(current_dir)

class ParticleNode:
    ARC_SLOPE = 0.05
    ARC_OFFSET_X = 10

    LIFESPAN = 30
    PARTICLE_COLOR = (0, 0, 0)
    PARTICLE_SIZE = 10

    particles = []

    def __init__(self, numParticles, particleLifeSpan):
        self.numParticles = numParticles
        self.particleLifeSpan = particleLifeSpan

        for _ in numParticles:
            newPart = Particle(
                self.PARTICLE_COLOR, 
                self.PARTICLE_SIZE, 
                particleLifeSpan,
                self.ARC_SLOPE,
                self.ARC_OFFSET_X
            )
            self.particles.append(newPart)

    def draw(self, pygame, screen):
        updatedParticles = []
        for particle in self.particles:
            if particle.livedTicks < particle.lifespan:
                updatedParticles.append(particle)
            pygame.draw.rect(screen, self.PARTICLE_COLOR, particle.getCurrentRect())
            
class Particle:
    def __init__(self, color, size, lifespan, arcSlope, arcHeight):
        self.color = color
        self.size = size
        self.lifespan = lifespan
        self.livedTicks = 0
        self.arcSlope = arcSlope
        self.arcHeight = arcHeight

        self.arcStepX = int(2 * math.sqrt(arcHeight * arcSlope) / lifespan)
        self.currentX = 0

    def getCurrentRect(self):
        if self.livedTicks <= self.lifespan:
            self.livedTicks += 1
            return Rect(
                self.arcStepX * self.lifespan, 
                self.arcSlope * (self.currentX ** 2) - self.arcHeight,
                self.size, self.size
            )
        else:
            return Rect(0, 0, 0, 0)