import math

def sigmoid(val):
    if val < 0:
        return (math.e ** val)/(1 + math.e ** val)
        
    else: return 1/(1 + math.e ** (-val))

class creatureMovementNN:
    def __init__(self, AWeights, BWeights, CWeights, DWeights):

        self.AWeights = AWeights
        self.BWeights = BWeights
        self.CWeights = CWeights
        self.DWeights = DWeights

    def determineMovement(self, relativePlantPosition):

        B = [sigmoid(sum([relativePlantPosition[j] * self.AWeights[i][j] for j in range(2)])) for i in range(256)]
        C = [sigmoid(sum([B[j] * self.BWeights[i][j] for j in range(256)])) for i in range(128)]
        D = [sigmoid(sum([C[j] * self.CWeights[i][j] for j in range(128)])) for i in range(32)]
        output = [math.tanh(sum([D[j] * self.DWeights[i][j] for j in range(32)])) for i in range(2)]
        return output
