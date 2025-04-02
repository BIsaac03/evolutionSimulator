import math

class creatureMovementNN:
    def __init__(self, AWeights, BWeights, CWeights, DWeights):

        self.AWeights = AWeights
        self.BWeights = BWeights
        self.CWeights = CWeights
        self.DWeights = DWeights

    def determineMovement(self, relativePlantPosition):

        B = [math.tanh(sum([relativePlantPosition[j] * self.AWeights[i][j] for j in range(2)])) for i in range(64)]
        C = [sum([B[j] * self.BWeights[i][j] for j in range(64)]) for i in range(64)]
        D = [math.tanh(sum([C[j] * self.CWeights[i][j] for j in range(64)])) for i in range(32)]
        output = [math.tanh(sum([D[j] * self.DWeights[i][j] for j in range(32)])) for i in range(2)]
        return output
