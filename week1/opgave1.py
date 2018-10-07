def printState(west, east):
    print(f'{west} | {east}')
    pass

def move(animals, fromCoast, toCoast):
    print(f'{animals}, {fromCoast}, {toCoast}')

    if 'F' in fromCoast:
        print(animals)

    pass


west, east = [], ['F', 'G', 'C', 'W']

printState(west, east)

move(['W', 'C'], west, east)
