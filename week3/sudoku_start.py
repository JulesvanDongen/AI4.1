import copy
import time

# helper function
def cross(A, B):
    # cross product of chars in string A and chars in string B
    return [a+b for a in A for b in B]

#   1 2 3 4 .. 9
# A
# B
# C
# D
# ..
# I

digits = '123456789'
rows   = 'ABCDEFGHI'
cols   = digits
cells  = cross(rows, cols) # for 3x3 81 cells A1..9, B1..9, C1..9, ... 

# unit = a row, a column, a box; list of all units
unit_list = ([cross(r, cols) for r in rows] +                             # 9 rows 
             [cross(rows, c) for c in cols] +                             # 9 cols
             [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]) # 9 units
# peers is a dict {cell : list of peers}
# every cell c has 20 peers p (i.e. cells that share a row, col, box)
# units['A1'] is a list of lists, and sum(units['A1'],[]) flattens this list
units = dict((s, [u for u in unit_list if s in u]) for s in cells)
peers = dict((s, set(sum(units[s],[]))-set([s])) for s in cells)

def test():
    # a set of tests that must pass
    assert len(cells) == 81
    assert len(unitlist) == 27
    assert all(len(units[s]) == 3 for s in cells)
    assert all(len(peers[s]) == 20 for s in cells)
    assert units['C2'] == [['A2', 'B2', 'C2', 'D2', 'E2', 'F2', 'G2', 'H2', 'I2'],
                           ['C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8', 'C9'],
                           ['A1', 'A2', 'A3', 'B1', 'B2', 'B3', 'C1', 'C2', 'C3']]
    assert peers['C2'] == set(['A2', 'B2', 'D2', 'E2', 'F2', 'G2', 'H2', 'I2',
                               'C1', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8', 'C9',
                               'A1', 'A3', 'B1', 'B3'])
    print ('All tests pass.')

def display(grid):
    # grid is a dict of {cell: string}, e.g. grid['A1'] = '1234'
    print()
    for r in rows:
        for c in cols:
            v = grid[r+c]
            # avoid the '123456789'
            if v == '123456789':
                v = '.'
            print (''.join(v), end=' ')
            if c == '3' or c == '6': print('|', end='')
        print()
        if r == 'C' or r == 'F':
            print('-------------------')
    print()

def parse_string_to_dict(grid_string):
    # grid_string is a string like '4.....8.5.3..........7......2.....6....   '
    # convert grid_string into a dict of {cell: chars}
    char_list1 = [c for c in grid_string if c in digits or c == '.']
    # char_list1 = ['8', '5', '.', '.', '.', '2', '4', ...  ]
    assert len(char_list1) == 81

    # replace '.' with '1234567'
    char_list2 = [s.replace('.', '123456789') for s in char_list1]

    # grid {'A1': '8', 'A2': '5', 'A3': '123456789',  }
    return dict(zip(cells, char_list2))

def no_conflict(grid, c, v):
    # check if assignment is possible: value v not a value of a peer
    for p in peers[c]:
        if grid[p] == v:
           return False # conflict
    return True

def grid_complete(grid):
    for position in grid:
        if len(grid[position]) > 1:
            return False
        elif not no_conflict(grid, position, grid[position]):
            return False

    return True

def solve(grid):
    # backtracking search a solution (DFS)
    # your code here
    def search(grid):

        # first check which solutions are possible for each unset space before starting to solve it, repeat until no values are changed\
        # if a space has no possibilities, the grid is incorrect
        peer_changed = True
        while peer_changed:
            peer_changed = False
            for element in grid:
                value = grid[element]
                if len(value) == 1:
                    for peer in peers[element]:
                        new_value = grid[peer].replace(value, "")
                        if len(new_value) == 0:
                            return None # This grid is not correct
                        elif len(grid[peer]) != len(new_value):
                            grid[peer] = new_value
                            peer_changed = True

        if grid_complete(grid):
            return grid

        result = None
        sorted_grid = list(filter(lambda e: len(e[1]) > 1, sorted(grid.items(), key=lambda e: len(e[1]))))

        for position, value in sorted_grid:
            for option in list(grid[position]):
                if no_conflict(grid, position, option): # If the move is possible, do it
                    new_grid = copy.deepcopy(grid)
                    new_grid[position] = option

                    # print(f"Option {option} from {grid[position]}, position {position} for depth {depth} + 1")
                    # display(new_grid)

                    result = search(new_grid)

                    if result != None:
                        return result

        return result


    result = search(grid)
    display(result)

# Todo: remove when done
# This is a partial solution to have the algorithm solve the Sudoku quicker
s0 = '4173698256321589479587243168254371697915864323469127582896435715732.1...1.4......' #
s00 = '4173698256321589479..7......2.....6.....8.4......1.......6.3.7.5.32.1...1.4......' # Use this to show speed improvement
# solve(parse_string_to_dict(s0))

# minimum nr of clues for a unique solution is 17
s1 = '4.....8.5.3..........7......2.....6.....8.4......1.......6.3.7.5..2.....1.4......'
s2 = '85...24..72......9..4.........1.7..23.5...9...4...........8..7..17..........36.4.'
s3 = '...5....2...3..85997...83..53...9...19.73...4...84...1.471..6...5...41...1...6247'
s4 = '.....6....59.....82....8....45........3........6..3.54...325..6..................'
s5 = '4.....8.5.3..........7......2.....6.....8.4......1.......6.3.7.5..2.....1.4......'
s6 = '8..........36......7..9.2...5...7.......457.....1...3...1....68..85...1..9....4..'
s7 = '6..3.2....5.....1..........7.26............543.........8.15........4.2........7..'
s8 = '.6.5.1.9.1...9..539....7....4.8...7.......5.8.817.5.3.....5.2............76..8...'
s9 = '..5...987.4..5...1..7......2...48....9.1.....6..2.....3..6..2.......9.7.......5..'
s10 = '3.6.7...........518.........1.4.5...7.....6.....2......2.....4.....8.3.....5.....'
s11 = '1.....3.8.7.4..............2.3.1...........958.........5.6...7.....8.2...4.......'
s12 = '6..3.2....4.....1..........7.26............543.........8.15........4.2........7..'
s13 = '....3..9....2....1.5.9..............1.2.8.4.6.8.5...2..75......4.1..6..3.....4.6.'
s14 = '45.....3....8.1....9...........5..9.2..7.....8.........1..4..........7.2...6..8..'

slist = [ s1, s2, s3, s4, s5, s6, s7, s8, s9, s10, s11, s12, s13, s14]

for s in slist:
    d = parse_string_to_dict(s)
    display(d)
    start_time = time.time()
    solve(d)
    print(time.time()-start_time)

