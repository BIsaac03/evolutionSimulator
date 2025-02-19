import pygame
import pygame.freetype
import math
import random

class Creature:
    def __init__(self, color, radius, maxSpeed, x, y):
        # immutable characteristics
        self.color = color
        self.radius = radius
        self.maxSpeed = maxSpeed

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

        # keeps creature on screen
        self.x = max(0, min(screenWidth, self.x))
        self.y = max(0, min(screenHeight, self.y))

        # updates graphics
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)
    
    def displayDetails(self):
        GAME_FONT.render_to(screen, (100, 100), str(int(self.energy)), (40, 40, 40))

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

creatures = [Creature((125, 125, 125), 10, 3, random.randint(0, screenWidth), random.randint(0, screenHeight)) for _ in range(20)]
plants = [Plant() for _ in range(50)]

FRAME_RATE = 60
GAME_FONT = pygame.freetype.SysFont('Comic Sans MS', 30)
plantRegrow = 0
slowed = False
done = False
while not done:

    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            done = True

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                slowed = not slowed
                if slowed:
                    FRAME_RATE = 3
                else: FRAME_RATE = 60

    screen.fill((255, 255, 255))

    for creature in creatures:
        
        if pygame.Vector2(pygame.mouse.get_pos()).distance_to(pygame.Vector2(creature.x, creature.y)) < creature.radius:
                creature.displayDetails()

        # creatures randomly update speed and direction
        creature.speed = max(0, min (creature.speed + random.uniform(-1, 1), creature.maxSpeed))
        creature.direction += random.uniform(-10, 10)
        creature.move()

        creature.energy -= (0.1 + creature.speed * 0.2)

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

    clock.tick(FRAME_RATE)
    pygame.display.flip()

pygame.quit()