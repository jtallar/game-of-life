from sys import stdin

import objects as obj
import utils

# Read dimension and side length
dim = int(stdin.readline())
N = int(stdin.readline()) # Full side length --> NxN or NxNxN

# Each i list element corresponds to i-th time
live_count = []
furthest_distance_l1 = []
furthest_distance_l2 = []
cur_max_distance = 0
restart = False
for line in stdin:
    if "*" == line.rstrip():
        restart = True
        continue
    if restart:
        # Particle count in current time
        live_count.append(int(line.rstrip()))
        # Initialize furthest distance to 0
        furthest_distance_l1.append(0)
        furthest_distance_l2.append(0)
        restart = False
        continue
    
    # Current time, reading alive particle positions
    cell = obj.Cell.new_from_array(line.split())
    # Update futhest L1 distance
    cur_distance_l1 = cell.distance_to_origin_l1()
    if cur_distance_l1 > furthest_distance_l1[-1]:
        furthest_distance_l1[-1] = cur_distance_l1
    # Update futhest L2 distance
    cur_distance_l2 = cell.distance_to_origin_l2()
    if cur_distance_l2 > furthest_distance_l2[-1]:
        furthest_distance_l2[-1] = cur_distance_l2

step_count = len(live_count)
utils.plot_values(range(0, step_count), live_count)           # Plot live_count=f(t)
utils.plot_values(range(0, step_count), furthest_distance_l1) # Plot furthest_distance_l1=f(t)
utils.plot_values(range(0, step_count), furthest_distance_l2) # Plot furthest_distance_l2=f(t)

# Hold execution until all plots are closed
utils.hold_execution()

# What to measure (one val)