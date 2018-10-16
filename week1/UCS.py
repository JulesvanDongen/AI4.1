from collections import deque

from week1.Algorithm import Algorithm


class UCS(Algorithm):
    NAME = "UCS"

    unvisited = deque()

    def nextIteration(self):
        # 1. Take an unvisited node
        nextPos = self.unvisited.pop()
        # print(f"Next position: {nextPos}")
        # print(f"Unvisited positions: {self.unvisited}")

        # 2. Draw the line from the previous position to the next position
        for pos in self.getSurroundingPositions(nextPos):
            x,y = pos
            if self.internalGrid[x][y] == 0:
                self.markCheckingPosition(pos, nextPos)

        # 3a. Check if that is the solution
        if nextPos == (len(self.grid) -1, len(self.grid[0]) -1):
            # This is the solution, remove everything from the unvisited queue and draw the path
            print(self.unvisited)
            self.unvisited = deque()
            print("Found final position")

        # 3b. Else, find the surrounding positions, add them to the surrounding nodes and mark the current spot as visited
        else:
            x,y = nextPos
            self.internalGrid[x][y] = 0
            self.appendSurroundingPositions(nextPos)

    def hasNextIteration(self):
        return len(self.unvisited) > 0 and self.shouldStop == False

    def initialize(self):
        super().initialize()
        self.unvisited = deque()
        self.appendSurroundingPositions((0,0))

    def appendSurroundingPositions(self, position):
        for pos in self.getSurroundingPossiblePositions(position):
            if pos not in self.unvisited:
                self.unvisited.appendleft(pos)