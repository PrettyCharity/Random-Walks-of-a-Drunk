# -*- coding: utf-8 -*-
"""
Created on Tue Apr  6 16:17:08 2021

@author: ersoy
"""
import matplotlib.pyplot as plt
import math
from Location import *

def walk(f, d, num_steps):
    """Assumes: f a Field, d a Drunk in f, and num_steps an int >= 0.
       Moves d num_steps times; returns the distance between the
       final location and the location at the start of the walk."""
     
    start = f.get_loc(d)
    for s in range(num_steps):
        f.move_drunk(d)
    return start.dist_from(f.get_loc(d))

def sim_walks(num_steps, num_trials, d_class):
    """Assumes num_steps an int >= 0, num_trials an int > 0,
           d_class a subclass of Drunk
       Simulates num_trials walks of num_steps steps each.
       Returns a list of the final distances for each trial"""
       
    Homer = d_class()
    origin = Location(0, 0)
    distances = []
    for t in range(num_trials):
        f = Field()
        f.add_drunk(Homer, origin)
        distances.append(round(walk(f, Homer, num_steps), 1))
    return distances

def drunk_test(walk_lenghts, num_trials, d_class):
    """Assumes walk_lenghts a sequence of ints >= 0
           num_trials an int > 0, d_class a subclass of Drunk
       For each number of steps in walk_lenghts, runs sim_walks with
           num_trials walk and prints results"""
    
    for num_steps in walk_lenghts:
        distances = sim_walks(num_steps, num_trials, d_class)
        print(d_class.__name__, 'walk of', num_steps, 'steps: Mean =',
              f'{sum(distances)/len(distances):.3f}, Max =',
              f'{max(distances)}, Min = {min(distances)}')

def sim_all(drunk_kinds, walk_lenghts, num_trials):
    
    for d_class in drunk_kinds:
        drunk_test(walk_lenghts, num_trials, d_class)
        
def sim_drunk(num_trials, d_class, walk_lenghts):
    
    mean_distances = []
    for num_steps in walk_lenghts:
        print('Starting simulation of', num_steps, 'steps')
        trials = sim_walks(num_steps, num_trials, d_class)
        mean = sum(trials)/len(trials)
        mean_distances.append(mean)
    return mean_distances

def sim_all_plot(drunk_kinds, walk_lenghts, num_trials):
    
    style_choice = style_iterator(('m-', 'r:', 'k-.'))
    for d_class in drunk_kinds:
        cur_style = style_choice.next_style()
        print('Starting simulation of', d_class.__name__)
        means = sim_drunk(num_trials, d_class, walk_lenghts)
        plt.plot(walk_lenghts, means, cur_style, label = d_class.__name__)
    
    plt.title(f'Mean Distance from Origin ({num_trials} trials)')
    plt.xlabel('Number of Steps')
    plt.ylabel('Distance from Origin')
    plt.legend(loc = 'best')
    plt.semilogx()
    plt.semilogy()
    
def get_final_locs(num_steps, num_trials, d_class):
    locs = []
    d = d_class
    for t in range(num_trials):
        f = Field()
        f.add_drunk(d, Location(0, 0))
        for s in range(num_steps):
            f.move_drunk(d)
        locs.append(f.get_loc(d))
    return locs

def plot_locs(drunk_kinds, num_steps, num_trials):
    style_choice = style_iterator(('k+', 'r^', 'mo'))
    for d_class in drunk_kinds:
        locs = get_final_locs(num_steps, num_trials, d_class)
        x_vals, y_vals = [], []
        for loc in locs:
            x_vals.append(loc.get_x())
            y_vals.append(loc.get_y())
        meanX = sum(x_vals) / len(x_vals)
        meanY = sum(y_vals) / len(y_vals)
        cur_style = style_choice.next_style()
        plt.plot(x_vals, y_vals, cur_style, 
                 label = (f'{d_class.__name__} mean loc. = <' +
                          f'{meanX}, {meanY} >'))
        plt.title(f'Location at End of Walks ({num_steps} steps)')
        plt.xlabel('Steps East / West of Origin')
        plt.ylabel('Steps North / South of Origin')
        plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')

def trace_walk(drunk_kinds, num_steps):
    style_choice = style_iterator(('k+', 'r^', 'mo'))
    # f = Field()
    f = Odd_field(1000, 100, 200)
    for d_class in drunk_kinds:
        d = d_class()
        f.add_drunk(d, Location(0, 0))
        locs = []
        for s in range(num_steps):
            f.move_drunk(d)
            locs.append(f.get_loc(d))
        x_vals, y_vals = [], []
        for loc in locs:
            x_vals.append(loc.get_x())
            y_vals.append(loc.get_y())
        cur_style = style_choice.next_style()
        plt.plot(x_vals, y_vals, cur_style, label = d_class.__name__)
        plt.title('Spots Visited on Walk (' + str(num_steps) +' steps)')
        plt.xlabel('Steps East / West of Origin')
        plt.ylabel('Steps North / South of Origin')
        plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')

        
### CODE TESTRUNS

# drunk_test((10, 100, 1000, 10000), 100, Usual_drunk)
# sim_all((Usual_drunk, Cold_drunk, EW_drunk), (100, 1000), 10)
# sim_all_plot((Usual_drunk, Cold_drunk, EW_drunk), (10, 100, 1000, 10000, 100000), 100)
# plot_locs((Usual_drunk, Cold_drunk, EW_drunk), 100, 200)
# trace_walk((Usual_drunk, Cold_drunk, EW_drunk), 200)
trace_walk((Usual_drunk, Cold_drunk, EW_drunk), 500) # For Treachorus Fields example

### Finger exercise p365
# Lengths = [10, 100, 1000, 10000, 100000]
# Sqrt = list(map(lambda x: math.sqrt(x), Lengths))
# Distance = []
# for steps in Lengths:
#     Result = sim_walks(steps, 100, Usual_drunk)
#     Distance.append(sum(Result)/len(Result))

# plt.clf()
# plt.axes(xscale = 'log', yscale = 'log')
# plt.ylabel("Distance from Origin", fontsize = 15)
# plt.xlabel("Number of Steps", fontsize = 15)
# plt.title("Mean Distance from Origin (100 Trials)", fontsize = 15)
# plt.plot(Lengths, Distance, 'b-', label ='Usual_drunk', linewidth = 2.0)
# plt.plot(Lengths, Sqrt, 'g--', label ='sqrt(steps)', linewidth = 2.0)
# plt.legend(loc = 'upper left')

