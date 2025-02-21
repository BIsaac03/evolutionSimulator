import pygame
import pygame.freetype
import math
import random

SCREEN_WIDTH = 900
SCREEN_HEIGHT = 600

FRAME_RATE = 60
STARTING_CREATURES = 20
STARTING_PLANTS = 40

CONSTANT_ENERGY_LOSS = 0.1
ENERGY_LOSS_PER_SPEED = 0.2
ENERGY_NEEDED_TO_REPRODUCE = 120
ENERGY_SPENT_TO_REPRODUCE = 100

TIME_FOR_PLANT_GROWTH = 5
PLANT_ENERGY = 100

# SIMULATION SETUP
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
GAME_FONT = pygame.freetype.SysFont('Comic Sans MS', 30)
pygame.display.set_caption("Interactive Evolution Simulator")
clock = pygame.time.Clock()

class Creature:
    def __init__(self, color, radius, maxSpeed, lifespan, ageOfMaturity, visionDistance, peripheralVision, x, y):
        # immutable characteristics
        self.color = color
        self.radius = radius
        self.maxSpeed = maxSpeed
        self.lifespan = lifespan
        self.ageOfMaturity = ageOfMaturity
        self.visionDistance = visionDistance
        self.pereipheralVision = peripheralVision

        # changing stats
        self.x = x
        self.y = y
        self.direction = random.randint(0, 360)
        self.speed = 0
        self.energy = 100
        self.age = 0
        self.plantsInSight = []
    
    def move(self):
        # calculates updated position
        self.x += math.sin(math.radians(self.direction)) * self.speed
        self.y += math.cos(math.radians(self.direction)) * self.speed

        # keeps creature on screen
        self.x = max(0, min(SCREEN_WIDTH, self.x))
        self.y = max(0, min(SCREEN_HEIGHT, self.y))

        # updates graphics
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)
        pygame.draw.line(screen, (20, 20, 20), (int(self.x), int(self.y)), (int(self.x + self.radius * math.sin(math.radians(self.direction))), int(self.y + self.radius * math.cos(math.radians(self.direction)))))

    def reproduce(self):
        return Creature((max(0, min(255, self.color[0] + random.randint(-10, 10))), 
                        max(0, min(255, self.color[1] + random.randint(-10, 10))), 
                        max(0, min(255, self.color[2] + random.randint(-10, 10)))), 
                        self.radius + random.randint(-1, 1),
                        self.maxSpeed + random.randint(-1, 1),
                        self.lifespan + random.randint(-20, 20), 
                        self.ageOfMaturity + random.randint(-20, 20), 
                        self.visionDistance + random.randint(-20, 20), 
                        self.pereipheralVision + random.randint(-10, 10), 
                        self.x, self.y)

    def displayDetails(self):
        GAME_FONT.render_to(screen, (100, 100), "Age: " + str(int(self.age)), (40, 40, 40))
        GAME_FONT.render_to(screen, (100, 150), "Lifespan: " + str(int(self.lifespan)), (40, 40, 40))
        GAME_FONT.render_to(screen, (100, 200), "Radius: " + str(int(self.radius)), (40, 40, 40))
        GAME_FONT.render_to(screen, (100, 250), "Speed: " + str(int(self.speed)), (40, 40, 40))
        GAME_FONT.render_to(screen, (100, 300), "Max Speed: " + str(int(self.maxSpeed)), (40, 40, 40))
        GAME_FONT.render_to(screen, (100, 400), "Plants in Sight: " + str(self.plantsInSight), (40, 40, 40))

class Plant:
    def __init__(self):
        self.x = random.randint(0, SCREEN_WIDTH)
        self.y = random.randint(0, SCREEN_HEIGHT)
    
    def draw(self, screen):
        pygame.draw.circle(screen, (15, 200, 50), (self.x, self.y), 5)

creatures = [Creature((125, 125, 125), 10, 3, 300, 100, 50, 20, random.randint(0, SCREEN_WIDTH), random.randint(0, SCREEN_HEIGHT)) for _ in range(STARTING_CREATURES)]
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
        creature.plantsInSight.clear()

        creature.age += 1
        creature.energy -= (CONSTANT_ENERGY_LOSS + creature.speed * ENERGY_LOSS_PER_SPEED)

        # creatures attempt to eat
        for plant in plants:
            if pygame.math.Vector2(creature.x, creature.y).distance_to((plant.x, plant.y)) <= creature.radius:
                creature.energy += PLANT_ENERGY
                plants.remove(plant)

            # finds plants within creature's vision
            elif pygame.math.Vector2(creature.x, creature.y).distance_to((plant.x, plant.y)) <= creature.visionDistance:
                if pygame.math.Vector2(creature.x, creature.y).angle_to((plant.x, plant.y)) % 360 - creature.direction % 360 <= creature.pereipheralVision / 2:
                    creature.plantsInSight.append((plant.x, plant.y))

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