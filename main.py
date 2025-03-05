import NN

import pygame
import pygame.freetype
import math
import random

SCREEN_WIDTH = 900
SCREEN_HEIGHT = 600

FRAME_RATE = 60
STARTING_CREATURES = 300
STARTING_PLANTS = 70

ORIGINAL_RADIUS = 10
ORIGINAL_MAX_SPEED = 3
ORIGINAL_LIFESPAN = 500
ORIGINAL_AGE_OF_MATURITY = 200
ORIGINAL_VISION_DISTANCE = 150
ORIGINAL_PERIPHERAL_VISION = 360
ORIGINAL_MAX_ENERGY = 500 
CONSTANT_ENERGY_LOSS = 0.05
ENERGY_LOSS_PER_SPEED = 0.1
ENERGY_NEEDED_TO_REPRODUCE = 300
ENERGY_SPENT_TO_REPRODUCE = 200
ENERGY_AT_BIRTH = 150

TIME_FOR_PLANT_GROWTH = 4
PLANT_ENERGY = 200

# SIMULATION SETUP
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
GAME_FONT = pygame.freetype.SysFont('Comic Sans MS', 30)
pygame.display.set_caption("Interactive Evolution Simulator")
clock = pygame.time.Clock()

class Creature:
    def __init__(self, color, radius, maxSpeed, lifespan, ageOfMaturity, visionDistance, peripheralVision, maxEnergy, movementModelWeights, x, y,):
        # immutable characteristics
        self.color = color
        self.radius = radius
        self.maxSpeed = maxSpeed
        self.lifespan = lifespan
        self.ageOfMaturity = ageOfMaturity
        self.visionDistance = visionDistance
        self.pereipheralVision = peripheralVision
        self.maxEnergy = maxEnergy
        self.movementModelWeights = movementModelWeights
        self.movementModel = NN.creatureMovementNN(movementModelWeights[0], movementModelWeights[1], movementModelWeights[2], movementModelWeights[3],
                                                   movementModelWeights[4], movementModelWeights[5], movementModelWeights[6], movementModelWeights[7], 
                                                   movementModelWeights[8], movementModelWeights[9], movementModelWeights[10], movementModelWeights[11])

        # changing stats
        self.x = x
        self.y = y
        self.direction = random.randint(0, 360)
        self.speed = 0
        self.energy = ENERGY_AT_BIRTH
        self.age = 0
        self.plantsInSight = []
        self.shouldDisplay = False
    
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

    def findOptimalPlant(self):
        bestPriority = None
        bestPlant = None
        for plant in self.plantsInSight:
            priority = math.dist((self.x, self.y), (plant[0], plant[1]))
            if bestPriority == None or priority < bestPriority:
                bestPriority = priority
                bestPlant = plant
        return bestPlant

    def TEST_directToBestPlant(self, plant):
        self.direction = (360 + math.degrees(math.atan2((plant[0] - self.x), (plant[1] - self.y) ))) % 360

    def reproduce(self):
        return Creature((max(0, min(255, self.color[0] + random.randint(-10, 10))), 
                        max(0, min(255, self.color[1] + random.randint(-10, 10))), 
                        max(0, min(255, self.color[2] + random.randint(-10, 10)))), 
                        self.radius,# + random.randint(-1, 1),
                        self.maxSpeed,# + random.randint(-1, 1),
                        self.lifespan + random.randint(-10, 10), 
                        self.ageOfMaturity + random.randint(-10, 10), 
                        self.visionDistance + random.randint(-10, 10), 
                        self.pereipheralVision + random.randint(-10, 10),
                        self.maxEnergy + random.uniform(-1, 1), 

                        [[self.movementModelWeights[0][0] + random.uniform(-1, 1), self.movementModelWeights[0][1] + random.uniform(-1, 1), self.movementModelWeights[0][2] + random.uniform(-1, 1), self.movementModelWeights[0][3] + random.uniform(-1, 1)],
                        [self.movementModelWeights[1][0] + random.uniform(-1, 1), self.movementModelWeights[1][1] + random.uniform(-1, 1), self.movementModelWeights[1][2] + random.uniform(-1, 1), self.movementModelWeights[1][3] + random.uniform(-1, 1)],
                        [self.movementModelWeights[1][0] + random.uniform(-1, 1), self.movementModelWeights[2][1] + random.uniform(-1, 1), self.movementModelWeights[2][2] + random.uniform(-1, 1), self.movementModelWeights[2][3] + random.uniform(-1, 1)],
                        [self.movementModelWeights[2][0] + random.uniform(-1, 1), self.movementModelWeights[3][1] + random.uniform(-1, 1), self.movementModelWeights[3][2] + random.uniform(-1, 1), self.movementModelWeights[3][3] + random.uniform(-1, 1)],
                        
                        [self.movementModelWeights[4][0] + random.uniform(-1, 1), self.movementModelWeights[4][1] + random.uniform(-1, 1), self.movementModelWeights[4][2] + random.uniform(-1, 1), self.movementModelWeights[4][3] + random.uniform(-1, 1)],
                        [self.movementModelWeights[5][0] + random.uniform(-1, 1), self.movementModelWeights[5][1] + random.uniform(-1, 1), self.movementModelWeights[5][2] + random.uniform(-1, 1), self.movementModelWeights[5][3] + random.uniform(-1, 1)],
                        [self.movementModelWeights[6][0] + random.uniform(-1, 1), self.movementModelWeights[6][1] + random.uniform(-1, 1), self.movementModelWeights[6][2] + random.uniform(-1, 1), self.movementModelWeights[6][3] + random.uniform(-1, 1)],
                        [self.movementModelWeights[7][0] + random.uniform(-1, 1), self.movementModelWeights[7][1] + random.uniform(-1, 1), self.movementModelWeights[7][2] + random.uniform(-1, 1), self.movementModelWeights[7][3] + random.uniform(-1, 1)],
                        
                        [self.movementModelWeights[8][0] + random.uniform(-1, 1), self.movementModelWeights[8][1] + random.uniform(-1, 1)],
                        [self.movementModelWeights[9][0] + random.uniform(-1, 1), self.movementModelWeights[9][1] + random.uniform(-1, 1)],
                        [self.movementModelWeights[10][0] + random.uniform(-1, 1), self.movementModelWeights[10][1] + random.uniform(-1, 1)],
                        [self.movementModelWeights[11][0] + random.uniform(-1, 1), self.movementModelWeights[11][1] + random.uniform(-1, 1)]],

                        self.x, self.y)

    def displayDetails(self):
        GAME_FONT.render_to(screen, (100, 50), "Energy: " + str(int(self.energy)), (40, 40, 40))
        GAME_FONT.render_to(screen, (100, 100), "Age: " + str(int(self.age)), (40, 40, 40))
        GAME_FONT.render_to(screen, (100, 150), "Lifespan: " + str(int(self.lifespan)), (40, 40, 40))
        GAME_FONT.render_to(screen, (100, 200), "Radius: " + str(int(self.radius)), (40, 40, 40))
        GAME_FONT.render_to(screen, (100, 250), "Direction: " + str(int(self.direction)), (40, 40, 40))
        GAME_FONT.render_to(screen, (100, 300), "Speed: " + str(int(self.speed)), (40, 40, 40))
        GAME_FONT.render_to(screen, (100, 350), "Max Speed: " + str(int(self.maxSpeed)), (40, 40, 40))
        if self.plantsInSight:
            GAME_FONT.render_to(screen, (100, 400), "Plants in Sight: " + str(self.plantsInSight), (40, 40, 40))
            GAME_FONT.render_to(screen, (100, 450), "Angle of Plants: " + str(math.degrees(math.atan2((self.plantsInSight[0][0] - self.x), (self.plantsInSight[0][1] - self.y)))))

        else: GAME_FONT.render_to(screen, (100, 400), "Plants in Sight: None", (40, 40, 40))
        GAME_FONT.render_to(screen, (100, 500), "Framerate: " + str(FRAME_RATE), (40, 40, 40))

