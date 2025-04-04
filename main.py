import NN

import pygame
import pygame.freetype
import math
import random

SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 600

FRAME_RATE = 60
STARTING_CREATURES = 15
STARTING_PLANTS = 70

ORIGINAL_RADIUS = 10
ORIGINAL_MAX_SPEED = 3
ORIGINAL_LIFESPAN = 500
ORIGINAL_AGE_OF_MATURITY = 200
ORIGINAL_VISION_DISTANCE = 150
ORIGINAL_PERIPHERAL_VISION = 45
ORIGINAL_MAX_ENERGY = 500 
CONSTANT_ENERGY_LOSS = 0.05
ENERGY_LOSS_PER_SPEED = 0.1
ENERGY_NEEDED_TO_REPRODUCE = 200
ENERGY_SPENT_TO_REPRODUCE = 100
ENERGY_AT_BIRTH = 150

timeForPlantGrowth = 10
plantEnergy = 150

# Neural Network Variables
L1NEURONS = 256
L2NEURONS = 128
L3NEURONS = 32
normalMutationStd = 0.01
majorMutationStd = 0.3

def creatureNNMutation():
    chance = random.randint(1, 100)
    if chance == 100:
        return random.gauss(0, majorMutationStd)
    else: return random.gauss(0, normalMutationStd)

# SIMULATION SETUP
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
DISPLAY_FONT = pygame.freetype.SysFont('Comic Sans MS', 30)
LABEL_FONT = pygame.freetype.SysFont('Comic Sans MS', 15)
pygame.display.set_caption("Interactive Evolution Simulator")
try:
    SETTINGS_ICON = pygame.image.load("settings.png")
except pygame.error as e:
    print(f"Error loading image: {e}")
    pygame.quit()
    exit()
SETTINGS_ICON = pygame.transform.scale(SETTINGS_ICON, (40, 40))
clock = pygame.time.Clock()

class Creature:
    def __init__(self, generation, color, radius, maxSpeed, lifespan, ageOfMaturity, visionDistance, peripheralVision, maxEnergy, movementModelWeights, x, y,):
        # immutable characteristics
        self.generation = generation
        self.color = color
        self.radius = radius
        self.maxSpeed = maxSpeed
        self.lifespan = lifespan
        self.ageOfMaturity = ageOfMaturity
        self.visionDistance = visionDistance
        self.pereipheralVision = peripheralVision
        self.maxEnergy = maxEnergy
        self.movementModelWeights = movementModelWeights
        self.movementModel = NN.creatureMovementNN([[movementModelWeights[0][i][j] for j in range(2)] for i in range (L1NEURONS)], 
                                                   [[movementModelWeights[1][i][j] for j in range(L1NEURONS)] for i in range (L2NEURONS)], 
                                                   [[movementModelWeights[2][i][j] for j in range(L2NEURONS)]for i in range (L3NEURONS)], 
                                                   [[movementModelWeights[3][i][j] for j in range(L3NEURONS)] for i in range (2)])
        
        # changing stats
        self.x = x
        self.y = y
        self.direction = random.randint(-180, 180)
        self.desiredDirection = None
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
        self.x = max(300, min(SCREEN_WIDTH, self.x))
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

    def reproduce(self):
        return Creature(self.generation + 1,
                        (max(0, min(255, self.color[0] + random.randint(-10, 10))),
                        max(0, min(255, self.color[1] + random.randint(-10, 10))), 
                        max(0, min(255, self.color[2] + random.randint(-10, 10)))), 
                        self.radius,# + random.randint(-1, 1),
                        self.maxSpeed,# + random.randint(-1, 1),
                        self.lifespan + random.randint(-10, 10), 
                        self.ageOfMaturity + random.randint(-10, 10), 
                        self.visionDistance + random.randint(-10, 10), 
                        self.pereipheralVision + random.randint(-10, 10),
                        self.maxEnergy + random.uniform(-1, 1), 
                        
                        [[[self.movementModelWeights[0][i][j] + creatureNNMutation() for j in range(2)] for i in range(L1NEURONS)],
                        [[self.movementModelWeights[1][i][j] + creatureNNMutation() for j in range(L1NEURONS)] for i in range(L2NEURONS)],
                        [[self.movementModelWeights[2][i][j] + creatureNNMutation() for j in range(L2NEURONS)] for i in range(L3NEURONS)],
                        [[self.movementModelWeights[3][i][j] + creatureNNMutation() for j in range(L3NEURONS)] for i in range(2)]],

                        self.x, self.y)

    def displayDetails(self):
        DISPLAY_FONT.render_to(screen, (10, 100), "Generation: " + str(int(self.generation)), (40, 40, 40))
        DISPLAY_FONT.render_to(screen, (10, 150), "Energy: " + str(int(self.energy)), (40, 40, 40))
        DISPLAY_FONT.render_to(screen, (10, 200), "Age: " + str(int(self.age)), (40, 40, 40))
        DISPLAY_FONT.render_to(screen, (10, 250), "Lifespan: " + str(int(self.lifespan)), (40, 40, 40))
        if self.desiredDirection != None:
            DISPLAY_FONT.render_to(screen, (10, 300), "Desired Direction: " + str(int(self.desiredDirection)), (40, 40, 40))
        DISPLAY_FONT.render_to(screen, (10, 350), "Speed: " + str(int(self.speed)), (40, 40, 40))
        
        bestPriority = None
        bestPlant = None
        if self.plantsInSight:
            for plant in self.plantsInSight:
                priority = math.dist((self.x, self.y), (plant[0], plant[1]))
                if bestPriority == None or priority < bestPriority:
                    bestPriority = priority
                    bestPlant = plant        

            DISPLAY_FONT.render_to(screen, (10, 400), "Closest Plant: " + str(round(bestPlant[0] - self.x, 2)) + "   " + str(round(bestPlant[1] - self.y, 2)), (40, 40, 40))
            DISPLAY_FONT.render_to(screen, (10, 450), "Direction to Plant: " + str(round(math.degrees(math.atan2((bestPlant[0] - self.x), (bestPlant[1] - self.y))), 2)))

        else: DISPLAY_FONT.render_to(screen, (10, 400), "No Plants in Sight", (40, 40, 40))
        DISPLAY_FONT.render_to(screen, (10, 500), "Framerate: " + str(FRAME_RATE), (40, 40, 40))

        pygame.draw.circle(screen, (0,0,0), (150, 20), 20)
        LABEL_FONT.render_to(screen, (120, 50), "Save NN", (40, 40, 40))
        pygame.draw.circle(screen, (170,50,70), (250, 20), 20)
        LABEL_FONT.render_to(screen, (238, 50), "Cull", (40, 40, 40))

