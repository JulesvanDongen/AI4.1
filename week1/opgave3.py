import copy

board = [
    [7, 0, 3, 0, 1, 0, 59, 0, 81],
    [0, 0, 0, 33, 34, 57, 0, 0, 0],
    [9, 0, 31, 0, 0, 0, 63, 0, 79],
    [0, 29, 0, 0, 0, 0, 0, 65, 0],
    [11, 12, 0, 0, 39, 0, 0, 66, 77],
    [0, 13, 0, 0, 0, 0, 0, 67, 0],
    [15, 0, 23, 0, 0, 0, 69, 0, 75],
    [0, 0, 0, 43, 42, 49, 0, 0, 0],
    [19, 0, 21, 0, 45, 0, 47, 0, 73]
]

currentPos = [0, 4]
currentValue = 1

def isFinished(board):
    for y in board:
        for x in y:
            if x != -1:
                return False
    return True

def getSurroundingPositions(position, board, stepcount):
    returnedPositions = []
    if position[0] > 0:
        appendedPosition = [position[0] - 1, position[1]]
        boardValue = board[appendedPosition[0]][appendedPosition[1]]
        if boardValue == stepcount:
            return [appendedPosition]
        elif boardValue == 0:
            returnedPositions.append(appendedPosition)
    if position[0] < len(board) - 1:
        appendedPosition = [position[0] + 1, position[1]]
        boardValue = board[appendedPosition[0]][appendedPosition[1]]
        if boardValue == stepcount:
            return [appendedPosition]
        elif boardValue == 0:
            returnedPositions.append(appendedPosition)
    if position[1] > 0:
        appendedPosition = [position[0], position[1] - 1]
        boardValue = board[appendedPosition[0]][appendedPosition[1]]
        if boardValue == stepcount:
            return [appendedPosition]
        elif boardValue == 0:
            returnedPositions.append(appendedPosition)
    if position[1] < len(board[0]) - 1:
        appendedPosition = [position[0], position[1] + 1]
        boardValue = board[appendedPosition[0]][appendedPosition[1]]
        if boardValue == stepcount:
            return [appendedPosition]
        elif boardValue == 0:
            returnedPositions.append(appendedPosition)

    return returnedPositions

def move(moves, board):
    # Put the last move on the board
    lastMove = moves[len(moves)-1]
    newboard = board.copy()
    newboard[lastMove[0]][lastMove[1]] = -1

    if isFinished(newboard):
        return moves
    else:
        # Find the possible moves, if there are no possible moves left which can be used, return Null
        # print(getSurroundingPositions(lastMove, board))
        possiblePositions = getSurroundingPositions(lastMove, newboard, len(moves) + 1)

        for pos in possiblePositions:
            newMoves = moves.copy()
            newMoves.append(pos)
            result = move(copy.deepcopy(newMoves), copy.deepcopy(newboard))
            if result is not None:
                return result

        return None
    pass

allMoves = move([currentPos], board)

print(allMoves)


