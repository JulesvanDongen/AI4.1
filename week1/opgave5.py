import copy

from week1.PriorityQueue import PriorityQueue

finalGrid = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]

#
# The Board has some functions which help manipulate it
#
class Board:
    grid = [
        [8, 6, 7],
        [2, 5, 4],
        [3, 0, 1]
    ]

    def swap(self, posFrom, posTo):
        toX, toY = posTo
        fromX, fromY = posFrom
        val = self.grid[toX][toY]
        self.grid[toX][toY] = self.grid[fromX][fromY]
        self.grid[fromX][fromY] = val

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

    def isFinished(self):
        return self.grid == finalGrid

    def getEmptyPosition(self):
        return self.findPositionOfValue(0)

    def findPositionOfValue(self, value):
        for indexi, i in enumerate(self.grid):
            for indexj, j in enumerate(i):
                if j == value:
                    return (indexi, indexj)

    def __str__(self):
        str = ""
        for i in self.grid:
            for j in i:
                str += "{:3}".format(j)
            str += "\n"

        return str

    def __eq__(self, other):
        return self.grid == other.grid

    def __lt__(self, other):
        return self != other

    def clone(self):
        clone = Board()
        clone.grid = copy.deepcopy(self.grid)
        return clone

#
# An A* implementation for the Board
#
class Astar:
    queue = PriorityQueue()
    paths = {}

    def find(self, board):
        if board.isFinished():
            previousPath = self.paths[str(board)]
            result = []
            while previousPath[0] != None:
                move = previousPath[0]
                result.append(board.getEmptyPosition())
                board.swap(board.getEmptyPosition(), move)
                previousPath = self.paths[str(board)]

            return result
        else:
            currentPos = board.getEmptyPosition()
            previousMove, stepCount = self.paths[str(board)]

            for nextPos in board.getSurroundingPositions(currentPos):
                newBoard = board.clone()
                newBoard.swap(currentPos, nextPos)
                self.addIfNotInQueue(newBoard, self.heuristic(newBoard))
                self.addPath(newBoard, currentPos, stepCount + 1)


    def startSearch(self, board):
        self.addIfNotInQueue(board, self.heuristic(board))
        self.paths[str(board)] = (None, 0)
        while not self.queue.empty():
            nextBoard = self.queue.pop()
            result = self.find(nextBoard)
            if result != None:
                return result

    def addPath(self, board, move, stepCount):
        if str(board) not in self.paths.keys():
            self.paths[str(board)] = (move, stepCount)
        else:
            otherMove, otherStepCount = self.paths[str(board)]
            if otherStepCount > stepCount:
                self.paths[str(board)] = (move, stepCount)

    def addIfNotInQueue(self, item, priority):
        if item not in self.queue and str(item) not in self.paths.keys():
            self.queue.put(item, priority)

    def heuristic(self, board):
        heuristicValue = 0
        properBoard = Board()
        properBoard.grid = finalGrid
        for i, row in enumerate(board.grid):
            for j, element in enumerate(row):
                m,n = properBoard.findPositionOfValue(element)
                heuristicValue += (m - i) ** 2 + (n - j) ** 2
        return heuristicValue

#
# Execute the A* algorithm on a default board
#
board = Board()
astar = Astar()
path = astar.startSearch(board)
print(len(path))

print(board)
while len(path) > 0:
    move = path.pop()
    print(move)
    board.swap(board.getEmptyPosition(), move)
    print(board)