class Plant:
    def __init__(self):
        self.x = random.randint(300, SCREEN_WIDTH)
        self.y = random.randint(0, SCREEN_HEIGHT)
    
    def draw(self, screen):
        pygame.draw.circle(screen, (15, 200, 50), (self.x, self.y), 5)

def displayDividingLine(x):
        pygame.draw.line(screen, (0,0,0), (x, 0), (x, SCREEN_HEIGHT), 1)

def displaySettingsIcon(x, y):
    screen.blit(SETTINGS_ICON, (x, y))
    LABEL_FONT.render_to(screen, (x - 20, 50), "Modify Sim.", (40, 40, 40))

NNfile = open("creatureNN.txt", "r")
trainedNN = eval(NNfile.read())

creatures = [Creature(1, (125, 125, 125),  ORIGINAL_RADIUS, ORIGINAL_MAX_SPEED, ORIGINAL_LIFESPAN, ORIGINAL_AGE_OF_MATURITY, 
                                        ORIGINAL_VISION_DISTANCE, ORIGINAL_PERIPHERAL_VISION, ORIGINAL_MAX_ENERGY, 
                                        #[[[random.uniform(-1, 1) for _ in range(2)] for _ in range(L1NEURONS)],
                                        #[[random.uniform(-1, 1) for _ in range(L1NEURONS)] for _ in range(L2NEURONS)],
                                        #[[random.uniform(-1, 1) for _ in range(L2NEURONS)] for _ in range(L3NEURONS)],
                                        #[[random.uniform(-1, 1) for _ in range(L3NEURONS)] for _ in range(2)]],
                                        trainedNN,
                                        random.randint(300, SCREEN_WIDTH), random.randint(0, SCREEN_HEIGHT)) 
                                        for _ in range(STARTING_CREATURES)]

plants = [Plant() for _ in range(STARTING_PLANTS)]

