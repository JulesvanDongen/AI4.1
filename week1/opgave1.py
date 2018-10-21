import copy

class State():
    def __init__(self, west, east):
        self.west = frozenset(west)
        self.east = frozenset(east)

    def isFinished(self):
        return self.west == frozenset(['F', 'G', 'C', 'W'])

    def getOptions(self):
        currentCoast = self.getCurrentCoast()

        result = []
        moveset = (currentCoast | {None}) - {'F'}
        for x in moveset:
            n = [m for m in currentCoast if m != x]

            if {'W', 'G'} & set(n) == {'W', 'G'} or {'G', 'C'} & set(n) == {'G', 'C'}:
                pass
            else:
                result.append(x)
        return result

    def getCurrentCoast(self):
        if 'F' in self.west:
            currentCoast = self.west
        else:
            currentCoast = self.east
        return currentCoast

    def move(self, unitMoved):
        newState = copy.deepcopy(self)

        moved_units = {'F'}
        if unitMoved != None:
            moved_units = moved_units | {unitMoved}

        if 'F' in newState.west:
            west = self.west - moved_units
            east = self.east | moved_units
            newState = State(west, east)
        else:
            east = self.east - moved_units
            west = self.west | moved_units
            newState = State(west, east)
        return newState

    def __str__(self) -> str:
        str = ""
        for w in self.west:
            str += w
        str += "|"
        for e in self.east:
            str += e

        return str

    def __key(self):
        return (self.east, self.west)

    def __eq__(self, other):
        return self.__key() == other.__key()

    def __hash__(self):
        return hash(self.__key())


def findFinishedState(state, exploredStateMap, movesDone):
    exploredStateMap[state] = 0

    if state.isFinished():
        return movesDone
    else:
        for move in state.getOptions():
            newState = state.move(move)

            if newState not in exploredStateMap.keys():
                result = findFinishedState(newState, exploredStateMap, movesDone + [move])
                if result != None:
                    return result

        return None



west, east = set(), {'F', 'G', 'C', 'W'} # Begin state

defaultState = State(west, east)
print(f"Finding for state: {defaultState}")
path = findFinishedState(defaultState, {}, [])
print(path)