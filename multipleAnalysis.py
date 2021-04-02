import sys
import os
import analyzer
import objects as obj

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
