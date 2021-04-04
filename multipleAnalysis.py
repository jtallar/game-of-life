import sys
import os
import analyzer
import objects as obj
import utils

if len(sys.argv) <= 1:
    print("Must run with python multipleAnalysis.py root_directory [save_dir]")
    sys.exit(1)

save_dir = None
if len(sys.argv) == 3:
    if sys.argv[2][-1] == '/':
        save_dir = sys.argv[2][:-1:]
    else:
        save_dir = sys.argv[2]
    # Create directory if not exists
    try:
        os.mkdir(save_dir)
    except FileExistsError as exc:
        print("save_dir already exists. continuing...")

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
step_values_dec = min([x.step.dec_count for x in sum_values])
save_name = save_dir + '/step.png' if save_dir else None
utils.plot_error_bars(keys, 'input (%)', step_values, 'steps', step_values_err, 1, step_values_dec, save_name=save_name)

live_count_slope = [x.live_count_slope.media for x in sum_values]
live_count_slope_err = [x.live_count_slope.std for x in sum_values]
live_count_slope_dec = min([x.live_count_slope.dec_count for x in sum_values])
save_name = save_dir + '/live_count_slope.png' if save_dir else None
utils.plot_error_bars(keys, 'input (%)', live_count_slope, 'live count slope', live_count_slope_err, 1, live_count_slope_dec, save_name=save_name)

max_distance_slope = [x.max_distance_slope.media for x in sum_values]
max_distance_slope_err = [x.max_distance_slope.std for x in sum_values]
max_distance_slope_dec = min([x.max_distance_slope.dec_count for x in sum_values])
save_name = save_dir + '/max_distance_slope.png' if save_dir else None
utils.plot_error_bars(keys, 'input (%)', max_distance_slope, 'max distance slope', max_distance_slope_err, 1, max_distance_slope_dec, save_name=save_name)

min_distance_slope = [x.min_distance_slope.media for x in sum_values]
min_distance_slope_err = [x.min_distance_slope.std for x in sum_values]
min_distance_slope_dec = min([x.min_distance_slope.dec_count for x in sum_values])
save_name = save_dir + '/min_distance_slope.png' if save_dir else None
utils.plot_error_bars(keys, 'input (%)', min_distance_slope, 'min distance slope', min_distance_slope_err, 1, min_distance_slope_dec, save_name=save_name)

gen_changes_slope = [x.gen_changes_slope.media for x in sum_values]
gen_changes_slope_err = [x.gen_changes_slope.std for x in sum_values]
gen_changes_slope_dec = min([x.gen_changes_slope.dec_count for x in sum_values])
save_name = save_dir + '/gen_changes_slope.png' if save_dir else None
utils.plot_error_bars(keys, 'input (%)', gen_changes_slope, 'gen changes slope', gen_changes_slope_err, 1, gen_changes_slope_dec, save_name=save_name)

if save_dir:
    print(f'Saved plots in {save_dir}/')

# Hold execution until all plots are closed
utils.hold_execution()    