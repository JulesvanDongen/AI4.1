import copy

import matplotlib.pyplot as plt
import random
import time
import itertools
import math
from collections import namedtuple

# Based on Peter Norvig's IPython Notebook on the TSP

City = namedtuple('City', 'x y')
# c1 = City(4,0)
# c2 = City(0,3)

def distance(A, B):
    return math.hypot(A.x - B.x, A.y - B.y)

def try_all_tours(cities):
    "Generate and test all possible tours of the cities and choose the shortest tour."
    tours = alltours(cities)
    return min(tours, key=tour_length)

def alltours(cities):
    # Return a list of tours (a list of lists), each tour a permutation of cities, but
    # each one starting with the same city.
    start = next(iter(cities)) # cities is a set, sets don't support indexing
    return [[start] + list(rest)
            for rest in itertools.permutations(cities - {start})]

def tour_length(tour):
    # The total of distances between each pair of consecutive cities in the tour.
    return sum(distance(tour[i], tour[i-1]) 
               for i in range(len(tour)))

def make_cities(n, width=1000, height=1000):
    # Make a set of n cities, each with random coordinates within a rectangle (width x height).

    random.seed() # the current system time is used as a seed
    # note: if we use the same seed, we get the same set of cities

    return frozenset(City(random.randrange(width), random.randrange(height))
                     for c in range(n))

def plot_tour(tour): 
    # Plot the cities as circles and the tour as lines between them.
    points = list(tour) + [tour[0]]
    plt.plot([p.x for p in points], [p.y for p in points], 'bo-')
    plt.axis('scaled') # equal increments of x and y have the same length
    plt.axis('off')
    plt.show()

def plot_tsp(algorithm, cities):
    # Apply a TSP algorithm to cities, print the time it took, and plot the resulting tour.
    t0 = time.clock()
    tour = algorithm(cities)
    t1 = time.clock()
    print("{} city tour with length {:.1f} in {:.3f} secs for {}"
          .format(len(tour), tour_length(tour), t1 - t0, algorithm.__name__))
    print("Start plotting ...")
    plot_tour(tour)

def nearest_neighbours(cities):
    last_city = next(iter(cities))
    result = [last_city]
    while cities - set(result) != set():
        leftover_cities = cities - set(result)
        closest_city = next(iter(leftover_cities))

        for leftover_city in leftover_cities:
            if distance(last_city, closest_city) > distance(last_city, leftover_city):
                closest_city = leftover_city

        result.append(closest_city)
        last_city = closest_city

    return result

def findBoundingBox(line):
    a, b = line
    xa, ya = a
    xb, yb = b

    return ((min(xa, xb), min(ya, yb)), (max(xa, xb), max(ya, yb)))

def is_point_on_line(point, segment):
    a = ((0,0), (segment[1][0] - segment[0][0], segment[1][1] - segment[0][1]))
    b = (point[0] - segment[0][0], point[1] - segment[0][1])
    r = cross_product(a[1], b)
    return abs(r) < 0.000001

def cross_product(point_a, point_b):
    return point_a[0] * point_b[1] - point_b[0] * point_a[1]

def is_point_right_of_line(line, point):
    a = ((0,0), (line[1][0] - line[0][0], line[1][1] - line[0][1]))
    b = (point[0] - line[0][0], point[1] - line[0][1])
    return cross_product(a[1], b) < 0


def lines_intersect(line_a, line_b):
    a1, a2 = findBoundingBox(line_a)
    b1, b2 = findBoundingBox(line_b)

    # 1, check if bounding boxes intersect
    l1 = a1[0] < b2[0]
    l2 = a2[0] > b1[0]
    l3 = a1[1] < b2[1]
    l4 = a2[1] > b1[1]
    bounding_boxes_intersect = l1 and l2 and l3 and l4

    if not bounding_boxes_intersect: return False

    # 2, does line a intersect segment b
    if not line_intersects_segment(line_a, line_b): return False

    # 3, does line b intersect segment a
    return line_intersects_segment(line_b, line_a)

def find_crossing(route):
    for i in range(len(route)):
        if i == len(route) - 1:
            d = 0
        else:
            d = i+1
        line_a = ((route[i].x, route[i].y), (route[d].x, route[d].y))
        for j in range(len(route)):
            if j == len(route) - 1:
                k = 0
            else:
                k = j+1
            line_b = ((route[j].x, route[j].y), (route[k].x, route[k].y))
            if i != j and i != j+1 and j != i+1 and (i != len(route) -1 and j != 0) and (i != 0 and j != len(route) -1) and lines_intersect(line_a, line_b):
                print(f"Fix crossing {i}, {j}, Lines: {line_a}, {line_b}")
                # Todo: fix this method
                new_crossing = (i, j)
                # if last_crossing == new_crossing:

                # draw_lines((route[i], route[d]), (route[j], route[k]), route)
                return new_crossing

    return None

def swap_edges(crossing, route):
    i, j = crossing

    if i > j:
        last = i + 1
        first = j
    else:
        last = j + 1
        first = i

    slice = route[first:last]
    slice.reverse()

    route[first:last] = slice

def line_intersects_segment(line, segment):
    return is_point_on_line(segment[0], line) or is_point_on_line(segment[1], line) or (is_point_right_of_line(line, segment[0]) ^ is_point_right_of_line(line, segment[1]))


def find_swap_for_crossing(crossing, route):
    test_route = copy.deepcopy(route)
    crossing_options = itertools.permutations([crossing[0], crossing[1], crossing[0] + 1, crossing[1] + 1], 2)
    best_swap = crossing
    swap_edges(best_swap, test_route)
    best_swap_value = tour_length(test_route)
    swap_edges(best_swap, test_route)

    for swap_option in crossing_options:

        swap_edges(swap_option, test_route)

        length = tour_length(test_route)
        if length < best_swap_value:
            best_swap = swap_option
            best_swap_value = length
            print(length)
        else:
            # Swap the edges back
            swap_edges(swap_option, test_route)

    return best_swap


def two_opt(cities):
    route = nearest_neighbours(cities)

    crossing = find_crossing(route)
    while (crossing != None):
        swap = find_swap_for_crossing(crossing, route)

        if swap != None:
            swap_edges(swap, route)
        # swap_edges(crossing, route)
        # plot_tour(route)
        crossing = find_crossing(route)

    return route

# for debugging purposes only
def draw_lines(line_a, line_b, tour):
    points = list(tour) + [tour[0]]
    plt.plot([p.x for p in points], [p.y for p in points], 'bo-')

    points = list(line_a) + [line_a[0]]
    points2 = list(line_b) + [line_b[0]]

    plt.plot([p.x for p in points], [p.y for p in points], 'ro-')
    plt.plot([p.x for p in points2], [p.y for p in points2], 'ro-')

    plt.axis('scaled') # equal increments of x and y have the same length
    plt.axis('off')
    plt.show()

cities = make_cities(50)

plot_tsp(nearest_neighbours, cities)
plot_tsp(two_opt, cities)
# plot_tsp(try_all_tours, cities)

## C.
## Als er een kruising is dan is de lengte van de kruising maximaal. Hierom hoeft er niet gecontroleerd te worden of
## de nieuwe route korter wordt

## E.
## O(n^3)