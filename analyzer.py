import utils
import objects as obj

def analyze_input(source, plot):
    # Read dimension and side length
    dim = int(source.readline())
    N = int(source.readline()) # Full side length --> NxN or NxNxN

    # Each i list element corresponds to i-th time
    live_count = []
    live_count_slope = []

    furthest_distance_l2 = []
    furthest_distance_l2_slope = []
    end_by_border = False

    cur_max_distance = 0
    restart = False
    for line in source:
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
    if end_by_border: ending = obj.Ending.Border
    elif live_count[-1] == 0: ending = obj.Ending.Dead
    else: ending = obj.Ending.Repeated

    observables = obj.Observables(ending, step_count, live_count_slope[-1], furthest_distance_l2_slope[-1])
    # Plot values
    if plot:
        utils.init_plotter()

        utils.plot_values(range(0, step_count), 'tiempo', live_count, 'celdas vivas')               # Plot live_count=f(t)
        utils.plot_values(range(0, step_count), 'tiempo', live_count_slope, 'velocidad celdas vivas')  # Plot live_count_slope=f(t)
        utils.plot_values(range(0, step_count), 'tiempo', furthest_distance_l2, 'radio de patrón')  # Plot furthest_distance_l2=f(t)
        utils.plot_values(range(0, step_count), 'tiempo', furthest_distance_l2_slope, 'velocidad radio de patrón')  # Plot furthest_distance_l2_slope=f(t)

        # Hold execution until all plots are closed
        utils.hold_execution()
    
    return observables