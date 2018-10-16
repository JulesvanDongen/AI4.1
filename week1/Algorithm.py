import copy
from abc import ABC, abstractmethod

class Algorithm(ABC):

    pauseMethod = lambda: None
    markCheckingPosition = lambda posFrom, posTo: None
    markFinalRoute = lambda posFrom, posTo: None
    grid = None
    internalGrid = None

    shouldStop = False

    @abstractmethod
    def nextIteration(self):
        pass

    @abstractmethod
    def hasNextIteration(self):
        pass

    def initialize(self):
        self.internalGrid = copy.deepcopy(self.grid)

    def iterate(self):
        self.initialize()
        while self.hasNextIteration():
            self.nextIteration()
            self.pauseMethod()

    def stop(self):
        self.shouldStop = True

    def getSurroundingPositions(self, position):
        x, y = position
        possiblePositions = []

        if x != 0:
            possiblePositions.append((x - 1, y))
        if x != len(self.grid) - 1:
            possiblePositions.append((x + 1, y))
        if y != 0:
            possiblePositions.append((x, y - 1))
        if y != len(self.grid[x]) - 1:
            possiblePositions.append((x, y + 1))

        return possiblePositions

    def getSurroundingPossiblePositions(self, position):
        possiblePositions = self.getSurroundingPositions(position)

        result = []
        for pos in possiblePositions:
            posx, posy = pos
            if self.internalGrid[posx][posy] == -1:
                result.append(pos)

        return result

    def getSurroundingPassedPositions(self, position):
        possiblePositions = self.getSurroundingPositions(position)

        result = []
        for pos in possiblePositions:
            x,y = pos
            if self.internalGrid[x][y] == 0:
                result.append(pos)

        return result