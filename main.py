import pygame
import math
import random

class Creature:
    def __init__(self, color, radius, x, y):
        # immutable characteristics
        self.color = color
        self.radius = radius

        # changing stats
        self.x = x
        self.y = y
        self.direction = random.randint(0, 360)
        self.speed = 0
        self.energy = 100
    
    def move(self):
        # calculates updated position
        self.x += math.sin(math.radians(self.direction)) * self.speed
        self.y += math.cos(math.radians(self.direction)) * self.speed

        # updates graphics
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)

class Plant:
    def __init__(self):
        self.x = random.randint(0, screenWidth)
        self.y = random.randint(0, screenHeight)
    
    def draw(self, screen):
        pygame.draw.circle(screen, (15, 200, 50), (self.x, self.y), 5)

# SIMULATION SETUP
pygame.init()
screenWidth, screenHeight = 900, 600
screen = pygame.display.set_mode((screenWidth, screenHeight))
pygame.display.set_caption("Interactive Evolution Simulator")
clock = pygame.time.Clock()

creatures = [Creature((125, 125, 125), 10, random.randint(0, screenWidth), random.randint(0, screenHeight)) for _ in range(20)]
plants = [Plant() for _ in range(50)]

plantRegrow = 0
done = False
while not done:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    screen.fill((255, 255, 255))

    for creature in creatures:
        # creatures randomly update speed and direction
        creature.speed += random.uniform(-1, 1)
        creature.direction += random.uniform(-10, 10)
        creature.move()

        creature.energy -= 1 + creature.speed * 2

        # creatures attempt to eat
        for plant in plants:
            if pygame.math.Vector2(creature.x, creature.y).distance_to((plant.x, plant.y)) < 10:
                creature.energy += 100
                plants.remove(plant)

        if creature.energy < 0:
            creatures.remove(creature)

    plantRegrow += 1
    if plantRegrow == 20:
        plants.append(Plant())
        plantRegrow = 0

    for plant in plants:
        plant.draw(screen)

    clock.tick(60)
    pygame.display.flip()

pygame.quit()