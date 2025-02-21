import pygame
import pygame.freetype
import math
import random

SCREEN_WIDTH = 900
SCREEN_HEIGHT = 600
GAME_FONT = pygame.freetype.SysFont('Comic Sans MS', 30)

FRAME_RATE = 60
STARTING_CREATURES = 7
STARTING_PLANTS = 5

CONSTANT_ENERGY_LOSS = 0.1
ENERGY_LOSS_PER_SPEED = 0.2
ENERGY_NEEDED_TO_REPRODUCE = 120
ENERGY_SPENT_TO_REPRODUCE = 100

TIME_FOR_PLANT_GROWTH = 50
PLANT_ENERGY = 100
DISTANCE_TO_EAT = 10

class Creature:
    def __init__(self, color, radius, maxSpeed, lifespan, ageOfMaturity, x, y):
        # immutable characteristics
        self.color = color
        self.radius = radius
        self.maxSpeed = maxSpeed
        self.lifespan = lifespan
        self.ageOfMaturity = ageOfMaturity

        # changing stats
        self.x = x
        self.y = y
        self.direction = random.randint(0, 360)
        self.speed = 0
        self.energy = 100
        self.age = 0
    
    def move(self):
        # calculates updated position
        self.x += math.sin(math.radians(self.direction)) * self.speed
        self.y += math.cos(math.radians(self.direction)) * self.speed

        # keeps creature on screen
        self.x = max(0, min(SCREEN_WIDTH, self.x))
        self.y = max(0, min(SCREEN_HEIGHT, self.y))

        # updates graphics
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)
    
    def reproduce(self):
        return Creature(self.color, self.radius, self.maxSpeed, self.lifespan, self.ageOfMaturity, self.x, self.y)
    
    def displayDetails(self):
        GAME_FONT.render_to(screen, (100, 100), str(int(self.energy)), (40, 40, 40))
        GAME_FONT.render_to(screen, (100, 200), str(int(self.age)), (40, 40, 40))

class Plant:
    def __init__(self):
        self.x = random.randint(0, SCREEN_WIDTH)
        self.y = random.randint(0, SCREEN_HEIGHT)
    
    def draw(self, screen):
        pygame.draw.circle(screen, (15, 200, 50), (self.x, self.y), 5)

# SIMULATION SETUP
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Interactive Evolution Simulator")
clock = pygame.time.Clock()

creatures = [Creature((125, 125, 125), 10, 3, 300, 100, random.randint(0, SCREEN_WIDTH), random.randint(0, SCREEN_HEIGHT)) for _ in range(STARTING_CREATURES)]
plants = [Plant() for _ in range(STARTING_PLANTS)]

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

        creature.age += 1
        creature.energy -= (CONSTANT_ENERGY_LOSS + creature.speed * ENERGY_LOSS_PER_SPEED)

        # creatures attempt to eat
        for plant in plants:
            if pygame.math.Vector2(creature.x, creature.y).distance_to((plant.x, plant.y)) < DISTANCE_TO_EAT:
                creature.energy += PLANT_ENERGY
                plants.remove(plant)

        # kills starving and old creatures
        if creature.energy < 0 or creature.age > creature.lifespan:
            creatures.remove(creature)

        # creatures attempt to reproduce
        if creature.energy > ENERGY_NEEDED_TO_REPRODUCE and creature.age > creature.ageOfMaturity:
            creature.energy -= ENERGY_SPENT_TO_REPRODUCE
            child = creature.reproduce()
            creatures.append(child)

    plantRegrow += 1
    if plantRegrow == TIME_FOR_PLANT_GROWTH:
        plants.append(Plant())
        plantRegrow = 0

    for plant in plants:
        plant.draw(screen)

    clock.tick(FRAME_RATE)
    pygame.display.flip()

pygame.quit()