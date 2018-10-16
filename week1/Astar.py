import math
from collections import deque

from week1.Algorithm import Algorithm
from week1.PriorityQueue import PriorityQueue


class Astar(Algorithm):
    NAME = "A*"

    unvisited = PriorityQueue()
    visited = {}

    def nextIteration(self):
        # 1. Take an unvisited node, find the fastest route on one of the surrounding positions and add this as a route
        nextPos = self.unvisited.pop()
        self.visited[nextPos] = self.findPassedPosWithLowestWeight(nextPos)


        # 2. Draw the line from the previous position to the next position
        for pos in self.getSurroundingPositions(nextPos):
            x,y = pos
            if self.internalGrid[x][y] == 0:
                self.markCheckingPosition(pos, nextPos)

        # 3a. Check if that is the solution
        if nextPos == (len(self.grid) -1, len(self.grid[0]) -1):
            # This is the solution, remove everything from the unvisited queue and draw the path
            self.unvisited = PriorityQueue()

            lastPos = nextPos
            weight, previousPos = self.visited[nextPos]

            while previousPos != None:
                self.markFinalRoute(lastPos, previousPos)
                lastPos = previousPos
                weight, previousPos = self.visited[previousPos]

        # 3b. Else, find the surrounding positions, add them to the surrounding nodes and mark the current spot as visited
        else:
            x,y = nextPos
            self.internalGrid[x][y] = 0
            self.appendSurroundingPositions(nextPos)

    def hasNextIteration(self):
        return len(self.unvisited) > 0 and self.shouldStop == False

    def initialize(self):
        super().initialize()
        self.unvisited = PriorityQueue()
        self.visited = {(0,0): (0, None)}
        self.appendSurroundingPositions((0,0))

    def appendSurroundingPositions(self, position):
        for pos in self.getSurroundingPossiblePositions(position):
            if pos not in self.unvisited:
                self.unvisited.put(pos, self.heuristic(pos))

    def findPassedPosWithLowestWeight(self, position):
        weight = math.inf
        lowestWeightPosition = None
        for passedPosition in self.getSurroundingPassedPositions(position):
            weightBefore, posBefore = self.visited[passedPosition]

            if weightBefore < weight:
                lowestWeightPosition = passedPosition
                weight = weightBefore

        return (weight + 1, lowestWeightPosition)

    def heuristic(self, position):
        return 1 - 1 / ((position[0] - len(self.grid)) ** 2 + (position[1] - len(self.grid[0])) ** 2)