testTick = 0
plantRegrow = 0
displaySettings = False
paused = False
done = False
while not done:

    while paused:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    paused = not paused

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for creature in creatures:
                    creature.shouldDisplay = False
                    if math.dist(pygame.mouse.get_pos(), (creature.x, creature.y)) < creature.radius:
                        creature.shouldDisplay = True
                        creature.displayDetails()
                if math.dist(pygame.mouse.get_pos(), (30, 150)) < 20:
                    normalMutationStd = float(input("Desired std: "))
                if math.dist(pygame.mouse.get_pos(), (30, 300)) < 20:
                    timeForPlantGrowth = int(input("Desired time: "))

        if displaySettings:
            for creature in creatures:
                    creature.shouldDisplay = False
            DISPLAY_FONT.render_to(screen, (10, 100), "Mutation std: " + str(float(normalMutationStd)), (40, 40, 40))
            screen.blit(SETTINGS_ICON, (10, 130))
            DISPLAY_FONT.render_to(screen, (10, 250), "Time for Plant Growth: " + str(timeForPlantGrowth)), (40, 40, 40)
            screen.blit(SETTINGS_ICON, (10, 280))
        pygame.display.flip()

    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            done = True

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                paused = not paused

            # arrow keys speed up/slow down the simulation
            elif event.key == pygame.K_LEFT:
                FRAME_RATE = max(1, FRAME_RATE - 10)
            elif event.key == pygame.K_RIGHT:
                FRAME_RATE = min(100, FRAME_RATE + 10)


        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            # "modiy sim." button
            if math.dist(pygame.mouse.get_pos(), (50, 25)) < 20:
                paused = True
                displaySettings = True

            # "save NN" button
            if math.dist(pygame.mouse.get_pos(), (150, 20)) < 20:
                for creature in creatures:
                    if creature.shouldDisplay == True:
                        f = open("creatureNN.txt", "w")
                        f.write(str(creature.movementModelWeights))
                        f.close()

            # "cull" button
            if math.dist(pygame.mouse.get_pos(), (250, 20)) < 20:
                for creature in creatures:
                    if creature.shouldDisplay == True:
                        creatures.remove(creature)

            # left click selects creature
            for creature in creatures:
                creature.shouldDisplay = False
                if math.dist(pygame.mouse.get_pos(), (creature.x, creature.y)) < creature.radius:
                    creature.shouldDisplay = True
        
        # right click deselects creature
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
            for creature in creatures:
                creature.shouldDisplay = False

    screen.fill((255, 255, 255))
    displayDividingLine(300)
    displaySettingsIcon(30, 5)

    for creature in creatures:
        
        if creature.shouldDisplay:
            creature.displayDetails()

        # creatures update speed and direction
        creature.speed = 10#max(0, min (creature.speed + random.uniform(-1, 1), creature.maxSpeed))
        plant = creature.findOptimalPlant()
        if plant is not None:
            #creature.desiredDirection = (360 + math.degrees(math.atan2((plant[0] - creature.x), (plant[1] - creature.y) ))) % 360
            output = creature.movementModel.determineMovement([plant[0] - creature.x, plant[1] - creature.y])

            creature.desiredDirection = output[0] * 180             
            adjustment = (creature.desiredDirection - creature.direction + 540) % 360 - 180

            creature.direction = (creature.direction + max(-50, min(50, adjustment)) + 540) % 360 - 180
            #creature.speed = max(0, min (creature.speed + speed, creature.maxSpeed))
        
        else:
            creature.direction = (creature.direction + random.uniform(-10, 10) + 180) % 360 - 180
            creature.desiredDirection = None
            #creature.speed = max(0, min (creature.speed + random.uniform(-1, 1), creature.maxSpeed))

        creature.move()
        creature.plantsInSight.clear()

        creature.age += 1
        creature.energy -= (CONSTANT_ENERGY_LOSS + creature.speed * ENERGY_LOSS_PER_SPEED)

        # creatures attempt to eat
        for plant in plants:
            if math.dist((creature.x, creature.y), (plant.x, plant.y)) <= creature.radius:
                creature.energy += plantEnergy
                plants.remove(plant)

            # finds plants within creature's vision
            elif math.dist((creature.x, creature.y), (plant.x, plant.y)) <= creature.visionDistance:
                if ((math.degrees(math.atan2((plant.x - creature.x), (plant.y - creature.y))) + 180) % 360 - 180 - creature.direction) <= creature.pereipheralVision:
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
    if plantRegrow > timeForPlantGrowth:
        plants.append(Plant())
        plantRegrow = 0
    for plant in plants:
        plant.draw(screen)

    clock.tick(FRAME_RATE)
    pygame.display.flip()

    testTick += 1

    if testTick == 400:
        d1, speed = creatures[0].movementModel.determineMovement([45, 45])
        d2, speed = creatures[0].movementModel.determineMovement([4.5, 4.5])
        d3, speed = creatures[0].movementModel.determineMovement([20, 0])
        d4, speed = creatures[0].movementModel.determineMovement([-200, 0])
        d5, speed = creatures[0].movementModel.determineMovement([0, -200])
        d6, speed = creatures[0].movementModel.determineMovement([0, 200])
        d7, speed = creatures[0].movementModel.determineMovement([-50, -50])
        d8, speed = creatures[0].movementModel.determineMovement([35, -35])

        print("45      ", d1 * 180)
        print("45      ", d2 * 180)
        print("90      ", d3 * 180)
        print("-90     ", d4 * 180)
        print("+/- 180 ", d5 * 180)
        print("0       ", d6 * 180)
        print("-135    ", d7 * 180)
        print("135     ", d8 * 180)
        testTick = 0

pygame.quit()