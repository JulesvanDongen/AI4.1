import tkinter as tk
from tkinter import ttk

from week1.Algorithm import Algorithm
# from week1.UCS import UCS

import random
import heapq

#assuming a resulution of 1920 x 1080 = 16 : 9

# hint - implementing a delay of 50ms in tkinter:
#    root.after(50)
#    root.update()

# global color scheme
from week1.UCS import UCS

bgc = '#FDF6E3'
gridc = '#542437'
blockc = 'red'
pathc = 'blue'
startc = '#C7F464'
goalc = 'yellow'

# global vars: grid
SIZE  = 25 # the nr of nodes=grid crossings in a row (or column)
grid  = [[0 for x in range(SIZE)] for y in range(SIZE)]
start = (0, 0)
goal  = (SIZE-1, SIZE-1)

START_FLAG = True # not redraw grid when pressing start first time

# global vars: pixel sizes
CELL  = 35 # size of cell/square in pixels
W  = (SIZE-1) * CELL # width of grid in pixels
H  = W # height of grid
TR = 10 # translate/move the grid, upper left is 10,10

def getAlgorithm(algorithmName):
    # The list of algorithms implemented
    algorithms = {
        UCS.NAME: globals()["UCS"]
    }

    algorithmClass = algorithms[algorithmName]
    return algorithmClass()

class PriorityQueue:
    # to be use in the A* algorithm
    # a wrapper around heapq (aka priority queue), a binary min-heap on top of a list
    # in a min-heap, the keys of parent nodes are less than or equal to those
    # of the children and the lowest key is in the root node
    def __init__(self):
        # create a min heap (as a list)
        self.elements = []
    
    def empty(self):
        return len(self.elements) == 0
    
    # heap elements are tuples (priority, item)
    def put(self, item, priority):
        heapq.heappush(self.elements, (priority, item))
    
    # pop returns the smallest item from the heap
    # i.e. the root element = element (priority, item) with highest priority
    def get(self):
        return heapq.heappop(self.elements)[1]

def bernoulli_trial():
    return 1 if random.random() < int(prob.get())/10 else 0

def get_grid_value(node):
    # node is a tuple (x, y), grid is a 2D list [x][y]
    return grid[node[0]][node[1]]

def set_grid_value(node, value): 
    # node is a tuple (x, y), grid is a 2D list [x][y]
    grid[node[0]][node[1]] = value

def make_grid(c):
    # vertical lines
    for i in range(0, W+1, CELL):
        c.create_line(i+TR, 0+TR, i+TR, H+TR, fill = gridc)

    # horizontal lines
    for i in range(0, H+1, CELL):
        c.create_line(0+TR, i+TR, W+TR, i+TR, fill = gridc)

def init_grid(c):
    for x in range(SIZE):
        for y in range(SIZE):
            node = (x, y)
            if bernoulli_trial():
                set_grid_value(node, 'b') # set as blocked
                plot_node(c, node, color=blockc)
            else:
                set_grid_value(node, -1)  # init costs, -1 means infinite

    # start and goal cannot be bloking nodes
    set_grid_value(start, 0)
    set_grid_value(goal, -1)

def plot_line_segment(c, x0, y0, x1, y1, color):
    c.create_line(x0*CELL+TR, y0*CELL+TR, x1*CELL+TR, y1*CELL+TR, fill = color, width = 2)

def plot_node(c, node, color):
    # size of (red) rectangle is 8 by 8
    x0 = node[0] * CELL - 4
    y0 = node[1] * CELL - 4
    x1 = x0 + 8 + 1
    y1 = y0 + 8 + 1
    c.create_rectangle(x0+TR, y0+TR, x1+TR, y1+TR, fill = color)

def control_panel():
    mf = ttk.LabelFrame(right_frame)
    mf.grid(column=0, row=0, padx=8, pady=4)
    mf.grid_rowconfigure(2, minsize=10)

    def start_search():
        global START_FLAG
        if not START_FLAG:
            init()
        START_FLAG = False
        # start searching
        print(f"Calculating: {bt_alg.get()}")
        algorithm = getAlgorithm(bt_alg.get())
        algorithm.pauseMethod = lambda: root.after(50)
        algorithm.iterate()

    start_button = tk.Button(mf, text="Start", command=start_search, width=10)
    start_button.grid(row=1, column=1, sticky='w', padx=5, pady=5)

    def select_alg():
        print('algorithm =', bt_alg.get())

    r1_button = tk.Radiobutton(mf, text=UCS.NAME, value=UCS.NAME, variable=bt_alg, command=select_alg)
    r2_button = tk.Radiobutton(mf, text='A*', value='A*', variable=bt_alg, command=select_alg)
    bt_alg.set(UCS.NAME)

    r1_button.grid(row=3, column=1, columnspan=2, sticky='w')
    r2_button.grid(row=4, column=1, columnspan=2, sticky='w')

    def box_update1(event):
        print('delay is set to:', box1.get())

    def box_update2(event):
        print('prob. blocking is set to:', box2.get())

    lf = ttk.LabelFrame(right_frame, relief="sunken")
    lf.grid(column=0, row=1, padx=5, pady=5)

    ttk.Label(lf, text="Delay").grid(row=1, column=1, sticky='w')
    box1 = ttk.Combobox(lf, textvariable=delay, state='readonly', width=6)
    box1.grid(row=2, column=1, sticky='w')
    box1['values'] = tuple(str(i) for i in range(5))
    box1.current(1)
    box1.bind("<<ComboboxSelected>>", box_update1)

    ttk.Label(lf, text="Prob. blocking").grid(row=3, column=1, sticky='w')
    box2 = ttk.Combobox(lf, textvariable=prob, state='readonly', width=6)
    box2.grid(row=4, column=1, sticky='ew')
    box2['values'] = tuple(str(i) for i in range(5))
    box2.current(2)
    box2.bind("<<ComboboxSelected>>", box_update2)  

def init():
    canvas.delete("all")
    make_grid(canvas)
    init_grid(canvas)
    # show start and goal nodes
    plot_node(canvas, start, color=startc)
    plot_node(canvas, goal, color=goalc)
    # plot a sample path for demonstration
    for i in range(SIZE-1):
        plot_line_segment(canvas, i, i, i, i+1, color=pathc)
        plot_line_segment(canvas, i, i+1, i+1, i+1, color=pathc)


# create and start GUI
root = tk.Tk()
root.title('A* demo')

delay = tk.StringVar()
prob = tk.StringVar()
bt_alg = tk.StringVar()
left_frame = ttk.Frame(root, padding="3 3 12 12")
left_frame.grid(column=0, row=0)

right_frame = ttk.Frame(root, padding="3 3 12 12")
right_frame.grid(column=1, row=0)

canvas = tk.Canvas(left_frame, height=H+4*TR, width=W+4*TR, borderwidth=-TR, bg = bgc)
canvas.pack(fill=tk.BOTH, expand=True)

control_panel()
init()
root.mainloop()

