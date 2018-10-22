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


cities = make_cities(10)
plot_tsp(nearest_neighbours, cities)
plot_tsp(try_all_tours, cities)