class Plant:
    def __init__(self):
        self.x = random.randint(0, SCREEN_WIDTH)
        self.y = random.randint(0, SCREEN_HEIGHT)
    
    def draw(self, screen):
        pygame.draw.circle(screen, (15, 200, 50), (self.x, self.y), 5)

creatures = [Creature((125, 125, 125),  ORIGINAL_RADIUS, ORIGINAL_MAX_SPEED, ORIGINAL_LIFESPAN, ORIGINAL_AGE_OF_MATURITY, 
                                        ORIGINAL_VISION_DISTANCE, ORIGINAL_PERIPHERAL_VISION, ORIGINAL_MAX_ENERGY, 
                                        [[random.uniform(-1, 1), random.uniform(-1, 1), random.uniform(-1, 1), random.uniform(-1, 1)],
                                         [random.uniform(-1, 1), random.uniform(-1, 1), random.uniform(-1, 1), random.uniform(-1, 1)],
                                         [random.uniform(-1, 1), random.uniform(-1, 1), random.uniform(-1, 1), random.uniform(-1, 1)],
                                         [random.uniform(-1, 1), random.uniform(-1, 1), random.uniform(-1, 1), random.uniform(-1, 1)],
                                         [random.uniform(-1, 1), random.uniform(-1, 1), random.uniform(-1, 1), random.uniform(-1, 1)],
                                         [random.uniform(-1, 1), random.uniform(-1, 1), random.uniform(-1, 1), random.uniform(-1, 1)],
                                         [random.uniform(-1, 1), random.uniform(-1, 1), random.uniform(-1, 1), random.uniform(-1, 1)],
                                         [random.uniform(-1, 1), random.uniform(-1, 1), random.uniform(-1, 1), random.uniform(-1, 1)],
                                         [random.uniform(-1, 1), random.uniform(-1, 1)],
                                         [random.uniform(-1, 1), random.uniform(-1, 1)],
                                         [random.uniform(-1, 1), random.uniform(-1, 1)],
                                         [random.uniform(-1, 1), random.uniform(-1, 1)]],
                                        #[[1, 1, 1, 1], [1, 1, 1, 1], [1, 1, 1, 1], [1, 1, 1, 1],
                                        # [1, 1, 1, 1], [1, 1, 1, 1], [1, 1, 1, 1], [1, 1, 1, 1],
                                        # [1, 1], [1, 1], [1, 1], [1, 1]],
                                        random.randint(0, SCREEN_WIDTH), random.randint(0, SCREEN_HEIGHT)) 
                                        for _ in range(STARTING_CREATURES)]

