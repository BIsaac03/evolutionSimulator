import math

class creatureMovementNN:
    def __init__(self, A1, A2, B1, B2, B3, B4, C1, C2, C3, C4):

        self.A1wB1 = A1[0]
        self.A1wB2 = A1[1]
        self.A1wB3 = A1[2]
        self.A1wB4 = A1[3]

        self.A2wB1 = A2[0]
        self.A2wB2 = A2[1]
        self.A2wB3 = A2[2]
        self.A2wB4 = A2[3]

        self.B1wC1 = B1[0]
        self.B1wC2 = B1[1]
        self.B1wC3 = B1[2]
        self.B1wC4 = B1[3]

        self.B2wC1 = B2[0]
        self.B2wC2 = B2[1]
        self.B2wC3 = B2[2]
        self.B2wC4 = B2[3]

        self.B3wC1 = B3[0]
        self.B3wC2 = B3[1]
        self.B3wC3 = B3[2]
        self.B3wC4 = B3[3]

        self.B4wC1 = B4[0]
        self.B4wC2 = B4[1]
        self.B4wC3 = B4[2]
        self.B4wC4 = B4[3]


        self.C1wO1 = C1[0]
        self.C1wO2 = C1[1]

        self.C2wO1 = C2[0]
        self.C2wO2 = C2[1]

        self.C3wO1 = C3[0]
        self.C3wO2 = C3[1]

        self.C4wO1 = C4[0]
        self.C4wO2 = C4[1]

    def determineMovement(self, relativePlantX, relativePlantY):
                
        B1 = math.tanh((relativePlantX * self.A1wB1 + relativePlantY * self.A2wB1))
        B2 = math.tanh((relativePlantX * self.A1wB2 + relativePlantY * self.A2wB2))
        B3 = math.tanh((relativePlantX * self.A1wB3 + relativePlantY * self.A2wB3))
        B4 = math.tanh((relativePlantX * self.A1wB4 + relativePlantY * self.A2wB4))

        C1 = math.tanh((B1 * self.B1wC1 + B2 * self.B2wC1 + B3 * self.B3wC1 + B4 * self.B4wC1))
        C2 = math.tanh((B1 * self.B1wC2 + B2 * self.B2wC2 + B3 * self.B3wC2 + B4 * self.B4wC2))
        C3 = math.tanh((B1 * self.B1wC3 + B2 * self.B2wC3 + B3 * self.B3wC3 + B4 * self.B4wC3))
        C4 = math.tanh((B1 * self.B1wC4 + B2 * self.B2wC4 + B3 * self.B3wC4 + B4 * self.B4wC4))
        
        direction = math.tanh((C1 * self.C1wO1 + C2 * self.C2wO1 + C3 * self.C3wO1 + C4 * self.C4wO1))
        speed = math.tanh((C1 * self.C1wO2 + C2 * self.C2wO2 + C3 * self.C3wO2 + C4 * self.C4wO2))

        return direction, speed
    
    def getWeights(self):
        A1 = [self.A1wB1, self.A1wB2, self.A1wB3, self.A1wB4]
        A2 = [self.A2wB1, self.A2wB2, self.A2wB3, self.A2wB4]

        B1 = [self.B1wC1, self.B1wC2, self.B1wC3, self.B1wC4]
        B2 = [self.B2wC1, self.B2wC2, self.B2wC3, self.B2wC4]
        B3 = [self.B3wC1, self.B3wC2, self.B3wC3, self.B3wC4]
        B4 = [self.B4wC1, self.B4wC2, self.B4wC3, self.B4wC4]

        C1 = [self.C1wO1, self.C1wO2]
        C2 = [self.C2wO1, self.C2wO2]
        C3 = [self.C3wO1, self.C3wO2]
        C4 = [self.C4wO1, self.C4wO2]

        return A1, A2, B1, B2, B3, B4, C1, C2, C3, C4

class plantPrioritizationNN:
    def __init__(self, A1, A2, A3, A4, B1, B2, B3, B4, C1, C2, C3, C4):

        self.A1wB1 = A1[0]
        self.A1wB2 = A1[1]
        self.A1wB3 = A1[2]
        self.A1wB4 = A1[3]

        self.A2wB1 = A2[0]
        self.A2wB2 = A2[1]
        self.A2wB3 = A2[2]
        self.A2wB4 = A2[3]

        self.A3wB1 = A3[0]
        self.A3wB2 = A3[1]
        self.A3wB3 = A3[2]
        self.A3wB4 = A3[3]

        self.A4wB1 = A4[0]
        self.A4wB2 = A4[1]
        self.A4wB3 = A4[2]
        self.A4wB4 = A4[3]


        self.B1wC1 = B1[0]
        self.B1wC2 = B1[1]
        self.B1wC3 = B1[2]
        self.B1wC4 = B1[3]

        self.B2wC1 = B2[0]
        self.B2wC2 = B2[1]
        self.B2wC3 = B2[2]
        self.B2wC4 = B2[3]

        self.B3wC1 = B3[0]
        self.B3wC2 = B3[1]
        self.B3wC3 = B3[2]
        self.B3wC4 = B3[3]

        self.B4wC1 = B4[0]
        self.B4wC2 = B4[1]
        self.B4wC3 = B4[2]
        self.B4wC4 = B4[3]


        self.C1wO = C1
        self.C2wO = C2
        self.C3wO = C3
        self.C4wO = C4

    def prioritize(self, relativePlantX, relativePlantY, currentSpeed, currentDirection):
        
        B1 = (relativePlantX * self.A1wB1 + relativePlantY * self.A2wB1 + currentSpeed * self.A3wB1 + currentDirection * self.A4wB1)
        B2 = (relativePlantX * self.A1wB2 + relativePlantY * self.A2wB2 + currentSpeed * self.A3wB2 + currentDirection * self.A4wB2)
        B3 = (relativePlantX * self.A1wB3 + relativePlantY * self.A2wB3 + currentSpeed * self.A3wB3 + currentDirection * self.A4wB3)
        B4 = (relativePlantX * self.A1wB4 + relativePlantY * self.A2wB4 + currentSpeed * self.A3wB4 + currentDirection * self.A4wB4)

        C1 = (B1 * self.B1wC1 + B2 * self.B2wC1 + B3 * self.B3wC1 + B4 * self.B4wC1)
        C2 = (B1 * self.B1wC2 + B2 * self.B2wC2 + B3 * self.B3wC2 + B4 * self.B4wC2)
        C3 = (B1 * self.B1wC3 + B2 * self.B2wC3 + B3 * self.B3wC3 + B4 * self.B4wC3)
        C4 = (B1 * self.B1wC4 + B2 * self.B2wC4 + B3 * self.B3wC4 + B4 * self.B4wC4)
        
        priority = (C1 * self.C1wO + C2 * self.C2wO + C3 * self.C3wO + C4 * self.C4wO)

        return priority 