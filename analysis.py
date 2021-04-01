import sys
import matplotlib.pyplot as plt

import objects as obj
import utils

if len(sys.argv) <= 1:
    plot_boolean = False
else:
    plot_boolean = (sys.argv[1] == 'plot')

# Read dimension and side length
dim = int(sys.stdin.readline())
N = int(sys.stdin.readline()) # Full side length --> NxN or NxNxN

# Each i list element corresponds to i-th time
live_count = []
live_count_slope = []

furthest_distance_l2 = []
furthest_distance_l2_slope = []
end_by_border = False

cur_max_distance = 0
restart = False
for line in sys.stdin:
    if "*" == line.rstrip():
        restart = True
        continue
    if restart:
        # Particle count in current time
        live_count.append(int(line.rstrip()))
        live_count_slope.append(utils.regression_slope(live_count))
        # Initialize furthest distance to 0
        if furthest_distance_l2:
            furthest_distance_l2_slope.append(utils.regression_slope(furthest_distance_l2))
        furthest_distance_l2.append(0)
        restart = False
        continue
    
    # Current time, reading alive particle positions
    cell = obj.Cell.new_from_array(line.split())
    # Update futhest L2 distance
    cur_distance_l2 = cell.distance_to_origin_l2()
    if cur_distance_l2 > furthest_distance_l2[-1]:
        furthest_distance_l2[-1] = cur_distance_l2
    if cell.is_border_cell(N):
        end_by_border = True
# Add last slope for furthest_distance_l2_slope
furthest_distance_l2_slope.append(utils.regression_slope(furthest_distance_l2))

step_count = len(live_count)

# Figure out how it ended
if end_by_border: end_print = 'Got to edge'
elif live_count[-1] == 0: end_print = 'All cells died'
else: end_print = 'Repetition'

# Print stats
print(f'Ended by: {end_print}')
print(f'Total number of generations (including initial one): {step_count}')
print(f'Final live_count slope: {live_count_slope[-1]}')
print(f'Final futhest_distance slope: {furthest_distance_l2_slope[-1]}')

# Plot values
if plot_boolean:
    plt.rcParams.update({'font.size': 20})

    utils.plot_values(range(0, step_count), 'tiempo', live_count, 'celdas vivas')               # Plot live_count=f(t)
    utils.plot_values(range(0, step_count), 'tiempo', live_count_slope, 'velocidad celdas vivas')  # Plot live_count_slope=f(t)
    utils.plot_values(range(0, step_count), 'tiempo', furthest_distance_l2, 'radio de patrón')  # Plot furthest_distance_l2=f(t)
    utils.plot_values(range(0, step_count), 'tiempo', furthest_distance_l2_slope, 'velocidad radio de patrón')  # Plot furthest_distance_l2_slope=f(t)

    # Hold execution until all plots are closed
    utils.hold_execution()
