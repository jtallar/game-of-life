import sys
import os
import analyzer
import objects as obj
import utils

if len(sys.argv) <= 1:
    print("Must run with python multipleAnalysis.py root_directory")
    sys.exit(1)

if sys.argv[1][-1] == '/':
    root_directory = sys.argv[1][:-1:]
else:
    root_directory = sys.argv[1]

obs_dict = {}
root_entries = os.listdir(root_directory)
for directory in root_entries:
    directory = root_directory + '/' + directory
    entries = os.listdir(directory)
    init_percentage = int(directory.split('/')[-1])
    obs_dict[init_percentage] = []
    for filename in entries:
        with open(directory + '/' + filename) as file:
            obs_dict[init_percentage].append(analyzer.analyze_input(file, False))

for percentage, obs_list in obs_dict.items():
    print(obj.Summary(obs_list, percentage))

keys = list(obs_dict.keys())
keys.sort()
sum_values = [obj.Summary(obs_list, percentage) for percentage, obs_list in obs_dict.items()]
sum_values.sort(key=lambda x: x.init_percentage)
utils.init_plotter()

step_values = [x.step.media for x in sum_values]
step_values_err = [x.step.std for x in sum_values]
utils.plot_error_bars(keys, 'input (%)', step_values, 'steps', step_values_err, sum_values[0].step.dec_count)

live_count_slope = [x.live_count_slope.media for x in sum_values]
live_count_slope_err = [x.live_count_slope.std for x in sum_values]
utils.plot_error_bars(keys, 'input (%)', live_count_slope, 'live count slope', live_count_slope_err, sum_values[0].live_count_slope.dec_count)

max_distance_slope = [x.max_distance_slope.media for x in sum_values]
max_distance_slope_err = [x.max_distance_slope.std for x in sum_values]
utils.plot_error_bars(keys, 'input (%)', max_distance_slope, 'max distance slope', max_distance_slope_err, sum_values[0].max_distance_slope.dec_count)

# Hold execution until all plots are closed
utils.hold_execution()