plants = [Plant() for _ in range(STARTING_PLANTS)]

plantRegrow = 0
slowed = False
done = False
while not done:

    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            done = True

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                slowed = not slowed
                while slowed:
                    FRAME_RATE = 3
                else: FRAME_RATE = 60

            # arrow keys speed up/slow down the simulation
            elif event.key == pygame.K_LEFT:
                FRAME_RATE = max(1, FRAME_RATE - 10)
            elif event.key == pygame.K_RIGHT:
                FRAME_RATE = min(500, FRAME_RATE + 10)

        # left click selects creature
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            for creature in creatures:
                creature.shouldDisplay = False
                if math.dist(pygame.mouse.get_pos(), (creature.x, creature.y)) < creature.radius:
                    creature.shouldDisplay = True
        
        # right click deselects creature
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
            for creature in creatures:
                creature.shouldDisplay = False

    screen.fill((255, 255, 255))

    for creature in creatures:
        
        if creature.shouldDisplay:
            creature.displayDetails()

        # creatures update speed and direction
        creature.speed = max(0, min (creature.speed + random.uniform(-1, 1), creature.maxSpeed))
        plant = creature.findOptimalPlant()
        if plant is not None:
            #creature.TEST_directToBestPlant((plant[0], plant[1]))
            speedChange, directionChange = creature.movementModel.determineMovement(plant[0] - creature.x, plant[1] - creature.y, creature.speed, creature.direction)
            directionChange = min(max(-20, directionChange), 20)
            creature.speed = max(0, min (creature.speed + speedChange, creature.maxSpeed))
            creature.direction = (creature.direction + directionChange / 5) % 360
        
        else:
            creature.direction = (creature.direction + random.uniform(-10, 10)) % 360

        creature.move()
        creature.plantsInSight.clear()

        creature.age += 1
        creature.energy -= (CONSTANT_ENERGY_LOSS + creature.speed * ENERGY_LOSS_PER_SPEED)

        # creatures attempt to eat
        for plant in plants:
            if math.dist((creature.x, creature.y), (plant.x, plant.y)) <= creature.radius:
                creature.energy += PLANT_ENERGY
                plants.remove(plant)

            # finds plants within creature's vision
            elif math.dist((creature.x, creature.y), (plant.x, plant.y)) <= creature.visionDistance:
                if abs((360 + math.degrees(math.atan2((plant.x - creature.x), (plant.y - creature.y) ))) % 360 - creature.direction) <= creature.pereipheralVision:
                    creature.plantsInSight.append((plant.x, plant.y))

        # starving and old creatures die
        if creature.energy < 0 or creature.age > creature.lifespan:
            creatures.remove(creature)

        # creatures attempt to reproduce
        if creature.energy > ENERGY_NEEDED_TO_REPRODUCE and creature.age > creature.ageOfMaturity:
            creature.energy -= ENERGY_SPENT_TO_REPRODUCE
            child = creature.reproduce()
            creatures.append(child)

    # new plants grow
    plantRegrow += 1
    if plantRegrow == TIME_FOR_PLANT_GROWTH:
        plants.append(Plant())
        plantRegrow = 0
    for plant in plants:
        plant.draw(screen)

    clock.tick(FRAME_RATE)
    pygame.display.flip()

pygame.quit()